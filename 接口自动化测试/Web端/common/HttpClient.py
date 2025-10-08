
import logging
import requests
from requests.exceptions import HTTPError
from web.config.url import base_url, login_url, payload, header
from utls.log import logger


class HttpClient:
    def __init__(self):
        self.base_url = base_url
        self.session = requests.Session()
        self.token = None
        self.headers = {}
        self.login()

    def login(self):
        try:
            res = requests.post(login_url, json=payload, headers=header)
            res.raise_for_status()
            self.token = res.json()["data"]["token"]
            if self.token:
                self.headers['Authorization'] = f'Bearer {self.token}'
            else:
                raise Exception("token失效")
        except HTTPError as http_err:
            print(f"登录发生错误: {http_err}")
            self.token = None

    def request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}{endpoint}"
        resp = self.session.request(method, url, **kwargs)
        logger.debug(f"request {url}, response {resp.status_code}")
        resp.raise_for_status()
        return resp

    def get(self, endpoint, **kwargs):
        resp = self.request("GET", endpoint, headers=self.headers, **kwargs)
        return resp

    def post(self, endpoint, **kwargs):
        resp = self.request("POST", endpoint, headers=self.headers, **kwargs)
        return resp

    def put(self, endpoint, **kwargs):
        resp = self.request("PUT", endpoint, headers=self.headers, **kwargs)
        return resp

    def delete(self, endpoint, **kwargs):
        resp = self.request("DELETE", endpoint, headers=self.headers, **kwargs)
        return resp
