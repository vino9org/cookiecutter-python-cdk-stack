from os.path import abspath, dirname

from aws_cdk import Stack
{% if cookiecutter.use_lambda == 'y' -%}
from aws_cdk import aws_apigateway as apigateway
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_logs as logs
from aws_cdk import aws_sam as sam
from aws_solutions_constructs.aws_apigateway_lambda import ApiGatewayToLambda

{%- endif %}
from constructs import Construct


class {{ cookiecutter.stack_name }}(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

    def build(self):
        {% if cookiecutter.use_lambda == 'y' -%}
        self.lamdba_with_restapi()
        {%- endif %}
        return self

    {% if cookiecutter.use_lambda == 'y' -%}
    def lamdba_with_restapi(self) -> ApiGatewayToLambda:
        src_dir = abspath(dirname(abspath(__file__)) + "/../runtime")
        return ApiGatewayToLambda(
            self,
            f"{self.stack_name}-restapi",
            api_gateway_props=apigateway.RestApiProps(
                endpoint_configuration=apigateway.EndpointConfiguration(
                    types=[apigateway.EndpointType.REGIONAL],
                ),
            ),
            lambda_function_props=_lambda.FunctionProps(
                runtime=_lambda.Runtime.PYTHON_3_9,
                handler="app.lambda_handler",
                code=_lambda.Code.from_asset(src_dir),
                layers=[self.powertools_layer("1.24.2")],
                memory_size=512,
                architecture=_lambda.Architecture.ARM_64,
                log_retention=logs.RetentionDays.ONE_WEEK,
            ),
            log_group_props=logs.LogGroupProps(
                retention=logs.RetentionDays.ONE_WEEK,
            ),
        )

    def powertools_layer(self, version: str) -> _lambda.ILayerVersion:
        # Launches SAR App as CloudFormation nested stack and return Lambda Layer
        POWERTOOLS_BASE_NAME = "AWSLambdaPowertools"
        powertools_app = sam.CfnApplication(
            self,
            f"{POWERTOOLS_BASE_NAME}Application",
            location={
                "applicationId": "arn:aws:serverlessrepo:eu-west-1:057560766410:applications/aws-lambda-powertools-python-layer-extras",  # noqa
                "semanticVersion": version,
            },
        )
        powertools_layer_arn = powertools_app.get_att("Outputs.LayerVersionArn").to_string()
        return _lambda.LayerVersion.from_layer_version_arn(self, f"{POWERTOOLS_BASE_NAME}", powertools_layer_arn)
    {%- endif %}
