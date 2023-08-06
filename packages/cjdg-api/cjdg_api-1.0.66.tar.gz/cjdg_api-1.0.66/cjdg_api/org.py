'''
@Author  :   顾一龙 
@Time    :   2023/02/03 11:31:46
@Version :   1.0
@Contact :   世界那么大，你不想走走吗
'''
# Hard to write shit mountain.......


from .base import base


class org(base):
    def __init__(self, token, domain=True, safe=False, app_secret=None):
        super().__init__(token, domain, safe, app_secret)


    # 组织结构:搜索
    def orglistOrgShop(self, data):
        api_name = "orglistOrgShop.jhtml"
        return self.request(api_name=api_name, data=data)

   # 区域管理:搜索
   # 上级区域的搜索
    def orgroleAreaList(self, data):
        api_name = "orgroleAreaList.jhtml"
        return self.request(api_name=api_name, data=data)

    # 区域管理，删除
    def orgdelArea(self, data):
        api_name = "orgdelArea.jhtml"
        return self.request(api_name=api_name, data=data)

    # 新增区域
    # 编辑区域
    def orgeditArea(self, data):
        api_name = "orgeditArea.jhtml"
        return self.request(api_name=api_name, data=data)
    # 新增区域：之后的操作

    def orgareaTree(self, data):
        api_name = "orgareaTree.jhtml"
        return self.request(api_name=api_name, data=data)
