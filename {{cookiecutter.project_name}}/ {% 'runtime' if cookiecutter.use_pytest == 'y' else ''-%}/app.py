import json
import os
from typing import Any, Dict, Tuple

from aws_lambda_powertools import Logger, Metrics, Tracer
from aws_lambda_powertools.event_handler.api_gateway import ApiGatewayResolver, ProxyEventType, Response
from aws_lambda_powertools.utilities.typing import LambdaContext


def init_monitoring() -> Tuple[Logger, Metrics, Tracer]:
    """initialize logger, metrics and tracer"""
    env = os.environ.get("DEPLOY_ENV", "feature")
    logger = Logger()
    logger.append_keys(env=env)
    metrics = Metrics()
    metrics.set_default_dimensions(env=env)
    tracer = Tracer()

    return logger, metrics, tracer


logger, metrics, tracer = init_monitoring()
app = ApiGatewayResolver(proxy_type=ProxyEventType.APIGatewayProxyEvent)


@app.get("/ping")
def ping():
    return Response(200, "application/json", json.dumps({"message": "hello"}))


def lambda_handler(event: Dict[str, Any], context: LambdaContext):
    logger.debug(event)
    return app.resolve(event, context)
