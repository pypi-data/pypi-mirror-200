'''
@Author  :   顾一龙 
@Time    :   2022/12/14 22:37:13
@Version :   1.0
@Contact :   世界那么大，你不想走走吗
'''
# Hard to write shit mountain.......
#  检核任务
from cjdg_open_api.base import baseApixxYent


class reviewTask(baseApixxYent):
    def __init__(self, token, domain=True, safe=False, app_secret=None):
        super().__init__(token, domain, safe, app_secret)

    def list(self):
        api_name = f"enter/superguide/inspection/task/list"
        data = {"pageNum": 1, "pageSize": 10,
                "queryParameter": {"type": "single"}}
        return self.request(api_name, json=data, method="POST")

    # 根据name查询任务
    def list_name(self, name):
        api_name = f"enter/superguide/inspection/task/list"
        data = {"pageNum": 1, "pageSize": 10, "queryParameter": {"name": name}}
        return self.request(api_name, json=data, method="POST")
#  失效任务

    def inspection(self, id):
        api_name = "enter/superguide/inspection/task/invalid"
        data = {"data": id}
        return self.request(api_name, json=data, method="POST")

# 删除任务
    def delete(self, id):
        api_name = "enter/superguide/inspection/task/delete"
        data = {"data": [id]}
        return self.request(api_name, json=data, method="POST")


# 查看任务01

    def info(self, id, token):
        api_name = "enter/superguide/inspection/task/data/info"
        data = {"taskId": id, "accessToken": token}
        return self.request(api_name, params=data, method="GET")
# 查看任务02

    def findBizCount(self, id):
        api_name = "enter/userCenter/extension/openBizSelect/findBizCount"
        data = {"bizType": "INSPECTION", "bizId": id,
                "bizSubType": "INSPECTED_USER", "temporaryId": ""}
        return self.request(api_name, json=data, method="POST")

# 数据查看
    def findBizCount(self, taskId):
        api_name = "enter/superguide/inspection/feedback/details"
        data = {"pageNum": 1, "pageSize": 10,
                "queryParameter": {"taskId": taskId}}
        return self.request(api_name, json=data, method="POST")


# 检核任务新增好麻烦啊。


    def add(self, taskId):
        api_name = "enter/superguide/inspection/feedback/details"
        data = {"pageNum": 1, "pageSize": 10,
                "queryParameter": {"taskId": taskId}}
        return self.request(api_name, json=data, method="POST")
