'''
@Author  :   顾一龙 
@Time    :   2023/02/03 11:31:46
@Version :   1.0
@Contact :   世界那么大，你不想走走吗
'''
# Hard to write shit mountain.......


from loguru import logger
from .base import base


class org(base):
    def __init__(self, token, domain=True, safe=False, app_secret=None):
        super().__init__(token, domain, safe, app_secret)

    # 组织结构:搜索
    def orglistOrgShop(self, data):
        api_name = "orglistOrgShop.jhtml"
        return self.request(api_name=api_name, data=data)
