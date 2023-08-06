
'''
@Author  :   顾一龙
@Time    :   2023/03/14 19:21:24
@Version :   1.0
@Contact :   世界那么大，你不想走走吗
'''
# Hard to write shit mountain.......


from .base import base


class article(base):

    def __init__(self, token, domain=True, safe=False, app_secret=None):
        super().__init__(token, domain, safe, app_secret)

    def getById(self, articleId):
        api_name = "contmgn/getArticleById"
        data = {}
        data["articleId"] = articleId
        return self.request(api_name)

    def addComment(self, articleId, content, stren=0):
        api_name = "contmgn/addComment"
        data = {}
        data["articleId"] = articleId
        data["content"] = content
        data["stren"] = stren
        return self.request(api_name=api_name, data=data)

    def getCommentListByArticleId(self, articleId,  page=1, row=20):
        api_name = "contmgn/getCommentListByArticleId"
        data = {}
        data["articleId"] = articleId
        data["page"] = page
        data["rows"] = row
        return self.request(api_name=api_name, data=data)

    def addPraiseNum(self, articleId):
        api_name = "contmgn/addPraiseNum"
        data = {}
        data["articleId"] = articleId
        return self.request(api_name=api_name, data=data)

    def addReplyPraise(self, targetId, articleId):
        api_name = "contmgn/addReplyPraise"
        data = {}
        data["favourToType"] = 3
        data["favourType"] = 2
        data["targetId"] = targetId
        data["targetParentId"] = articleId
        return self.request(api_name=api_name, data=data)

# 查找文章
    def list(self):
        api_name = "article/query"
        data = {
            "accessToken": self.token,
            "page": 1,
            "rows": 10,
            "title": "",
            "topNum": 9999,
            "homeTopFlag": 9999
        }
        return self.request(api_name=api_name, data=data)
# 根据文章的名字

    def list_name(self, title):
        api_name = "article/query"
        data = {
            "accessToken": self.token,
            "page": 1,
            "rows": 10,
            "title": title,
            "topNum": 9999,
            "homeTopFlag": 9999
        }
        return self.request(api_name=api_name, data=data)

    def delete(self, articleIds):
        api_name = "article/delete"
        data = {
            "accessToken": self.token,
            "articleIds": articleIds
        }

        return self.request(api_name=api_name, data=data)

    def comments(self, articleId, page, rows):
        api_name = "article/comments"
        data = {
            "accessToken": self.token,
            "articleId": articleId,
            "page": page,
            "rows": rows,
            "sortParam": 1,
            "selectParam": 1
        }
        return self.request(api_name=api_name, data=data)


# selectParam 2 是置顶评论

    def comments_list(self, articleId, rows):
        api_name = "article/comments"
        data = {
            "accessToken": self.token,
            "articleId": articleId,
            "rows": rows,
            "sortParam": 1,
            "timeParam:": 1,
            "selectParam": 2
        }
        return self.request(api_name=api_name, data=data)
# 删除评论
    def delete_comments(self, articleId, commentId):
        api_name = "article/comment/delete"
        data = {
            "accessToken": self.token,
            "articleId": articleId,
            "commentId": commentId,
        }
        return self.request(api_name=api_name, data=data)
