
import requests
from url import base_url,  login, payload, headers, login1, payload1


class HttpClient:
    def __init__(self):
        self.base_url = base_url
        self.token = None
        self.headers = {}
        self.login()
        self.session = requests.session()

    def login(self):
        try:
            res = requests.post(url=login, headers=headers, json=payload)
            res.raise_for_status()
            self.token = res.json()['data']['token']
            if self.token:
                self.headers['Authorization'] = f'Bearer {self.token}'
            else:
                print('未获取到token')
        except Exception as e:
            print(f"登录失败{e}")

    def request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}{endpoint}"
        res = self.session.request(method, url, **kwargs)
        res.raise_for_status()
        return res

    def get(self, endpoint, **kwargs):
        res = self.request("GET", endpoint, headers=self.headers, **kwargs)
        return res

    def post(self, endpoint, **kwargs):
        res = self.request("POST", endpoint, headers=self.headers, **kwargs)
        return res

    def put(self, endpoint, **kwargs):
        res = self.request("PUT", endpoint, headers=self.headers, **kwargs)
        return res

    def delete(self, endpoint, **kwargs):
        res = self.request("DELETE", endpoint, headers=self.headers, **kwargs)
        return res


class Http:
    def __init__(self):
        self.base_url = base_url
        self.session = requests.session()

    def request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}{endpoint}"
        res = self.session.request(method, url, **kwargs)
        res.raise_for_status()
        return res

    def get(self, endpoint, **kwargs):
        res = self.request("GET", endpoint, **kwargs)
        return res

    def post(self, endpoint, **kwargs):
        res = self.request("POST", endpoint, **kwargs)
        return res




