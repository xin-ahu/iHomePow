
import logging
import requests
from requests.exceptions import HTTPError
from url import base_url, login_url, payload, header, base_url_app, login_url_app, payload_app, header_app
from log import get_logger

log = get_logger()


class HttpClient:
    def __init__(self):
        self.base_url = base_url
        self.session = requests.Session()
        self.token = None
        self.headers = header
        self.login()

        self.base_url_app = base_url_app
        self.session_app = requests.Session()
        self.token_app = None
        self.headers_app = header_app
        self.login_app()

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

    def login_app(self):
        try:
            res = requests.post(login_url_app, json=payload_app, headers=header_app)
            res.raise_for_status()
            self.token_app = res.json()["data"]["token"]
            if self.token_app:
                self.headers_app['Authorization'] = f'Bearer {self.token_app}'
            else:
                raise Exception("token失效")
        except HTTPError as http_err:
            print(f"登录发生错误: {http_err}")
            self.token_app = None

    def request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}{endpoint}"
        resp = self.session.request(method, url, **kwargs)
        resp.raise_for_status()
        return resp

    def request_app(self, method, endpoint, **kwargs):
        url = f"{self.base_url_app}{endpoint}"
        resp = self.session_app.request(method, url, **kwargs)
        # log.debug(f"request {url}, response {resp.status_code}")
        resp.raise_for_status()
        return resp

    def get(self, endpoint, **kwargs):
        resp = self.request("GET", endpoint, headers=self.headers, **kwargs)
        return resp

    def post(self, endpoint, **kwargs):
        resp = self.request("POST", endpoint, headers=self.headers, **kwargs)
        return resp

    def post_app(self, endpoint, **kwargs):
        resp = self.request_app("POST", endpoint, headers=self.headers_app, **kwargs)
        return resp

    def put(self, endpoint, **kwargs):
        resp = self.request("PUT", endpoint, headers=self.headers, **kwargs)
        return resp

    def delete(self, endpoint, **kwargs):
        resp = self.request("DELETE", endpoint, headers=self.headers, **kwargs)
        return resp
