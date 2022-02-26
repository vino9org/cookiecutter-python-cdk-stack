import json
import os.path

import app


def event_from_file(file_name):
    path = os.path.abspath(os.path.dirname(__file__))
    in_f = open(f"{path}/{file_name}", "r")
    payload = json.load(in_f)
    in_f.close()
    return payload


def test_handler_for_apigateway(lambda_context):
    event = event_from_file("events/event_api_1.json")
    ret = app.lambda_handler(event, lambda_context)
    assert ret["statusCode"] == 200
