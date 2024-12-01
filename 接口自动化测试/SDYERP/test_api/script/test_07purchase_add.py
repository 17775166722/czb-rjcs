# -*- coding:utf-8 -*-
# @Time :  2024-11-28 18:52
# @Author : 沈东杨
# @Email : shendongyang844@gmail.com

import allure
import pytest
from test_api.common.business.purchase_add import purchase
from test_api.common.readfile import readline
class Testadd:
    @allure.feature("采购订单功能")
    @allure.story("采购订单测试")
    @pytest.fixture(autouse=True)  # 使用 fixture 自动调用
    def setup(self):
        # 初始化 LoginAPI 实例
        self.add_api = purchase()
    @pytest.mark.parametrize('args', readline('/Users/yangayangdemac/pythonProject/SDYERP/test_api/data/purchase_add.yml'))
    def test_add(self,args):
        data1=args.get("data",{})
        scId=data1.get("scId")
        supplierId=data1.get("supplierId")
        purchaserId=data1.get("purchaserId")
        expectArriveDate=data1.get("expectArriveDate")
        payTypes=data1.get("payTypes")
        products=data1.get("products")
        user = data1.get("login_username")
        pwd = data1.get("login_password")
        is_true = data1.get("is_true",False)
        is_low = data1.get("is_low",False)
        login_data = {
            "scId": scId,
            "supplierId": supplierId,
            "purchaserId": purchaserId,
            "expectArriveDate": expectArriveDate,
            "payTypes": payTypes,
            "products": products,
        }
        rev_add=self.add_api.add(username=user,password=pwd,test_data=login_data)
        print(rev_add.json())
        self.msg = rev_add.json().get("msg")
        self.code = rev_add.json().get("code")
        print(self.code)
        if is_true:
            print(is_true)
            assert 200 == self.code
            assert "success" in self.msg
        elif is_low:
            assert 403 == self.code
            assert "无系统权限" in self.msg
        else:
            assert 400 == self.code
            assert "仓库不存在" in self.msg or "供应商不存在" in self.msg or "采购员不存在" in self.msg or "第1行商品不存在" in self.msg or "传入参数有误" in self.msg