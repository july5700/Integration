import os
import subprocess
# from Config import IniConfig
from PrivateLib.ConfigCache import TomlConfig
import re
from loguru import logger
import datetime
import time


class Artifactory(object):

    def __init__(self):
        self.toml_path = 'cfg.toml'
        self.cfg = TomlConfig(self.toml_path)
        self.web = self.cfg.get('common.web')
        self.api = self.cfg.get('common.api')
        self.directory = self.cfg.get('common.directory')
        self.https_proxy = self.cfg.get('common.https_proxy')
        self.http_proxy = self.cfg.get('common.http_proxy')
        self.cp_current_version = ''


        self.head = {f'X-JFrog-Art-Api':self.api}
        self.release = r'artifactory/zeekr/8295_ZEEKR/daily_8155/BXCN_OS5.2/Release/'
        self.version = ''
        self.full_url = ''
        self.target_zip_path = ''
        self.is_proxies = self.get_is_proxies_value()
        logger.info(f"in init self.is_proxies = {self.is_proxies}")

        # 'curl -H "X-JFrog-Art-Api:AKCpBtMeL1yqE2pk4dRTfFHeb6cqhwCxVYun9bJ8yoR8WbxnFeL7iGvFm1AS2rhf7TRZRCNZb" “https://hw-snc-jfrog-dmz.zeekrlife.com/artifactory/zeekr/8295_ZEEKR/daily_8155/BX1E_CA/Release/”
    def get_is_proxies_value(self):
        _ = self.cfg.read('parameter.is_proxies')
        logger.info(f"value of parameter.is_proxies = {_}")
        if str(_) in ['True', "1", 'true']:

            return True
        else:
            return False


    def print_cfg(self):
        logger.info(f"self.cfg = {self.cfg}")
        logger.info(f"self.web = {self.web}")
        logger.info(f"self.api = {self.api}")
        logger.info(f"self.directory = {self.directory}")
        logger.info(f"self.https_proxy = {self.https_proxy}")
        logger.info(f"self.is_proxies = {self.is_proxies} type of is_proxies is {type(self.is_proxies)}")

    def check_artifactory_directory(self):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    # def set_proxies(self):
    #     logger.info(f"value of self.is_proxies  = {self.is_proxies}")
    #     if self.is_proxies:
    #
    #         os.environ['https_proxy'] = self.https_proxy
    #         os.environ['http_proxy'] = self.http_proxy
    #         logger.info(f"current environment variables:\n{os.environ}")
    #     else:
    #         pass
            # os.environ['no_proxy'] = self.web
            # print(os.environ['no_proxy'])

    def set_proxies(self):
        if self.is_proxies:
            os.environ['https_proxy'] = self.https_proxy
            os.environ['http_proxy'] = self.http_proxy
            logger.info(f"current environment variables:\n{os.environ}")
        else:
            logger.info("Proxies are not enabled")

    @staticmethod
    def del_proxies():
        if 'https_proxy' in os.environ:
            del os.environ['https_proxy']
        if 'http_proxy' in os.environ:
            del os.environ['http_proxy']
        # if 'no_proxy' in os.environ:
        #     del os.environ['no_proxy']

    def joint_cmd(self):
        cmd = ['curl', '-L', self.full_url]
        for key, value in self.head.items():
            cmd.extend(['-H', str(f"{key}:{value}")])
        if not self.is_proxies:
            cmd.extend(['--noproxy', self.web])

        cmd.extend(['-o', str(self.target_zip_path)])
        return cmd

    def compare_version(self):
        try:
            self.set_proxies()
            logger.info(f"current environment = \n{os.environ}\n")
            cmd = [
                'curl', self.web + self.release,
            ]
            for key, value in self.head.items():
                cmd.extend(['-H', f"{key}:{value}"])
            # cmd.extend(['-H', "X-JFrog-Art-Api: AKCpBtMeL1yqE2pk4dRTfFHeb6cqhwCxVYun9bJ8yoR8WbxnFeL7iGvFm1AS2rhf7TRZRCNZb"])
            logger.info(f"Will execute cmd :{' '.join(cmd)}")
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            logger.info(result.stdout)
            cp = r'<a[^>]*>V(\d.\d.\d.\d\d)/</a>'
            version_list = re.findall(cp, result.stdout)
            history_versions = self.get_history_versions()
            logger.info(f"history versions = {history_versions}, version_list = {version_list}")
            # version_list.append(current_version)
            last_version = max(version_list, key=self.parse_version)
            logger.info(f"last_version = {last_version}")
            if last_version in history_versions:
                self.del_proxies()
                logger.critical(f"latest version:{last_version} is in history versions, no need to download")
                return False
            else:
                self.cp_current_version = last_version
                self.cfg.set('current_version.version', last_version)
                return last_version


        except Exception as e:
            logger.exception(e)
            raise
        finally:
            self.del_proxies()

    def get_history_versions(self):
        history_versions = []
        for version in self.cfg.get('versions'):
            history_versions.append(version.get('version'))
        return history_versions

    def prepare_download_path(self):
        """
        从URL中提取所需的路径部分，确保目录存在，并返回完整的文件路径。

        :return: 完整的文件路径。
        """
        # 解析URL以提取路径部分
        start_index = self.full_url.find("BXCN_OS5.2")
        if start_index == -1:
            raise ValueError("URL中没有找到BXCN_OS5.2路径部分")

        # 提取从"BXCN_OS5.2"开始的路径部分
        base_path = self.full_url[start_index:]

        # 分离目录路径和文件名
        target_dir = os.path.dirname(base_path)
        file_name = os.path.basename(base_path)

        # 确保目标目录存在
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        # 构造完整的目标路径
        self.target_zip_path += os.path.join(target_dir, file_name)

    @staticmethod
    def parse_version(version):
        return list(map(int, version.split('.')))

    def refresh_version_url(self):
        self.version = self.cfg.read('current_version.version')
        self.full_url = self.web + self.release + f'V{self.version}/b_Package_USB.zip'

    def add_history_entry(self):
        new_version_info = {
            'version': '',
            'date': '',
            'link': '',
            'path': ''
        }

        # 获取当前日期和时间
        current_datetime = datetime.datetime.now().strftime('%Y.%m.%d_%H:%M')
        new_version_info['version'] = self.cp_current_version
        new_version_info['date'] = current_datetime
        new_version_info['link'] = self.full_url
        new_version_info['path'] = self.target_zip_path

        self.cfg.add_version(new_version_info)
        self.cfg.set('current_version.version', self.cp_current_version)
        self.cfg.set('current_version.path', self.target_zip_path)

        # 新增三行内容
        # new_entry = f'\n{current_datetime} = {self.version}\nversion = {self.full_url}\n\n'
        #
        # # 读取现有的配置文件
        # with open(self.ini_path, 'r') as file:
        #     lines = file.readlines()
        #
        # # 找到 [history] 部分的起始位置
        # history_start_index = None
        # for i, line in enumerate(lines):
        #     if line.strip() == '[history]':
        #         history_start_index = i
        #         break
        #
        # if history_start_index is not None:
        #     # 在 [history] 部分的下一行插入新的条目
        #     lines.insert(history_start_index + 1, new_entry)
        # else:
        #     # 如果 [history] 部分不存在，创建它并插入新的条目
        #     lines.append('[history]\n')
        #     lines.append(new_entry)
        #
        # # 写回文件
        # with open(self.ini_path, 'w') as file:
        #     file.writelines(lines)

    def download_via_curl(self):
        download_result = False
        try:
            self.set_proxies()
            self.refresh_version_url()
            self.prepare_download_path()
            cmd = self.joint_cmd()
            logger.info(f"Will execute cmd :{' '.join(cmd)}")
            logger.critical("Start to download")

            subprocess.run(cmd, check=True)
            local_full_zip_path = os.path.join(os.getcwd(), self.target_zip_path)
            logger.critical(f"File downloaded successfully: {self.target_zip_path}")
            self.target_zip_path = local_full_zip_path
            # self.cfg.update_cfg('version', 'path', local_full_zip_path)
            time.sleep(1)
            self.add_history_entry()
            download_result = True

        except Exception as e:
            logger.exception(f"An error occurred:\n")
            # self.cfg.update_cfg('version', 'last_download_version', 'fail_to_download')
            # self.cfg.update_cfg('version', 'current_version', self.cp_current_version)
            download_result = False
            raise
        finally:
            self.del_proxies()
            return download_result

    def main(self):
        need_update = self.compare_version()
        if need_update:
            logger.critical(f"Start to download via curl")
            self.download_via_curl()
        else:
            logger.critical("no need to download")


if __name__ == '__main__':
    art = Artifactory()
    art.main()


