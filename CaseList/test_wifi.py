import pytest
import os, sys
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)
from PrivateLib.ADB import ADB
import re
import allure

@allure.epic('BXCN')
@allure.story('WIFI')
class TestWIFI(object):
    adb = ADB()

    @staticmethod
    def find_keyword(pattern, string):
        match = re.search(pattern, string)
        if match:
            return True
        else:
            return False

    @allure.title('查看WLAN驱动是否挂载')
    @allure.description('预期结果：wlan存在')
    def test_wlan_mounted(self):
        pattern = 'wlan'
        cmd = 'lsmod | grep wlan'
        output = self.adb.run_shell_command(cmd)
        result = self.find_keyword(pattern, output)
        assert result

    @allure.title('查看wifi是否打开')
    @allure.description('预期结果：wlan0存在')
    def test_wlan_enable(self):
        pattern = 'wlan0'
        cmd = [
        'svc wifi enable',
        'sleep 1',
        'ifconfig | grep wlan0'
        ]
        output = self.adb.run_multiple_shell_commands(cmd)
        result = self.find_keyword(pattern, output)
        print(f"result is {result}")
        assert result

    @allure.title('查看wifi是否关闭')
    @allure.description('预期结果：wlan0不存在')
    def test_wlan_disable(self):
        pattern = 'wlan0'
        cmd = [
        'svc wifi disable',
        'sleep 1',
        'ifconfig | grep wlan0'
        ]
        output = self.adb.run_multiple_shell_commands(cmd)
        result = self.find_keyword(pattern, output)
        print(f"result is {result}")
        assert not result