import os
from loguru import logger
import subprocess
import time
import threading


# 加入sleep 5 可以避免输出缓存的混乱
class ADB(object):
    output_list = []
    @staticmethod
    def run_adb_command(command):
        """
        发单挑指令
        :param command:
        :return:
        """
        output = ''
        # 构造完整的ADB命令
        full_command = f'{command}'
        logger.info(f"Will send command:{full_command}")

        try:
            # 执行命令并获取输出
            result = subprocess.run(full_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            # 打印命令输出
            output = result.stdout.decode('utf-8')
            logger.info(f'Output:\n{output}')

        except subprocess.CalledProcessError as e:
            # 如果命令执行失败，打印错误信息
            logger.exception(f"Error: {e.stderr.decode('utf-8')}")
            output = e.stderr.decode('utf-8')
        finally:
            return output

    @staticmethod
    def run_shell_command(command):
        """
        发送一条adb shell下的指令
        :param command:
        :return:
        """
        output = ''
        # 构造完整的ADB命令，先进入shell再执行命令
        full_command = f'adb shell "{command}"'
        logger.info(f"Will send command:{full_command}")
        try:
            # 执行命令并获取输出
            result = subprocess.run(full_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            # 打印命令输出
            output = result.stdout.decode('utf-8')
            logger.info(f'Output:\n{output}')
        except subprocess.CalledProcessError as e:
            # 如果命令执行失败，打印错误信息
            logger.exception(f"Error: {e.stderr.decode('utf-8')}")
            output = e.stderr.decode('utf-8')
        finally:
            return output
    # 示例：获取设备列表

    @staticmethod
    def run_multiple_shell_commands(commands):
        """
        在adb shell下发送多条或者1条指令
        :param commands:
        :return:
        """
        output = ''
        # 将多个命令用 && 连接起来，确保前一个命令成功后才执行下一个命令
        # 如果不需要这种顺序依赖，可以用 ; 连接
        combined_command = ' && '.join(commands)

        # 构造完整的ADB命令，先进入shell再执行命令
        full_command = f'adb shell "{combined_command}"'
        logger.info(f"Will send command:{full_command}")
        try:
            # 执行命令并获取输出
            result = subprocess.run(full_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    shell=True)
            print(f"result = {result}, type of result is {type(result)}")
            # 打印命令输出
            output = result.stdout.decode('utf-8')
            logger.info(f'Output:\n{output}')
        except subprocess.CalledProcessError as e:
            # 如果命令执行失败，打印错误信息
            print(f"Error: {e.stderr.decode('utf-8')}")
            output = e.stderr.decode('utf-8')
            logger.info(f"Output:\n{output}")
        finally:
            time.sleep(3)
            return output

    # 示例：启用WiFi并输出网络配置

    @staticmethod
    def add_path_to_environ():
        path_to_add = r'F:\BackUp\exe\Tools\platform-tools'

        # 获取当前的 PATH 环境变量
        current_path = os.environ.get('PATH', '')

        # 如果当前路径中没有包含要添加的路径，则将其添加
        if path_to_add not in current_path:
            # 分隔符通常是分号 (;) 在 Windows 上，冒号 (:) 在 Unix-like 系统上
            if os.name == 'nt':  # Windows
                path_separator = ';'
            else:  # Unix-like
                path_separator = ':'

            # 添加新路径
            new_path = current_path + path_separator + path_to_add
            os.environ['PATH'] = new_path



    def read_output(self, pipe, process, timeout=1):
        data = ''
        last_time = time.time()
        # logger.critical("Start")

        while True:
            output = pipe.readline()
            if output:
                data += output.strip() + '\n'  # 累加输出

                last_time = time.time()  # 更新最后输出时间

            # 检查进程是否仍在运行
            if process.poll() is not None:
                break

            # 检查是否超过 timeout
            if time.time() - last_time >= timeout:
                if data:
                    logger.info(f"Output:\n{data.strip()}\n")
                    self.output_list.append(data.strip())
                    data = ''  # 重置累加的输出

        # 输出剩余的 data
        if data:
            logger.info(f"Output:\n{data.strip()}\n")
            self.output_list.append(data.strip())
        # logger.critical("Done")

    def execute_adb_commands_as_root(self, commands):
        """
        发送需要su root权限的指令，并且是在adb shell下
        :param commands: 接受一组command，但是每个command后面要跟回车
        :return: 返回一个list，但是这个list只有一个元素
        """
        self.output_list = []
        # 启动 adb shell
        adb_shell = subprocess.Popen(['adb', 'shell'], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE, text=True)

        # 启动一个线程用于读取输出
        output_thread = threading.Thread(target=self.read_output, args=(adb_shell.stdout, adb_shell))
        output_thread.start()

        for command in commands:
            # 发送命令
            adb_shell.stdin.write(command)
            adb_shell.stdin.flush()  # 确保命令被发送

            # 等待一段时间以确保命令执行完成
            time.sleep(1)
            # logger.info(f"Output for command '{command.strip()}':\n{self.output_list}\n" if self.output_list else
            #             f"{command.strip()} result: No output.")

        # 关闭 adb shell
        adb_shell.stdin.close()
        output_thread.join()  # 等待输出线程结束
        adb_shell.wait()
        return self.output_list[-1]

    @staticmethod
    def run_adb_command_with_check(command):
        """
        异常会被raise从而被捕获，run方法不会raise，而是作为文字信息输出
        :param command:
        :return:
        """
        # 构造完整的ADB命令
        full_command = f'{command}'
        logger.info(f"Will send command:{full_command}")

        try:
            # 执行命令并获取输出
            result = subprocess.check_output(full_command, text=True)
            # 打印命令输出
            # output = result.stdout.decode('utf-8')
            logger.info(f'Output:\n{result}')

        except subprocess.CalledProcessError as e:
            # 如果命令执行失败，打印错误信息
            logger.exception(f"Error: {e.stderr.decode('utf-8')}")
            result = False
            # output = e.stderr.decode('utf-8')
        finally:
            return result


if __name__ == '__main__':
    cmd = ADB()
    # add_path_to_environ()
    # adb("309be77b", 'COM14')
    # cmd.run_adb_command('adb devices')
    # cmd.run_shell_command('lsmod | grep wlan')
    cmds = [
        'su root\n',
        'sleep 3\n',
        'ls\n',
        'sleep 3\n',
        'svc bluetooth enable\n',
        'sleep 3\n',
        'settings get global bluetooth_on\n',
    ]
    #
    # res = cmd.execute_adb_commands_as_root(cmds)
    # print(f"type of res = {type(res)}")
    # print(len(res))
    # print("res",res)
    # cmd.run_adb_command_with_check('')
    # time.sleep(1)
    # cmds = [
    #     'adb shell',
    #     'lls'
    # ]
    cc = 'adb shell "ls"'
    a = cmd.execute_adb_commands_as_root(cmds)
    print(a)

    time.sleep(0.1)
    print("hi")
    print(type(a))