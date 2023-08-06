from __future__ import absolute_import

import datetime
import json

import requests


class ApiClient(object):
    def __init__(self, config={}):
        """Contructor"""

        # Base URL of the API
        self.host = "https://connect.mailerlite.com/"

        # Base headers
        self.default_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "MailerLite-Python-SDK-Client",
        }
        self.set_config(config)

    def set_config(self, config={}):
        """API Client Configuration Setter"""

        # Authentication
        self.api_key = config["api_key"] if "api_key" in config.keys() else ""
        self.default_headers["Authorization"] = "Bearer " + self.api_key

        # API version
        if "api_version" in config.keys():
            self.api_version = config["api_version"]
            self.default_headers["X-Version"] = self.api_version

        # Request timeout
        self.timeout = config["timeout"] if "timeout" in config.keys() else 120

    def request(self, method, url, query_params=None, body=None):
        """Requests Wrapper"""

        if method == "POST":
            return requests.post(
                self.host + url,
                data=json.dumps(body),
                params=query_params,
                headers=self.default_headers,
                timeout=self.timeout,
            )
        elif method == "GET":
            return requests.get(
                self.host + url,
                params=query_params,
                headers=self.default_headers,
                timeout=self.timeout,
            )
        elif method == "PUT":
            return requests.put(
                self.host + url,
                data=json.dumps(body),
                params=query_params,
                headers=self.default_headers,
                timeout=self.timeout,
            )
        elif method == "DELETE":
            return requests.delete(
                self.host + url,
                params=query_params,
                headers=self.default_headers,
                timeout=self.timeout,
            )
        else:
            raise ValueError("http method must be `POST`, `GET`, `PUT` or `DELETE`.")
