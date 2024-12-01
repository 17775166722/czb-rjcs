# -*- coding:utf-8 -*-
# @Time : 2024-11-24 15:48
# @Author : 沈东杨
# @Email : shendongyang844@gmail.com

import subprocess
import time

import allure
import pytest
from test_api.common.login import LoginAPI
from test_api.common.readfile import readline
class TestLogin:
    @allure.feature("登录功能")
    @allure.story("登录成功测试")
    def test_login_success(self):
        allure.attach("描述", "测试用例描述", allure.attachment_type.TEXT)
    @pytest.fixture(autouse=True)  # 使用 fixture 自动调用
    def setup(self):
        # 初始化 LoginAPI 实例
        self.login_api = LoginAPI()

    @pytest.mark.parametrize('args', readline('/Users/yangayangdemac/pythonProject/SDYERP/test_api/data/login.yml'))
    def test_login(self,args):
        data1=args.get("data",{})
        username=data1.get("login_username")
        password = data1.get("login_password")
        # 根据 need_captcha 的值判断是否需要固定的验证码和 SN
        if args.get('data').get('need_captcha'):
            # 尝试获取验证码和 SN，最多尝试三次
            for attempt in range(3):
                code, sn = None, None  # 初始化验证码和 SN 为 None
                for attempt in range(3):
                    # 获取验证码和 SN
                    code, sn = self.login_api.get_code(username=username)
                    if code and sn:  # 如果验证码和 SN 获取成功，跳出循环
                        break
                    else:
                        print(f"验证码获取失败，尝试第 {attempt + 1} 次...")
                        time.sleep(2)  # 加个延迟，避免频繁请求导致被封

                # 如果三次尝试都失败，抛出异常
                if not code or not sn:
                    raise ValueError("获取验证码失败，请检查验证码识别服务！")
        else:
            code, sn = "dummy_code", "dummy_sn"  # 使用固定的验证码和 SN

        login_data = {
            "username": username,
            "password": password,
            "sn": sn,
            "captcha": code
        }
        res_l = self.login_api.login(test_data=login_data)
        print("sn",sn,"code",code)
        print(res_l.json())
        # 断言
        if data1.get("nature"):
            assert 'token' in res_l.json().get("data")
            assert 200 == res_l.status_code
        else:
            code = res_l.json().get("code")
            msg = res_l.json().get("msg")
            assert code != 200  # 确保错误码不是 200
            assert msg is not None
            # 可以添加更多的特定错误码检查
            if code == 500:
                assert "验证码错误" in msg or "验证码已过期" in msg
            if code == 419:
                assert "错误" in msg or "登录失败" in msg
            if code ==400:
                assert "用户名不能为空" in msg or "密码不能为空" in msg
# if __name__ == '__main__':
#     pytest.main(["-sq", "script/test_01login.py", "--alluredir=./report/json"])
#     subprocess.run(
#         ["allure", "generate", "./report/json", "-o", "./report/html", "--clean"],
#         check=True
#     )
#     print("测试报告已生成：report-result")