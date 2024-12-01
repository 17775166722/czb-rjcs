# -*- coding:utf-8 -*-
# @Time : 2024-11-25 12:48
# @Author : 沈东杨
# @Email : shendongyang844@gmail.com

from random import randint
import allure
import pytest
from test_api.common.base_information.Stash_add import stash_ad
from test_api.common.readfile import readline
class Testadd:
    @allure.feature("仓库新增功能")
    @allure.story("仓库增成功测试")
    @pytest.fixture(autouse=True)  # 使用 fixture 自动调用
    def setup(self):
        # 初始化 LoginAPI 实例
        self.add_api = stash_ad()

    @pytest.mark.parametrize('args', readline('/Users/yangayangdemac/pythonProject/SDYERP/test_api/data/stash_add.yml'))
    def test_add(self,args):
        data1=args.get("data",{})
        user=data1.get("login_username")
        pwd=data1.get("login_password")
        contact=data1.get("contact")
        description=data1.get("description")
        address=data1.get("address")
        peopleNum=data1.get("peopleNum")
        telephone=data1.get("telephone")
        is_random_name=data1.get("is_random_name",False)
        is_random_code=data1.get("is_random_code",False)
        #随机编号，避免重复
        is_randon=data1.get("is_random",False)
        cityId=data1.get("cityId")
        self.num = randint(0000, 9999)
        if is_randon:
            code=self.num
            name="仓库"+ str(self.num)
        elif is_random_name:
            name = "仓库" + str(self.num)
            code = data1.get("code")
        elif is_random_code:
            code = self.num
            name = data1.get("name")
        else:
            name = data1.get("name")
            code = data1.get("code")
        login_data = {
            "code": code,
            "contact": contact,
            "description": description,
            "name": name,
            "address": address,
            "peopleNum":peopleNum,
            "telephone":telephone,
            "cityId":cityId
        }
        rev_add=self.add_api.add(username=user,password=pwd,test_data=login_data)
        print(rev_add.json())
        r_j=rev_add.json()
        # 断言
        if is_random_name or is_random_code:
            msg = rev_add.json().get("msg")
            assert 400 == r_j.get("code")
            assert "请输入编号" in msg or "请输入名称" in msg
        else:
            assert 200==rev_add.status_code