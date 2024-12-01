# -*- coding:utf-8 -*-
# @Time : 2024-11-23 21:30
# @Author : 沈东杨
# @Email : shendongyang844@gmail.com

from test_api.common.login import LoginAPI

def get_token(username, password):
    """
    获取 token。
    如果获取失败，返回 None 并记录警告信息。
    """
    try:
        token = LoginAPI().get_token(username, password)
        if not token:
            print(f"警告: 登录失败，未能获取到有效的 token，用户名: {username}, 密码: {password}")
            return None  # 返回 None 以便调用方处理
        return token
    except Exception as e:
        print(f"错误: 获取 token 时发生异常: {e}")
        return None  # 返回 None 避免程序崩溃