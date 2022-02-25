from os.path import abspath, dirname

from aws_cdk import Stack
from aws_cdk import aws_apigateway as apigateway
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_logs as logs
{% if cookiecutter.use_pytest == 'y' -%}
from aws_solutions_constructs.aws_apigateway_lambda import ApiGatewayToLambda
{%- endif %}
from constructs import Construct


class {{ cookiecutter.stack_name }}(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

    def build(self):
{% if cookiecutter.use_pytest == 'y' -%}
        self.lamdba_with_restapi()
{%- endif %}
        return self

{% if cookiecutter.use_pytest == 'y' -%}
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
                layers=[
                    _lambda.LayerVersion.from_layer_version_arn(
                        self,
                        "lambda-powertools-layer",
                        f"arn:aws:lambda:{Stack.of(self).region}:017000801446:layer:AWSLambdaPowertoolsPython:10",
                    )
                ],
                memory_size=512,
                architecture=_lambda.Architecture.ARM_64,
                log_retention=logs.RetentionDays.ONE_WEEK,
            ),
            log_group_props=logs.LogGroupProps(
                retention=logs.RetentionDays.ONE_WEEK,
            ),
        )
{%- endif %}
