# -*- coding:utf-8 -*-
# @Time :  2024-11-28 18:49
# @Author : 沈东杨
# @Email : shendongyang844@gmail.com

import time

# 封装公共代码
import requests
from test_api.common.get_token import get_token
class purchase:
    def __init__(self):
        millis = int(round(time.time() * 1000))
        self.goods_add = "http://localhost:5173/api/purchase/order/approve/pass/direct"
        self.headers={
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json;charset=UTF-8",
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
        response = requests.post(url=self.goods_add, headers=self.headers, json=test_data)
        return response  # 返回响应对象
