from enum import Enum
import requests
import json


class HttpMethod(Enum):
    GET = "get"
    POST = "post"
    PUT = "put"
    DELETE = "delete"


def RequestHandler(url: str, method: HttpMethod, headers: object, data: json):
    try:
        if method == HttpMethod.GET:
            response = requests.get(url, headers=headers)
        elif method == HttpMethod.POST:
            response = requests.post(url, headers=headers, data=data)
        elif method == HttpMethod.PUT:
            response = requests.put(url, headers=headers, data=data)
        elif method == HttpMethod.DELETE:
            response = requests.delete(url, headers=headers)
        else:
            print(f"Invalid method {method} specified.")
            return None
        return response
    except Exception as e:
        print("Error: %s" % e)
        