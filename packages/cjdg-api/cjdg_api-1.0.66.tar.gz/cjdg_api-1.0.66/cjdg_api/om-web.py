'''
@Author  :   顾一龙 
@Time    :   2023/03/02 16:47:28
@Version :   1.0
@Contact :   世界那么大，你不想走走吗
'''
# Hard to write shit mountain.......


from .base import baseSub
from .base import base


class om_web(baseSub):

    def __init__(self, token, domain=True, safe=False, convert=False, app_secret=None):
        super().__init__(token, domain, safe, convert, app_secret)

    #    巡店检查表-列表接口
    def list(self, data):
        api_name = "storemanagement/inspection/inspectionform/templatequery.do"
        return self.request(api_name=api_name, data=data)

    # 巡店检查表-新增/编辑保存
    def save(self, data):
        api_name = "storemanagement/inspection/inspectionform/templateallsave.do"
        return self.request(api_name=api_name, data=data)

    # 巡店检查表-发布
    def publish(self, data):
        api_name = "storemanagement/inspection/inspectionform/publish.do"
        return self.request(api_name=api_name, data=data)

    # 巡店检查表-发布后撤销
    def unpublish(self, data):
        api_name = "storemanagement/inspection/inspectionform/unpublish.do"
        return self.request(api_name=api_name, data=data)

    # 巡店检查表-查看
    def templatedetail(self, data):
        api_name = "storemanagement/inspection/inspectionform/templatedetail.do"
        return self.request(api_name=api_name, data=data)

    # 巡店检查表-删除
    def templatedelete(self, data):
        api_name = "storemanagement/inspection/inspectionform/templatedelete.do"
        return self.request(api_name=api_name, data=data)


class om_web1(base):
    def __init__(self, token, app_secret=None):
        super().__init__(token, app_secret)

    # 巡店检查表-设置
    def saveOrEdit(self, data):
        api_name = "shopguide/api/cruiseshop/distance/saveOrEdit"
        return self.request(api_name=api_name, data=data)


# 巡店模板

    # 巡店模板-列表

    def templatequery(self, data):
        api_name = "storemanagement/inspection/template/templatequery.do"
        return self.request(api_name=api_name, data=data)

    # 巡店模板-新增/编辑 保存
    def templateallsave(self, data):
        api_name = "storemanagement/inspection/template/templateallsave.do"
        return self.request(api_name=api_name, data=data)

    # 巡店模板-复制
    def templatecopy(self, data):
        api_name = "storemanagement/inspection/template/templatecopy.do"
        return self.request(api_name=api_name, data=data)

    # 巡店模板-删除
    def templatedelet(self, data):
        api_name = "storemanagement/inspection/template/templatedelete.do"
        return self.request(api_name=api_name, data=data)

    #  巡店报告-列表
    def inspectionquery(self, data):
        api_name = "storemanagement/inspection/storeinspect/inspectionquery.do"
        return self.request(api_name=api_name, data=data)

    # 巡店报告-删除
    def inspectiondelete(self, data):
        api_name = "storemanagement/inspection/storeinspect/inspectiondelete.do"
        return self.request(api_name=api_name, data=data)



