import requests


def RequestHandler(url, method, headers=None, data=None, params=None, json=None, files=None):
    try:
        response = requests.request(
            method,
            url,
            headers,
            data,
            params,
            json,
            files
        )
        return response
    except Exception as e:
        print("Error: %s" % e)
        