# -*- coding:utf-8 -*-
# @Time : 2024-11-23 16:30
# @Author : 沈东杨
# @Email : shendongyang844@gmail.com

# 封装公共代码
import time

import requests
from test_api.common.Verification_code import code_function

class LoginAPI:
    def __init__(self):
        self.login_url = "http://localhost:5173/api/auth/login"
        self.require="http://localhost:5173/api/auth/captcha/require"
        self.headers={
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Origin": "http://localhost:5173",
            "Referer": "http://localhost:5173/",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        }
    def get_code(self,username):
        """
        获取验证码和 SN (验证码的唯一标识)
        :return: (验证码, SN)
        """
        try:
            requests.post(url=self.require, data={'username': username})
            # 获取验证码

            # 获取 SN
            code,sn = code_function()
            # 从响应中提取数据
            if not sn:
                raise ValueError("验证码 SN 获取失败")
            return code, sn

        except requests.exceptions.RequestException as e:
            print(f"请求失败: {e}")
            return None, None
        except ValueError as ve:
            print(f"数据处理失败: {ve}")
            return None, None

    def get_token(self, username1, password, max_retries=3):
        for attempt in range(max_retries):
            code, sn = self.get_code(username=username1)  # 获取验证码和 SN
            login_data = {
                "username": username1,
                "password": password,
                "sn": sn,
                "captcha": code
            }
            print(f"尝试第 {attempt + 1} 次登录，验证码: {code}, SN: {sn}")
            # 调用 login 方法发送请求
            res_l = self.login(test_data=login_data)
            print(res_l)
            if not res_l:  # 如果请求失败
                print("登录接口请求失败，请检查网络或接口配置！")
                continue

            try:
                res_j = res_l.json()
            except Exception as e:
                print(f"解析 JSON 时出错: {e}，响应内容: {res_l.text}")
                continue

            # 检查是否包含 token
            data = res_j.get("data")
            if data and "token" in data:
                print("成功登录！")
                return res_l
            else:
                print(f"登录失败，接口返回: {res_j}")
            time.sleep(2)
        raise ValueError(f"在尝试 {max_retries} 次后未能获取到 token，请检查验证码识别或登录流程！")
    def login(self,test_data):
        return requests.post(url=self.login_url,headers=self.headers,data=test_data)


# 在 login.py 中的调用方式
if __name__ == '__main__':
    # 创建 LoginAPI 类的实例
    token = LoginAPI().get_token(username="1000@superadmin", password="123456")
    print(token)
    # print(LoginAPI().get_code())
