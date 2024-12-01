# -*- coding:utf-8 -*-
# @Time : 2024-11-24 15:40
# @Author : 沈东杨
# @Email : shendongyang844@gmail.com

# 封装公共代码
import time

import requests
from test_api.common.get_token import get_token
class user_add:
    def __init__(self):
        millis = int(round(time.time() * 1000))

        self.role_add = "http://localhost:5173/api/system/user"
        #随机生成编号
        self.random_id = f'http://localhost:5173/api/component/generate/code?type=1&_t={millis}'
        #加载部门信息
        self.apart_url = f'http://localhost:5173/api/selector/dept?_t={millis}'
        #加载角色信息
        self.role_url = f'http://localhost:5173/api/selector/role?pageIndex=1&pageSize=20&available=true&code=&name=&_t={millis}'
        self.headers={
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json;charset=UTF-8",
            "Origin": "http://localhost:5173",
            "Referer": "http://localhost:5173/",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
            # "Connection": "keep-alive"
        }
#获取各种部门信息等
    def get_value(self, username, password):
        self.get_to=get_token(username=username,password=password)
        self.token = self.get_to.json().get("data").get("token")
        # 添加 token 到 headers
        self.headers["x-auth-token"] = f"{self.token}"
        apartment=requests.get(url=self.apart_url,headers=self.headers).json()
        role=requests.get(url=self.role_url,headers=self.headers).json()
        random_id=requests.get(url=self.random_id,headers=self.headers).json()
        return  random_id # 返回响应对象
#添加
    def add_role(self,test_data):
        # 发送请求
        self.headers["x-auth-token"] = f"{self.token}"
        response = requests.post(url=self.role_add, headers=self.headers, json=test_data)
        return response
# if __name__ == '__main__':
#     a=user_add().add_role(username="1000@superadmin",password="123456")
#     print(a)
