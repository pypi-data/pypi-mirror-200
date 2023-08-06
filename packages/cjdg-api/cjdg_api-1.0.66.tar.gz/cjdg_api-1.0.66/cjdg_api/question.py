import pytest
import requests
import requests
import json
# from loguru import logger

from cjdg_open_api.base import baseQuestion


class questionBank(baseQuestion):

    def __init__(self, token, domain=True, safe=False, app_secret=None):
        super().__init__(token, domain, safe, app_secret)
    # 题库-查询列表

    def list(self):
        api_name = 'shopguide_question/api/questionBank/page'
        data = {'name': '', 'state': ''}
        return self.request(api_name=api_name, data=data)

    # 题库-新增

    def save(self):
        api_name = 'shopguide_question/api/questionBank/save'
        headers = {'ContentType': 'application/json'}
        data = {'bankDesc': '', 'type': '', 'visibleRange': '', 'state': '',
                'complateCondition': '', 'contents': '', 'userGroupIds': ''}
        return self.request(api_name=api_name, json=data, headers=headers, method='post')

    # 题库-修改

    def edit(self):
        api_name = 'shopguide_question/api/questionBank/edit'
        headers = {'ContentType': 'application/json'}
        # data = {'accessToken': ''}
        return self.request(api_name=api_name, headers=headers, method='post')

    # 题库-发布
    def publish(self, id):
        api_name = 'shopguide_question/api/questionBank/publish'
        headers = {'ContentType': 'application/x-www-form-urlencoded'}
        data = {'id': id}
        return self.request(api_name=api_name, data=data, headers=headers, method='post')

    # 题库-失效

    def invalid(self, id):
        api_name = f'shopguide_question/api/questionBank/invalid/{id}'
        headers = {'ContentType': 'application/x-www-form-urlencoded'}
        # data = {'accessToken': ''}
        # id?
        return self.request(api_name=api_name, headers=headers, method='post')

    # 题库-删除

    def delete(self, id):
        api_name = f'shopguide_question/api/questionBank/del/{id}'
        headers = {'ContentType': 'application/x-www-form-urlencoded'}
        # data = {'accessToken': ''}
        # id?
        return self.request(api_name=api_name, headers=headers, method='post')

    # 题库-查询详情

    def detail(self, id):
        api_name = f'shopguide_question/api/questionBank/datail/{id}'
        # data = {'accessToken': ''}
        return self.request(api_name=api_name, method='get')

    # 答题-获取用户的答题状态

    def findContentAnswer(self, id):
        api_name = f'shopguide_question/api/questionBank/findContentAnswer/{id}'
        # data = {'accessToken': ''}
        return self.request(api_name=api_name, method='get')

    # 答题-获取答题批次号

    def gainBathNo(self):
        api_name = 'shopguide_question/api/answerBatch/gainBatchNo'
        data = {'questionBankId': ''}
        return self.request(api_name=api_name, data=data, method='get')

    # 答题-回答

    def ansert(self):
        api_name = 'shopguide_question/api/answerBatch/answer'
        headers = {'ContentType': 'application/json'}
        # data = {'accessToken': ''}
        return self.request(api_name=api_name, headers=headers, method='post')

    # 答题-结算

    def settle(self):
        api_name = 'shopguide_question/api/answerBatch/settle'
        headers = {'ContentType': 'application/x-www-form-urlencoded'}
        data = {'batchNo': ''}
        return self.request(api_name=api_name, data=data, headers=headers, method='post')


def main():
    token = 'd2ca889ecc08d70ca0a2abf376606f2b_csz_web'
    a = questionBank(token=token, domain=False)
    t = a.list()
    print(t)


if __name__ == '__main__':
    main()
