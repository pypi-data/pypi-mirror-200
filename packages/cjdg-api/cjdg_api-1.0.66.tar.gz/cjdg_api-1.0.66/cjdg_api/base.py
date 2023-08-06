# 开放平台接口基类
from loguru import logger
import requests


def get_up_token(cjdg_access_token):
    """
    七牛上传令牌
    """
    url = "http://bms.chaojidaogou.com/shopguide/api/file/qiniu/getUpToken"
    params = {
        "accessToken": cjdg_access_token
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    params["response"] = response
    params["response_raw"] = response.content
    logger.error(params)


def request_accesstoken(acc: str, pwd: str, safe=False, domain=True, **kwargs) -> str:
    # 请求accesstooke函数
    protocol = "https" if safe else "http"
    domain_name = "bms.chaojidaogou.com" if domain else "it.xxynet.com"
    url = f"{protocol}://{domain_name}/shopguide/api/auth/logon"
    data = {}
    data["loginName"] = acc
    data["password"] = pwd
    data["version"] = "1"
    response = requests.get(url, data)
    if response.status_code == 200:
        accessToken = response.json().get("accessToken")
        return accessToken

# domain为真时-取bms。


def request_accesstoken_pc(acc: str, pwd: str, safe=False, domain=True, **kwargs) -> str:
    # 请求accesstooke函数
    protocol = "https" if safe else "http"
    domain_name = "bms.chaojidaogou.com" if domain else "it.xxynet.com"
    url = f"{protocol}://{domain_name}/shopguide/api/auth/logonweb"
    data = {}
    data["loginName"] = acc
    data["password"] = pwd
    data["version"] = "1"
    response = requests.get(url, data)
    if response.status_code == 200:
        accessToken = response.json().get("token")
        return accessToken


class base:
    def __init__(self, token, domain=True, safe=False, app_secret=None):
        self.token = token
        self.domain = domain
        self.safe = safe
        self.app_secret = app_secret

    def request(self, api_name=None, method="GET", url=None, api_prefix="api/", **kwargs):
        protocol = "https" if self.safe else "http"
        domain_name = "bms.chaojidaogou.com" if self.domain else "it.xxynet.com"
        host_name = f"{protocol}://{domain_name}/shopguide/"
        if not url:
            url = f"{host_name}{api_prefix}{api_name}"
        # params
        params = kwargs.get("params", {})
        params["accessToken"] = self.token
        params["appSecret"] = self.app_secret
        kwargs["params"] = params
        # cookies
        cookies = kwargs.get("cookies", {})
        cookies["accessToken"] = self.token
        kwargs["cookies"] = cookies
        logger.debug(url)
        logger.debug(kwargs)
        response = requests.request(
            method=method,
            url=url,
            **kwargs
        )
        if response.status_code == 200:
            return self.response(response.json())
        logger.error(response.text)

    def response(self, response_raw):

        return response_raw


class baseNoapi:
    def __init__(self, token, domain=True, safe=False, app_secret=None):
        self.token = token
        self.domain = domain
        self.safe = safe
        self.app_secret = app_secret

    def request(self, api_name=None, method="GET", url=None, **kwargs):
        protocol = "https" if self.safe else "http"
        domain_name = "bms.chaojidaogou.com" if self.domain else "it.xxynet.com"
        host_name = f"{protocol}://{domain_name}/shopguide/"
        if not url:
            url = f"{host_name}{api_name}"
        # params
        params = kwargs.get("params", {})
        params["accessToken"] = self.token
        params["appSecret"] = self.app_secret
        kwargs["params"] = params
        # cookies
        cookies = kwargs.get("cookies", {})
        cookies["accessToken"] = self.token
        kwargs["cookies"] = cookies
        logger.debug(url)
        logger.debug(kwargs)
        response = requests.request(
            method=method,
            url=url,
            **kwargs
        )
        if response.status_code == 200:
            return self.response(response.json())
        logger.error(response.text)

    def response(self, response_raw):

        return response_raw


class baseT:
    def __init__(self, token, domain=True, safe=False, convert=False, app_secret=None):
        self.token = token
        self.domain = domain
        self.safe = safe
        self.convert = convert
        self.app_secret = app_secret

    def request(self, api_name=None, method="GET", url=None, api_prefix="api/", **kwargs):
        protocol = "https" if self.safe else "http"
        domain_name = "bms.chaojidaogou.com" if self.safe else "it.xxynet.com"
        host_name = f"{protocol}://{domain_name}/"
        if not url:
            # url is None:generate url use hostname+api_prefix+apiname
            url = f"{host_name}{api_prefix}{api_name}" if self.convert else f"{host_name}{api_name}"
        # params
        params = kwargs.get("params", {})
        params["accessToken"] = self.token
        params["appSecret"] = self.app_secret
        kwargs["params"] = params
        # cookies
        cookies = kwargs.get("cookies", {})
        cookies["accessToken"] = self.token
        kwargs["cookies"] = cookies
        logger.debug(url)
        logger.debug(kwargs)
        response = requests.request(
            method=method,
            url=url,
            **kwargs
        )
        if response.status_code == 200:
            return self.response(response.json())
        logger.error(response.text)

    def response(self, response_raw):

        return response_raw


class baseSub:
    def __init__(self, token, domain=True, safe=False, convert=False, app_secret=None):
        self.token = token
        self.domain = domain
        self.safe = safe
        self.convert = convert
        self.app_secret = app_secret

    def request(self, api_name=None, method="GET", url=None, api_prefix="api/",  **kwargs):
        protocol = "https" if self.safe else "http"
        domain_name = "sub.chaojidaogou.com" if self.domain else "it.xxynet.com"
        host_name = f"{protocol}://{domain_name}/"
        if not url:
            # url is None:generate url use hostname+api_prefix+apiname
            url = f"{host_name}{api_prefix}{api_name}" if self.convert else f"{host_name}{api_name}"
        # params
        params = kwargs.get("params", {})
        params["accessToken"] = self.token
        params["appSecret"] = self.app_secret
        kwargs["params"] = params
        # cookies
        cookies = kwargs.get("cookies", {})
        cookies["accessToken"] = self.token
        kwargs["cookies"] = cookies
        logger.debug(url)
        logger.debug(kwargs)
        response = requests.request(
            method=method,
            url=url,
            **kwargs
        )
        if response.status_code == 200:
            return self.response(response.json())
        logger.error(response.text)

    def response(self, response_raw):

        return response_raw


class baseCient:
    def __init__(self, token, domain=True, safe=False, app_secret=None):
        self.token = token
        self.domain = domain
        self.safe = safe
        self.app_secret = app_secret

    def request(self, api_name=None, method="GET", url=None, api_prefix="api/", **kwargs):
        protocol = "https" if self.safe else "http"
        domain_name = "cient.chaojidaogou.com" if self.domain else "it.xxynet.com"
        host_name = f"{protocol}://{domain_name}/"
        if not url:
            # url is None:generate url use hostname+api_prefix+apiname
            url = f"{host_name}{api_prefix}{api_name}"
        # params
        params = kwargs.get("params", {})
        params["accessToken"] = self.token
        params["appSecret"] = self.app_secret
        kwargs["params"] = params
        # cookies
        cookies = kwargs.get("cookies", {})
        cookies["accessToken"] = self.token
        kwargs["cookies"] = cookies
        logger.debug(url)
        logger.debug(kwargs)
        response = requests.request(
            method=method,
            url=url,
            **kwargs
        )
        if response.status_code == 200:
            return self.response(response.json())
        logger.error(response.text)

    def response(self, response_raw):

        return response_raw


class baseApi:
    def __init__(self, token, domain=True, safe=False, app_secret=None):
        self.token = token
        self.domain = domain
        self.safe = safe
        self.app_secret = app_secret

    def request(self, api_name=None, method="GET", url=None, api_prefix="api/", **kwargs):
        protocol = "https" if self.safe else "http"
        domain_name = "api.chaojidaogou.com" if self.domain else "it.xxynet.com"
        host_name = f"{protocol}://{domain_name}/"
        if not url:
            # url is None:generate url use hostname+api_prefix+apiname
            url = f"{host_name}{api_prefix}{api_name}"
        # params
        params = kwargs.get("params", {})
        params["accessToken"] = self.token
        params["appSecret"] = self.app_secret
        kwargs["params"] = params
        # cookies
        cookies = kwargs.get("cookies", {})
        cookies["accessToken"] = self.token
        kwargs["cookies"] = cookies
        logger.debug(url)
        logger.debug(kwargs)
        response = requests.request(
            method=method,
            url=url,
            **kwargs
        )
        if response.status_code == 200:
            return self.response(response.json())
        logger.error(response.text)

    def response(self, response_raw):

        return response_raw


class baseApixxYent:
    def __init__(self, token, domain=True,  app_secret=None):
        self.token = token
        self.domain = domain
        self.app_secret = app_secret

    def request(self, api_name=None, method="GET", url=None, **kwargs):
        domain_name = "api.xxynet.com" if self.domain else "it.xxynet.com"
        host_name = f"https://{domain_name}/"
        if not url:
            # url is None:generate url use hostname+api_prefix+apiname
            url = f"{host_name}{api_name}"
        # params
        params = kwargs.get("params", {})
        params["accessToken"] = self.token
        params["appSecret"] = self.app_secret
        kwargs["params"] = params
        # cookies
        cookies = kwargs.get("cookies", {})
        cookies["accessToken"] = self.token
        kwargs["cookies"] = cookies
        logger.debug(url)
        logger.debug(kwargs)
        response = requests.request(
            method=method,
            url=url,
            **kwargs
        )
        if response.status_code == 200:
            return self.response(response.json())
        logger.error(response.text)

    def response(self, response_raw):

        return response_raw




