import json
import os.path

import app

events_path = os.path.abspath(os.path.dirname(__file__) + "/../events")


def test_handler_for_apigateway(lambda_context):
    with open(f"{events_path}/event_api_1.json", "r") as f:
        event = json.load(f)
        ret = app.lambda_handler(event, lambda_context)
        assert ret["statusCode"] == 200
