import pytest
import os, sys
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)
from PrivateLib.ADB import ADB
import re
import allure

@allure.epic('BXCN')
@allure.story('BT')
class TestBT(object):
    adb = ADB()

    @staticmethod
    def find_keyword(pattern, string):
        match = re.search(pattern, string)
        if match:
            return True
        else:
            return False

    @allure.title('查看BT是打开')
    @allure.description('预期结果：settings get global bluetooth_on输出1')
    def test_bt_enabled(self):
        result = '1'
        cmds = [
            'su root\n',
            'sleep 3\n',
            'svc bluetooth enable\n',
            'sleep 3\n',
            'settings get global bluetooth_on\n',
               ]
        output = self.adb.execute_adb_commands_as_root(cmds)
        # result_1 = self.find_keyword(pattern_1, output)
        assert result in output

    @allure.title('查看BT是否关闭')
    @allure.description('预期结果：settings get global bluetooth_on输出0')
    def test_bt_disabled(self):
        result_1 = 'killed'
        result_2 = '0'
        cmds = [
            'su root\n',
            'sleep 3\n',
            'svc bluetooth disable\n',
            'sleep 3\n',
            'settings get global bluetooth_on\n',
        ]
        output = self.adb.execute_adb_commands_as_root(cmds)
        # result_1 = self.find_keyword(pattern_1, output)
        # result_2 = self.find_keyword(pattern_2, output)
        assert result_1 not in output
        assert result_2 in output
