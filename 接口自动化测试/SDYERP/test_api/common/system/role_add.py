# -*- coding:utf-8 -*-
# @Time : 2024-11-24 14:48
# @Author : 沈东杨
# @Email : shendongyang844@gmail.com

# 封装公共代码
import requests
from test_api.common.get_token import get_token
class role_add:
    def __init__(self):
        self.role_add = "http://localhost:5173/api/system/role"
        self.headers={
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Origin": "http://localhost:5173",
            "Referer": "http://localhost:5173/",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        }

    def add(self, username, password,test_data):
        self.get_to = get_token(username=username, password=password)
        token = self.get_to.json().get("data").get("token")
        # 添加 token 到 headers
        self.headers["x-auth-token"] = f"{token}"
        # 发送请求
        response = requests.post(url=self.role_add, headers=self.headers, data=test_data)
        return response  # 返回响应对象
if __name__ == '__main__':
    role_add().add(username="1000@superadmin",password="123456")
