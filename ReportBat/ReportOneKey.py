import pytest
import os
import subprocess
import sys

if __name__ == '__main__':
    # 1. 使用pytest生成测试报告时需要传递一个列表
    json_dir_path = 'testoutput'
    args_list = ['-s', '-v', 'C:\\Users\\qdai4\\Desktop\\Integration\\CaseList', '--alluredir', json_dir_path]
    pytest.main(args_list)
    print("test finised")

    # 2. 使用allure命令生成测试报告
    html_dir_path = 'allure-report'
    allure_path = r'C:\Tools\allure-2.30.0\bin\allure.bat'  # Windows 下的 allure 命令

    # 生成报告
    cmd_generate = '{} generate {} -o {}'.format(allure_path, json_dir_path, html_dir_path)
    print("going to generate html report")
    try:
        result_generate = subprocess.run(cmd_generate, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("generate html report done")
        print("Allure generate command output:\n", result_generate.stdout.decode('utf-8'))
    except subprocess.CalledProcessError as e:
        print("Error generating HTML report:\n", e.stderr.decode('utf-8'))

    # 打开报告
    cmd_open = '{} open {}'.format(allure_path, html_dir_path)
    print("going to open html report")
    try:
        result_open = subprocess.run(cmd_open, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("open html report done")
        print("Allure open command output:\n", result_open.stdout.decode('utf-8'))
    except subprocess.CalledProcessError as e:
        print("Error opening HTML report:\n", e.stderr.decode('utf-8'))