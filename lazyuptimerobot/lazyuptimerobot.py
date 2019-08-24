import os

try:
    from urllib import urlencode


    def urljoin(*args):
        return "".join(args)
except ImportError:
    from urllib.parse import urlencode, urljoin

import requests
import json


class LazyUptimeRobot(object):
    class ResponseFormat(object):
        JSON = "json"
        XML = "xml"

    _DEFAULT_API_URL = "https://api.uptimerobot.com/v2/"

    def __init__(self, api_key, api_url=_DEFAULT_API_URL, format=ResponseFormat.JSON):
        self.api_url = api_url
        self.api_key = api_key
        self.payload = {'api_key': self.api_key,
                        'format': format}

    def __getattr__(self, name):
        if name not in self.__dict__:
            api_endpoint_url = urljoin(self.api_url, name)
            return self.__call_api(api_endpoint_url)
        else:
            return super(LazyUptimeRobot, self).__getattribute__(name)

    def __build_payload(self, params):
        payload = {} or params
        payload.update(self.payload)
        return urlencode(payload)

    def __call_api(self, api_endpoint_url):
        def __inner(**kwargs):
            headers = {
                'cache-control': "no-cache",
                'content-type': "application/x-www-form-urlencoded"
            }
            payload = self.__build_payload(kwargs)
            print(payload)
            resp = requests.request("POST", api_endpoint_url, data=payload, headers=headers)
            return json.loads(resp.text)

        return __inner


if __name__ == "__main__":
    c = LazyUptimeRobot(os.environ['UPTIME_ROBOT_API_KEY'])
    print(c.getMonitors())
    print(c.getAccountDetails())
