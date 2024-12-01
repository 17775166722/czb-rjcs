# -*- coding:utf-8 -*-
# @Time : 2024-11-23 12:10
# @Author : 沈东杨
# @Email : shendongyang844@gmail.com

import base64
import requests
import os
import ddddocr
import sys
import time

def code_function():
    # 创建文件夹
    os.makedirs('../script/code/', exist_ok=True)
    millis = int(round(time.time() * 1000))
    # 请求验证码
    url = f'http://localhost:5173/api/auth/captcha?_t={millis}'
    try:
        response = requests.get(url)
        sn = response.json().get("data").get("sn")
        response.raise_for_status()  # 如果返回状态码不是2xx，抛出异常
        base64_img = response.json().get("data", {}).get("image")
        if not base64_img:
            raise ValueError("未能从接口获取 Base64 图片数据")
    except Exception as e:
        print(f"获取验证码失败: {e}")
        exit()

    # 解码 Base64 图片
    try:
        base64_data = base64_img.split(",")[1]  # 去掉前缀
        img_data = base64.b64decode(base64_data)
        img_path = '../script/code/3.png'  # 修正保存路径
        with open(img_path, 'wb') as f:
            f.write(img_data)
    except Exception as e:
        print(f"图片解码失败: {e}")
        exit()

    # 使用 ddddocr 识别验证码
    try:
        # 重定向标准输出以禁用 ddddocr 输出的欢迎信息
        sys.stdout = open(os.devnull, 'w')  # 忽略 ddddocr 输出

        ocr = ddddocr.DdddOcr()
        with open(img_path, 'rb') as f:
            img_byte = f.read()
            res = ocr.classification(img_byte)

        # 恢复标准输出
        sys.stdout = sys.__stdout__

        # 只打印一次识别结果
        return res, sn
    except Exception as e:
        # 恢复标准输出并处理错误
        sys.stdout = sys.__stdout__
        print(f"验证码识别失败: {e}")
        exit()

# 调用函数进行测试
if __name__ == '__main__':
    code, sn = code_function()
    print(f"识别结果: {code}, SN: {sn}")