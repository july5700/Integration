from BX_Artifactory import Artifactory
from PrivateLib.ConfigCache import TomlConfig
from Unzip import unzip_file_with_progress
import os
from USBSwitch import USBSwitch
from Copy import copy_large_file_to_UDisk
from PrivateLib import Serial
from MyLog import MyLog
import sys

# ToDo
# Test

if __name__ == '__main__':
    _ = MyLog(3)
    logger = _.create_log_sample()

    toml_cache = TomlConfig('cfg.toml')
    # logger.info(ini_cache.read_cfg('common', 'api'))
    art = Artifactory()
    art.main()
    src_zip = toml_cache.read('current_version.version')
    tar_path = src_zip + 'unzip'
    # 解压缩
    unzip_result = unzip_file_with_progress(src_zip, tar_path)
    unzip_file = os.path.join(tar_path, 'b_Package_USB\\UpdatePackage')
    if os.path.exists(unzip_file):
        logger.info(f"zip file exist:{unzip_file}")

    else:
        logger.info("No zip file")
        sys.exit()

    if unzip_result:
        # 切U盘到PC
        usb_switch = USBSwitch()
        usb_switch.init_usb_switch()
        usb_switch.switch_to_pc()
        # copy_result = 1
        # time.sleep(3)

        # 复制到U盘
        copy_result = copy_large_file_to_UDisk(unzip_file)
        if copy_result:
            logger.info("copy to u PASS")
            # usb_switch.init_usb_switch()
            usb_switch.switch_to_ecu()


        #
        port = toml_cache.read('common.qnx_port')
        s = Serial.Serial(port)
        s.open()
        s.upgrade()
        logger.critical("Start to upgrade, please wait 20~30 minutes...")
    else:
        logger.critical("Fail to Download, test stopped!!!")
        sys.exit()







# See PyCharm help at https://www.jetbrains.com/help/pycharm/
