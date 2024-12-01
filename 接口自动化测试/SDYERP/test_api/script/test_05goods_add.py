# -*- coding:utf-8 -*-
# @Time : 2024-11-28  08:39
# @Author : 沈东杨
# @Email : shendongyang844@gmail.com
from random import randint

import allure
import pytest
from test_api.common.business.goods_add import goods
from test_api.common.readfile import readline
class Testadd:
    @allure.feature("商品新增功能")
    @allure.story("商品增成功测试")
    @pytest.fixture(autouse=True)  # 使用 fixture 自动调用
    def setup(self):
        # 初始化 LoginAPI 实例
        self.add_api = goods()

    @pytest.mark.parametrize('args', readline('/Users/yangayangdemac/pythonProject/SDYERP/test_api/data/goods_add.yml'))
    def test_add(self,args):
        data1=args.get("data",{})
        name=data1.get("name")
        categoryId=data1.get("categoryId")
        brandId=data1.get("brandId")
        weight=data1.get("weight")
        volume=data1.get("volume")
        taxRate=data1.get("taxRate")
        saleTaxRate=data1.get("saleTaxRate")
        purchasePrice=data1.get("purchasePrice")
        salePrice=data1.get("salePrice")
        retailPrice=data1.get("retailPrice")
        productType=data1.get("productType")
        user = data1.get("login_username")
        pwd = data1.get("login_password")
        # 随机编号，避免重复
        is_random_code=data1.get("is_random_code")
        # 随机sku，避免重复
        is_random_sku=data1.get("is_random_sku")
        #是否为低权限账户
        is_low=data1.get("is_low",False)
        #是否为正确数据
        is_true=data1.get("is_true",False)
        self.num = randint(0000, 9999999999)
        code = self.num if is_random_code else ""
        skuCode = self.num if is_random_sku else ""
        login_data = {
            "code": str(code),
            "name": name,
            "skuCode": str(skuCode),
            "categoryId": categoryId,
            "brandId": brandId,
            "weight": weight,
            "volume": volume,
            "taxRate": taxRate,
            "saleTaxRate": saleTaxRate,
            "purchasePrice": purchasePrice,
            "salePrice": salePrice,
            "retailPrice": retailPrice,
            "productType": productType
        }
        rev_add=self.add_api.add(username=user,password=pwd,test_data=login_data)
        r_j=rev_add.json()
        print(rev_add.json())
        self.msg = r_j.get("msg")
        self.code=r_j.get("code")
        # 断言
        if is_true:
            assert 200 == self.code
            assert "success" in self.msg
        elif  is_low :
            assert 403==self.code
            assert "无系统权限" in self.msg
        else:
            assert 400==self.code
            assert "请输入编号" in self.msg or "商品SKU编号不能为空" in self.msg or"传入参数有误" in self.msg or"重量最多允许2位小数" in self.msg or"体积最多允许2位小数" in self.msg or"进项税率（%）必须为整数"