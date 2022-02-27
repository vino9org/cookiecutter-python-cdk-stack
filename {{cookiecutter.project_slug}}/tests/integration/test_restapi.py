import requests


def test_restapi(api_base_url, http_api_auth):
    response = requests.get(f"{api_base_url}/ping", auth=http_api_auth)
    assert response.status_code == 200
