# -*- coding:utf-8 -*-
# @Time : 2024-11-25 10:48
# @Author : 沈东杨
# @Email : shendongyang844@gmail.com

import os
import pytest

def generate_allure_report():
    # 设置工作目录为项目根目录
    os.chdir("/Users/yangayangdemac/pythonProject/SDYERP")

    # 定义结果目录
    allure_results_dir = os.path.abspath("test_api/allure_results")
    report_dir = os.path.abspath("test_api/report")

    # 运行 pytest 并生成 allure 原始数据
    pytest.main(["-v", "-s", f"--alluredir={allure_results_dir}"])

    # 使用 Allure 生成 HTML 报告
    result = os.system(f"allure generate {allure_results_dir} -o {report_dir} --clean")
    if result == 0:
        print(f"Allure 报告已生成，存放路径为：{report_dir}")
        os.system(f"allure open {report_dir}")
    else:
        print("生成 Allure 报告失败，请检查 Allure 命令是否正确。")

if __name__ == "__main__":
    generate_allure_report()