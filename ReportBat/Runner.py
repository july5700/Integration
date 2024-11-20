import pytest
import os
import subprocess
import sys

if __name__ == '__main__':
    # 1. 使用pytest生成测试报告时需要传递一个列表
    json_dir_path = 'allure\\result'
    args_list = ['-s', '-v', 'C:\\Users\\qdai4\\Desktop\\Integration\\CaseList', '--alluredir', json_dir_path]
    pytest.main(args_list)
    print("test finised")

    # 2. 使用allure命令生成测试报告 ：allure generate 数据路径文件 -o html路径文件 -c
    html_dir_path = 'allure\\result'
    allure_path = r'C:\Tools\allure-2.30.0\bin\allure.bat'  # Windows 下的 allure 命令

    cmd = '{} generate {} -o {} -c'.format(allure_path, json_dir_path, html_dir_path)
    print("going to generate html report")

    # 使用 subprocess.run 而不是 os.system，以捕获输出并处理错误
    try:
        result = subprocess.run(cmd, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("generate html report done")
        print("Allure command output:\n", result.stdout.decode('utf-8'))
    except subprocess.CalledProcessError as e:
        print("Error generating HTML report:\n", e.stderr.decode('utf-8'))