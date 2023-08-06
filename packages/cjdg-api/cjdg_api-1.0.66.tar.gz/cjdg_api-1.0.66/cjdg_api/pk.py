# 排行榜PK

from .base import base


class pk(base):

    def __init__(self, token, domain=True, safe=False, app_secret=None):
        super().__init__(token, domain, safe, app_secret)

    # 排行榜PK列表
    def query(self, data):
        api_name = 'om-web/storemanagement/pk/pk/query'
        return self.request(api_name, data)

    # 排行榜新增/编辑
    # 配置必填项和主指标

    def save(self, data):
        api_name = 'om-web/stoermanagement/pk/v2/pk/save'
        return self.request(api_name, data)

    # 配置其他副指标，非必填项

    def pkIndex(self, data):
        api_name = 'om-web/storemanagement/pk/pk/saveOrUpdatePkIndex'
        return self.request(api_name, data)

    # 选择组织/战队

    def player(self, data):
        api_name = 'om-web/storemanagement/pk/v2/pk/savePlayer'
        return self.request(api_name, data)

    # 发布

    def public(self, data):
        api_name = 'om-web/storemanagement/pk/v2/pk/public'
        return self.request(api_name, data)

    # 查看PK基础信息

    def queryDetail(self, data):
        api_name = 'om-web/storemanagement/pk/pk/querydetailselectmenber'
        return self.request(api_name, data)

    # 查看上报明细

    def submitDetail(self, data):
        api_name = 'om-web/storemanagement/pk/pk/querySubmitDetailList4Backend'
        return self.request(api_name, data)

    # 删除PK

    def pkdel(self, data):
        api_name = 'om-web/storemanagement/pk/pk/delete'
        return self.request(api_name, data)


def main():
    token = ""
    a = pk(token=token)
    a.query(data=data)


if __name__ == '__main__':
    main()
