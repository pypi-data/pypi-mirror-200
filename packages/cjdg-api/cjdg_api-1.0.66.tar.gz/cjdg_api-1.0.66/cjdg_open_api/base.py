'''
@author: renqiukai
@Date: 2020-05-29 10:30:41
@Description: 
@LastEditTime: 2020-06-10 18:32:44
# 开放平台接口基类
'''
import requests
import json
from loguru import logger


def request_accesstoken(acc: str, pwd: str, domain=True, **kwargs) -> str:
    # 请求accesstooke函数
    domain_name = "bms.chaojidaogou.com" if domain else "it.xxynet.com"
    url = f"http://{domain_name}/shopguide/api/auth/logonweb"
    data = {}
    data["loginName"] = acc
    data["password"] = pwd
    data["version"] = "1"
    response = requests.get(url, data)
    if response.status_code == 200:
        # print(response.json())
        accessToken = response.json().get("token")
        return accessToken


class base:
    def __init__(self, token, domain=True, safe=False, app_secret=None):
        self.token = token
        self.domain = domain
        self.safe = safe
        self.app_secret = app_secret

    def request(self, api_name=None, params={}, data={}, json={}, headers={}, method="GET", url=None, **kwargs):

        protocol = "https" if self.safe else "http"
        domain_name = "bms.chaojidaogou.com" if self.domain else "it.xxynet.com"
        host_name = f"{protocol}://{domain_name}/shopguide/api/"
        if not url:
            if host_name not in api_name:
                url = f"{host_name}{api_name}"
                logger.debug(url)

        condition = {}
        if "accessToken" not in params:
            # 没有token自动添加
            params["accessToken"] = self.token
        if "appSecret" not in params:
            # 没有token自动添加
            params["appSecret"] = self.app_secret
        if params:
            condition["params"] = params
        if data:
            condition["data"] = data
        if json:
            condition["json"] = json
        if headers:
            condition["headers"] = headers

        if method == "GET":
            response = requests.get(url, **condition, timeout=10)
        elif method == "POST":
            response = requests.post(url, **condition, timeout=10)
        else:
            raise ValueError("请求方法错误。")
        if response.status_code == 200:
            return self.response(response.json())

    def response(self, response_raw):
        return response_raw


class baseApi:
    def __init__(self, token, domain=True, safe=False, app_secret=None):
        self.token = token
        self.domain = domain
        self.safe = safe
        self.app_secret = app_secret

    def request(self, api_name=None, params={}, data={}, json={}, headers={}, method="GET", url=None, **kwargs):

        protocol = "https" if self.safe else "http"
        domain_name = "api.xxynet.com" if self.domain else "it.xxynet.com"
        host_name = f"{protocol}://{domain_name}/"
        if not url:
            if host_name not in api_name:
                url = f"{host_name}{api_name}"
        condition = {}

        if "accessToken" not in params:
            # 没有token自动添加
            params["accessToken"] = self.token
        if "appSecret" not in params:
            # 没有token自动添加
            params["appSecret"] = self.app_secret
        if params:
            condition["params"] = params
        if data:
            condition["data"] = data
        if json:
            condition["json"] = json
        if headers:
            condition["headers"] = headers

        if method == "GET":
            response = requests.get(url, **condition, timeout=10)
        elif method == "POST":
            response = requests.post(url, **condition, timeout=10)
        else:
            raise ValueError("请求方法错误。")
        if response.status_code == 200:
            return self.response(response.json())

    def response(self, response_raw):
        return response_raw


class baseSub:
    def __init__(self, token, domain=True, safe=False, app_secret=None):
        self.token = token
        self.domain = domain
        self.safe = safe
        self.app_secret = app_secret


    def request(self, api_name=None, params={}, data={}, json={}, headers={}, method="GET", url=None,**kwargs):

        protocol = "https" if self.safe else "http"
        domain_name = "sub.chaojidaogou.com" if self.domain else "it.xxynet.com"
        host_name = f"{protocol}://{domain_name}/shopguide/api/"
        if not url:
            if host_name not in api_name:
                url = f"{host_name}{api_name}"
        condition = {}

        if "accessToken" not in params:
            # 没有token自动添加
            params["accessToken"] = self.token
        if "appSecret" not in params:
            # 没有token自动添加
            params["appSecret"] = self.app_secret
        if params:
            condition["params"] = params
        if data:
            condition["data"] = data
        if json:
            condition["json"] = json
        if headers:
            condition["headers"] = headers

        if method == "GET":
            response = requests.get(url, **condition, timeout=10)
        elif method == "POST":
            response = requests.post(url, **condition, timeout=10)
        else:
            raise ValueError("请求方法错误。")
        if response.status_code == 200:
            return self.response(response.json())

    def response(self, response_raw):
        return response_raw


class baseCient:
    def __init__(self, token, domain=True, safe=False, app_secret=None):
        self.token = token
        self.domain = domain
        self.safe = safe
        self.app_secret = app_secret

    def request(self, api_name=None, params={}, data={}, json={}, headers={}, method="GET", url=None,**kwargs):

        protocol = "https" if self.safe else "http"
        domain_name = "cient.chaojidaogou.com" if self.domain else "it.xxynet.com"
        host_name = f"{protocol}://{domain_name}/shopguide/api/"
        if not url:
            if host_name not in api_name:
                url = f"{host_name}{api_name}"
        condition = {}

        if "accessToken" not in params:
            # 没有token自动添加
            params["accessToken"] = self.token
        if "appSecret" not in params:
            # 没有token自动添加
            params["appSecret"] = self.app_secret
        if params:
            condition["params"] = params
        if data:
            condition["data"] = data
        if json:
            condition["json"] = json
        if headers:
            condition["headers"] = headers

        if method == "GET":
            response = requests.get(url, **condition, timeout=10)
        elif method == "POST":
            response = requests.post(url, **condition, timeout=10)
        else:
            raise ValueError("请求方法错误。")
        if response.status_code == 200:
            return self.response(response.json())

    def response(self, response_raw):
        return response_raw


class baseApixxYent:
    def __init__(self, token, domain=True, safe=False, app_secret=None):
        self.token = token
        self.domain = domain
        self.safe = safe
        self.app_secret = app_secret

    def request(self, api_name=None, params={}, data={}, json={}, headers={}, method="GET", url=None, **kwargs):
        protocol = "https" if self.safe else "http"
        domain_name = "api.xxynet.com" if self.domain else "it.xxynet.com"
        host_name = f"{protocol}://{domain_name}/"
        if not url:
            if host_name not in api_name:
                url = f"{host_name}{api_name}"
                logger.debug(url)
        condition = {}

        if "accessToken" not in params:
            # 没有token自动添加
            params["accessToken"] = self.token
        if "appSecret" not in params:
            # 没有token自动添加
            params["appSecret"] = self.app_secret
        if params:
            condition["params"] = params
        if data:
            condition["data"] = data
        if json:
            condition["json"] = json
        if headers:
            condition["headers"] = headers

        if method == "GET":
            response = requests.get(url, **condition, timeout=10)
        elif method == "POST":
            response = requests.post(url, **condition, timeout=10)
        else:
            raise ValueError("请求方法错误。")
        if response.status_code == 200:
            return self.response(response.json())

    def response(self, response_raw):
        return response_raw


class baseQuestion:
    def __init__(self, token, domain=True, safe=False, app_secret=None):
        self.token = token
        self.domain = domain
        self.safe = safe
        self.app_secret = app_secret

    def request(self, api_name=None, params={}, data={}, json={}, headers={}, method="GET", url=None, **kwargs):

        protocol = "https" if self.safe else "http"
        domain_name = "bms.chaojidaogou.com" if self.domain else "it.xxynet.com"
        host_name = f"{protocol}://{domain_name}/shopguide-question/api/"
        if not url:
            if host_name not in api_name:
                url = f"{host_name}{api_name}"

        condition = {}

        if "accessToken" not in params:
            # 没有token自动添加
            params["accessToken"] = self.token
        if "appSecret" not in params:
            # 没有token自动添加
            params["appSecret"] = self.app_secret
        if params:
            condition["params"] = params
        if data:
            condition["data"] = data
        if json:
            condition["json"] = json
        if headers:
            condition["headers"] = headers

        if method == "GET":
            response = requests.get(url, **condition, timeout=10)
        elif method == "POST":
            response = requests.post(url, **condition, timeout=10)
        else:
            raise ValueError("请求方法错误。")
        if response.status_code == 200:
            return self.response(response.json())

    def response(self, response_raw):
        return response_raw
