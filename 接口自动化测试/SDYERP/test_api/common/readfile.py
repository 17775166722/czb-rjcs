# -*- coding:utf-8 -*-
# @Time : 2024-11-23 15:20
# @Author : 沈东杨
# @Email : shendongyang844@gmail.com

import yaml

def readline(path):
    # 读取并解析 YAML 文件
    with open(path, 'r', encoding='utf-8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    return data