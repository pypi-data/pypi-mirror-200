from cjdg_open_api.base import base
from cjdg_open_api.base import baseApixxYent
'''
@Author  :   顾一龙 
@Time    :   2022/11/27 21:06:23
@Version :   1.0
@Contact :   小爷怕什么就做什么，就是那么拽！
'''
# Hard to write shit mountain......
# 商品清单


class Goods_list(baseApixxYent):

    def __init__(self, token, domain=True, safe=False, app_secret=None):
        super().__init__(token, domain, safe, app_secret)

# 商品清单搜索用例
    def goods_list(self, data):
        api_name = f"enter/goods/center/mgt/goodslist/pageQuery"
        return self.request(api_name=api_name, json=data, method="POST")

# # 商品清单商品组id
    def goods_groud_get_id(self):
        api_name = f"enter/goods/component/extension/goodsBiz/getTemporaryCode"
        data = {"bizType": "SPGL_3", "bizSubType": "SPGL_3_2", "bizId": ""}
        return self.request(api_name=api_name, json=data, method="POST")

# 商品清单用户id
    def goods_user_get_id(self, bizId):
        api_name = f"enter/userCenter/extension/bizSelect/getTemporaryId"
        data = {"bizType": "SPGL_3", "bizSubType": "SPGL_3_1", "bizId": bizId}
        return self.request(api_name=api_name, json=data, method="POST")

# 商品清单查看用例
    def goods_detail(self, data):
        api_name = f"enter/goods/center/mgt/goodslist/detail"
        return self.request(api_name=api_name, json=data, method="POST")

    def goods_list_id(self, data):
        api_name = f"enter/goods/center/mgt/goodslist/pageQuery"
        return self.request(api_name=api_name, json=data, method="POST")

# 商品清单编辑用例
    def goods_findBizCount01(self, data):
        api_name = f"enter/goods/component//extension/goodsBiz/findBizCount"
        return self.request(api_name=api_name, json=data, method="POST")

    def goods_findBizCount02(self, temporaryId):
        api_name = f"enter/userCenter/extension/openBizSelect/findBizCount"
        data = {"bizType": "SPGL_3", "bizSubType": "SPGL_3_1",
                "temporaryId": temporaryId}
        return self.request(api_name=api_name, json=data, method="POST")

    def goods_confirm(self, temporaryId):
        api_name = f"enter/userCenter/extension/newBizSelect/confirm"
        data = {"bizType": "SPGL_3", "bizSubType": "SPGL_3_1",
                "bizId": "", "temporaryId": temporaryId, "realTime": False}
        return self.request(api_name=api_name, json=data, method="POST")

# 添加商品组和商品
    def goods_save(self, temporaryId, group, grouprols):
        api_name = f"enter/goods/component/extension/goodsBiz/save"
        data = {
            "bizType": "SPGL_3",
            "bizSubType": "SPGL_3_2",
            "bizId": "",
            "temporaryId": temporaryId,
            "selectObj": [{
                "objType": "GOODS",
                "objInfo": group
            }, {
                "objType": "GOODSGROUP",
                "objInfo": grouprols
            }],
            "realTime": False
        }
        return self.request(api_name=api_name, json=data, method="POST")

# 商品清单-查询人员用例
    def goods_user_list(self, temporaryId):
        api_name = f"enter/userCenter/extension/user/list"
        data = {"pageNum": 1, "pageSize": 10,
                "queryParameter": {"bizType": "SPGL_3",
                                   "bizSubType": "SPGL_3_1",
                                   "bizId": "",
                                   "temporaryId": temporaryId,
                                   "filterOrgs": [],
                                   "tags": []}}
        return self.request(api_name=api_name, json=data, method="POST")

# 商品清单-查询工号用例
    def goods_user_usercode(self, data):
        api_name = f"enter/userCenter/extension/user/list"

        return self.request(api_name=api_name, json=data, method="POST")


# 商品清单-用户组用例

    def goods_userGroup(self, bizType, bizSubType, temporaryId):
        api_name = f"enter/userCenter/extension/userGroup/list"
        data = {"pageNum": 1, "pageSize": 10,
                "queryParameter": {"bizType": bizType,
                                   "bizSubType": bizSubType,
                                   "bizId": "",
                                   "temporaryId": temporaryId,
                                   "filterOrgs": [],
                                   "tags": []}}
        return self.request(api_name=api_name, json=data, method="POST")

# 商品清单-查询组织用例
    def goods_treeList(self, data):
        api_name = f"enter/userCenter/extension/org/treeList"
        return self.request(api_name=api_name, data=data, )


#  商品清单用户组添加人员


    def goods_save_user(self, temporaryId, user_id):
        api_name = f"enter/userCenter/extension/newBizSelect/saveOrCance"
        data = {"bizType": "SPGL_3", "bizSubType": "SPGL_3_1", "bizId": "", "temporaryId": temporaryId,
                "optType": "ADD", "selectObj": {"objType": "USER", "objId": [user_id]}}
        return self.request(api_name=api_name, json=data, method="POST")
#  商品清单用户组添加人员

    def goods_save_usergroup(self, temporaryId, objType, usergorup_id):
        api_name = f"enter/userCenter/extension/newBizSelect/saveOrCancel"
        data = {"bizType": "SPGL_3", "bizSubType": "SPGL_3_1", "bizId": "", "temporaryId": temporaryId,
                "optType": "ADD", "selectObj": {"objType": objType, "objId": usergorup_id}}
        return self.request(api_name=api_name, json=data, method="POST")
# 商品清单-编辑用例

    def goods_modify(self, data):
        api_name = f"enter/goods/component//extension/goodsBiz/findBizCount"
        return self.request(api_name=api_name, headers=data, )

# 商品清单-新增用例
    def goods_add(self, listName, code):
        api_name = f"enter/goods/center/mgt/goodslist/add"
        data = {"listName": listName,
                "listDesc": "商品清单自动化测试1商品清单自动化测试1商品清单自动化测试1商品清单自动化测试1商品清单自动化测试1",
                "categoryId": "0",
                "categoryName": "默认分类",
                "coverUri": "https://supershoper.xxynet.com/vsvz1679996821231",
                "goodsBizCode": code,
                "userBizCode": "",
                "isAll": 1
                }
        return self.request(api_name=api_name, json=data, method="POST")

    """


    清单分类
    """
# 清单分类

    def goods_detailed_list(self, data):
        api_name = "enter/goods/center/mgt/category/add?"

        return self.request(api_name=api_name, json=data, method="POST")

# 清单的编辑
    def goods_edit_list(self, _ids, categoryName, createUserName):
        api_name = "enter/goods/center/mgt/category/modify"
        data = {"id": _ids,
                "categoryName": categoryName,
                "listNum": 0,
                "createUserName": createUserName,
                "createTime": "2023-03-23 18:28:5",
                "_index": 1,
                "_createTime": "2023-03-23 18:28"}
        return self.request(api_name=api_name, json=data, method="POST")

# 清单查询
    def goods_pagequery_list(self, data):
        api_name = "enter/goods/center/mgt/category/pageQuery"
        return self.request(api_name=api_name, json=data, method="POST")

    # 清单查询

    def goods_delte(self, ids):
        api_name = "enter/goods/center/mgt/goodslist/delete"
        data = {"id": ids}
        return self.request(api_name=api_name, json=data, method="POST")

    def goods_detailPageList(self, ids):
        api_name = "enter/userCenter/extension/newBizSelect/detailPageList"
        data = {"pageNum": 1, "pageSize": 12,
                "queryParameter": {"bizType": "SPGL_3", "bizSubType": "SPGL_3_1", "bizId": "", "temporaryId": "SPGL_30000000170", "isDisabledSelected": false, "objType": "USER"}}
        return self.request(api_name=api_name, json=data, method="POST")


class goods_group(base):
    def __init__(self, token, domain=True, safe=False, app_secret=None):
        super().__init__(token, domain, safe, app_secret)

    def goods_list_user(self, data):
        api_name = f"fab/goods/list"
        return self.request(api_name=api_name, data=data,)
    # 查询商品组

    def goods_list_role(self, data):
        api_name = f"product/group/query"
        return self.request(api_name=api_name, data=data)
