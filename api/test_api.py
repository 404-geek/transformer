import json
from config.config import API_URI
from api.api import RequestHandler, HttpMethod


def test_api():
    url = f"{API_URI}/test"
    headers = {"Content-Type": "application/json"}
    data = json.dumps({"mode": "test"})
    response = RequestHandler(url=url, method=HttpMethod.POST, headers=headers, data=data)
    if response != None:
        print(f"Response: {response.text}")