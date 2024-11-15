from loguru import logger
import serial
import time

# 1. 添加了清楚缓存区，防止read_until的时候，读取到了send command的#导致的提前抓取结果的问题
class Serial(object):
    def __init__(self, port, baudrate=115200, timeout=3):  # 减少超时时间
        """
        初始化 Serial 类

        :param port: 串口号，例如 'COM4'
        :param baudrate: 波特率，默认为 115200
        :param timeout: 超时时间，默认为 3 秒，这个数值取决于command中所需时间最长的那个
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None

    def open(self):
        """
        打开串口
        """
        if self.ser and self.ser.is_open:
            logger.info(f"Serial port {self.port} is already open.")
            return

        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            logger.info(f"Serial port {self.port} opened successfully.")
        except serial.SerialException as e:
            logger.error(f"Failed to open serial port {self.port}: {e}")
            raise

    def close(self):
        """
        关闭串口
        """
        if self.ser and self.ser.is_open:
            self.ser.close()
            logger.info(f"Serial port {self.port} closed successfully.")
        else:
            logger.warning(f"Serial port {self.port} is not open.")
            raise

    def clear_buffers(self):
        """
        清空输入和输出缓存区
        """
        if not self.ser or not self.ser.is_open:
            logger.error("Serial port is not open.")
            return

        try:
            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()
            logger.info("Buffers cleared successfully.")
        except serial.SerialException as e:
            logger.error(f"Failed to clear buffers: {e}")
            raise

    def send_command(self, command, end_marker=b'#'):
        """
        发送命令到串口

        :param command: 要发送的命令字符串
        """

        if not self.ser or not self.ser.is_open:
            logger.error("Serial port is not open.")
            return

        try:
            self.clear_buffers()
            self.ser.write(f"{command}\n".encode())
            logger.info(f"Command sent: [{command}]")
            result = b''
            data = self.ser.read_until(end_marker)
            result += data
            # if b'#' in result:
            #     print("find #")
            res = result.decode().replace('\r', '')
            if len(res) == 0:
                logger.error("Response received 0 byte, check the environment manually")
                return False
            else:
                logger.info(f"Response [{len(res)}] received: \n{'='*60}\n{res}\n{'='*60}")
                return res

        except serial.SerialException as e:
            logger.exception(f"Failed to send command: {e}")
            raise

    def send_command_without_response(self, command):
        """
        发送命令到串口

        :param command: 要发送的命令字符串
        """

        if not self.ser or not self.ser.is_open:
            logger.error("Serial port is not open.")
            return

        try:
            self.ser.write(f"{command}\n".encode())
            logger.info(f"Command sent: {command}")

        except serial.SerialException as e:
            logger.exception(f"Failed to send command: {e}")
            raise

    def log_in_as_root(self):
        if not self.ser:
            self.ser.open()
        res = self.send_command('\n')
        if 'login' in res:
            self.send_command('root')
            time.sleep(1)
            self.send_command('ady@#45623csdihfciufZeekra5~00X')
            time.sleep(1)
        else:
            logger.info("Already logged in")
        # time.sleep(1)
        # self.send_command('dbus-send --bus=tcp:host=192.168.0.4,port=999 --type=signal / PMA.Update.SW.OK array:byte:1')

    def upgrade(self):
        if not self.ser:
            self.ser.open()
        self.log_in_as_root()
        self.send_command('dbus-send --bus=tcp:host=192.168.0.4,port=999 --type=signal / PMA.Update.SW.OK array:byte:1')
        time.sleep(1)

    def cancel_upgrade(self):
        if not self.ser:
            self.ser.open()
        self.log_in_as_root()
        self.send_command('swdl_utils - r clear')
        time.sleep(1)
        self.send_command('reset')

if __name__ == '__main__':
    # 创建 Serial 类的实例
    s = Serial('COM4', baudrate=115200, timeout=10)  # 增加超时时间`

    try:
        # 打开串口
        s.open()
        s.log_in_as_root()
        # 发送命令并读取响应
        command = '\n'  # 替换为实际的命令
        # s.send_command_without_response('cd /bin')
        # time.sleep(1)
        # response = s.send_command('pwd', end_marker=b'#')
        # time.sleep(1)
        response = s.send_command(command)


    finally:
        # 关闭串口
        s.close()