# -*- coding:utf-8 -*-
# @Time : 2024-11-25 10:48
# @Author : 沈东杨
# @Email : shendongyang844@gmail.com

from random import randint
import allure
import pytest
from test_api.common.system.user_add import user_add
from test_api.common.readfile import readline
class Testadd:
    @allure.feature("用户新增功能")
    @allure.story("用户新增成功测试")
    @pytest.fixture(autouse=True)  # 使用 fixture 自动调用
    def setup(self):
        # 初始化 LoginAPI 实例
        self.add_api = user_add()

    @pytest.mark.parametrize('args', readline('/Users/yangayangdemac/pythonProject/SDYERP/test_api/data/user_add.yml'))
    def test_add(self,args):
        #获取参数
        data1=args.get("data",{})
        user = data1.get("login_username")
        pwd = data1.get("login_password")
        deptIds=data1.get("deptIds")
        description=data1.get("description")
        name=data1.get("name")
        email=data1.get("email")
        gender=data1.get("gender")
        password=data1.get("password")
        roleIds=data1.get("roleIds")
        telephone=data1.get("telephone")
        not_username=data1.get("not_username","")
        if not_username:
            username = data1.get("username")
        else:
            num=randint(0000, 9999)
            username ="test"+str(num)
        if data1.get("not_code"):
            code=data1.get("code")
        else:
            #获取随机生成的编码
            code=self.add_api.get_value(username=user,password=pwd).get("data")
        login_data = {
            "code": code,
            "deptIds": deptIds,
            "description": description,
            "name": name,
            "email": email,
            "gender": gender,
            "password": password,
            "roleIds": roleIds,
            "telephone": telephone,
            "username": username
        }

        rev_add=self.add_api.add_role(test_data=login_data)
        # #打印响应内容
        print(rev_add.json())
        # 断言
        if data1.get("is_true"):
            assert 'success' in rev_add.json().get("msg")
            assert 200 == rev_add.status_code
        else:
            code = rev_add.json().get("code")
            msg = rev_add.json().get("msg")
            assert code != 200  # 确保错误码不是 200
            assert msg is not None
            # 可以添加更多的特定错误码检查
            if code == 400:
                assert "请输入密码" in msg or "密码长度必须为5-16位，只允许包含大写字母、小写字母、数字、下划线" in msg or "请选择性别" in msg or "联系电话格式不正确" in msg or "请输入用户名" in msg or "请输入姓名" in msg
            elif code ==500:
                assert "用户名重复，请重新输入" in msg
