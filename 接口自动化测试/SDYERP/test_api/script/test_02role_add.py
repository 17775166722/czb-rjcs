# -*- coding:utf-8 -*-
# @Time : 2024-11-24 14:48
# @Author : 沈东杨
# @Email : shendongyang844@gmail.com

from random import randint

import allure
import pytest
from test_api.common.system.role_add import role_add
from test_api.common.readfile import readline
class Testadd:
    @allure.feature("角色新增功能")
    @allure.story("角色新增成功测试")
    @pytest.fixture(autouse=True)  # 使用 fixture 自动调用
    def setup(self):
        # 初始化 LoginAPI 实例
        self.add_api = role_add()

    @pytest.mark.parametrize('args', readline('/Users/yangayangdemac/pythonProject/SDYERP/test_api/data/role_add.yml'))
    def test_add(self,args):
        data1=args.get("data",{})
        user=data1.get("login_username")
        pwd=data1.get("login_password")
        permission=data1.get("permission")
        description=data1.get("description")
        #随机编号，避免重复
        is_randon=data1.get("is_random")
        if is_randon:
            num=randint(0000, 9999)
            code=num
            name="员工"+ str(num)
        else:
            name = data1.get("name")
            code = data1.get("code")

        shortName=data1.get("shortName")
        login_data = {
            "code": code,
            "permission": permission,
            "description": description,
            "name": name,
            "shortName": shortName
        }
        rev_add=self.add_api.add(username=user,password=pwd,test_data=login_data)
        print(rev_add.json())
#         # 断言
        if data1.get("is_true"):
            assert 200 == rev_add.status_code
        else:
            code = rev_add.json().get("code")
            msg = rev_add.json().get("msg")
            assert code != 200  # 确保错误码不是 200
            assert msg is not None
            # 可以添加更多的特定错误码检查
            if code == 400:
                assert "请输入名称" in msg or "编号必须由字母、数字、“-_.”组成，长度不能超过20位" in msg or "请输入编号" in msg
            if code ==403:
                assert "无系统权限" in msg