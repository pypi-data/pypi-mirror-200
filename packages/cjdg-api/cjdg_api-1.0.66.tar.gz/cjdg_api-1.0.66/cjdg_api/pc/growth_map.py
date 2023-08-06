
'''
@Author  :   顾一龙 
@Time    :   2023/03/14 20:22:57
@Version :   1.0
@Contact :   世界那么大，你不想走走吗
成长地图搜索用例
'''
# Hard to write shit mountain.......
from cjdg_api.base import baseApixxYent


class Growth_Map(baseApixxYent):
    def __init__(self, token, domain=True, app_secret=None):
        super().__init__(token, domain, app_secret)

    def growth_map_list(self, data):
        api_name = f"learn_path/api/learnPathGroup?"
        return self.request(api_name, params=data)

    #  返回的id 有问题，造成无法删除。
    # 删除成长路径测试用户,引用搜索用例返回的id

    def growth_map_dele(self, data):
        api_name = f"learn_path/api/learnPathGroup/delete"
        return self.request(api_name, json=data)
    # 新增成长地图

    def growth_map_add(self, data):
        api_name = f"learn_path/api/learnPathGroup/save?"
        return self.request(api_name, json=data)
