import serial.tools.list_ports
from binascii import a2b_hex
import zipfile
import shutil
from loguru import logger as logging
import os
import sys
import subprocess
import serial
import serial.tools.list_ports

import re
from time import sleep
import time


class CMDHexTable:
    cmd_hex_table = [
        [0x09, 0x01, 0x01, 0x31, 0x00, 0x00, 0x00, 0x00, 0x77, 0xD5],  # Clear USB
        [0x09, 0x01, 0x01, 0x31, 0x00, 0x00, 0x00, 0x01, 0xB6, 0x15],  # 1
        [0x09, 0x01, 0x01, 0x31, 0x00, 0x00, 0x00, 0x02, 0xF6, 0x14],  # 2
        [0x09, 0x01, 0x01, 0x31, 0x00, 0x00, 0x00, 0x04, 0x76, 0x16],  # 3
        [0x09, 0x01, 0x01, 0x31, 0x00, 0x00, 0x00, 0x08, 0x76, 0x13],  # 4
        [0x09, 0x01, 0x01, 0x31, 0x00, 0x00, 0x00, 0x10, 0x76, 0x19],  # 5
        [0x09, 0x01, 0x01, 0x31, 0x00, 0x00, 0x00, 0x20, 0x76, 0x0D],  # 6
        [0x09, 0x01, 0x01, 0x31, 0x00, 0x00, 0x00, 0x40, 0x76, 0x25],  # 7
        [0x09, 0x01, 0x01, 0x31, 0x00, 0x00, 0x00, 0x80, 0x76, 0x75],  # 8
        [0x09, 0x01, 0x01, 0x31, 0x00, 0x00, 0x03, 0x08, 0x76, 0xE3],  # 9power供电
        [0x09, 0x01, 0x01, 0x31, 0x00, 0x00, 0x03, 0x08, 0x77, 0xD5],  # 10断开所有USB
        [0x09, 0x01, 0x01, 0x31, 0x00, 0x00, 0x03, 0x08, 0x77, 0x25],  # 11断开所有K通道
    ]
    
    
class USBSwitch:
    def __init__(self):
        # self.usb_switch_port = self.GetUSBHubPort()
        self.usb_switch_port = ''
        # self.open_com = serial.Serial(PORT_ID, 38400, timeout=0.5)
        self.open_com = None
        self.switch_time = 0.5

    def get_usb_switch_port(self):
        try:
            port_list = list(serial.tools.list_ports.comports())
            logging.info(f"Detect port_list = {port_list}")
            serial_port_list = []

            # get all com
            if len(port_list) <= 0:
                logging.info("NO serial port was find!")
                # return False
            else:
                for item in port_list:
                    if item[1].startswith('USB Serial Port') and item[2].startswith('USB VID:PID=0403:6001'):
                        # print("Serial Port %s" %item.device)
                        serial_port_list.append(item.device)
            logging.info(f"Collect serial_port_list = {serial_port_list}")
            if len(serial_port_list) == 0:
                logging.critical("No USB switch device was found")

            elif len(serial_port_list) == 1:
                self.usb_switch_port = serial_port_list[0]
                logging.info(f"find USB switch: {self.usb_switch_port}")
                return self.usb_switch_port

            elif len(serial_port_list) > 1:
                self.usb_switch_port = serial_port_list[-1]
                self.usb_switch_port = input("Please input USB switch com port like: 'COM4'")
                if self.usb_switch_port in serial_port_list:
                    logging.info(f"use USB switch:{self.usb_switch_port}")
                    return self.usb_switch_port

                else:
                    logging.error("Incorrect!")
                    # sys.exit(-1)
        except Exception as e:
            logging.exception(f"Error occurs: {e}")

    def init_usb_switch(self):
        """
            connect the device with pc by serial port [COM11]
        """
        logging.info('Start to initial USB switch...')

        try:
            self.usb_switch_port = self.get_usb_switch_port()
            self.open_com = serial.Serial(self.usb_switch_port, 38400, timeout=0.5)
            self.port_open()
            time.sleep(self.switch_time)
            logging.info("Clear all USB...")
            self.usb_switch_to(0)
            time.sleep(self.switch_time)
            logging.info("Disconnect all USB...")
            self.usb_switch_to(10)
            time.sleep(self.switch_time)

            # hex_list = [0x09, 0x01, 0x01, 0x31, 0x00, 0x00, 0x03, 0x08, 0x76, 0xE3]
            # self.open_com.write(a2b_hex(self.get_hex_cmd(hex_list)))
            logging.info("Give power to all USB...")
            self.usb_switch_to(9)
            time.sleep(self.switch_time)
            logging.info("Initial done")
        except Exception as _:
            logging.exception("Fail to initial...")

    @staticmethod
    def get_hex_cmd(hex_list):
        return ''.join([f'{i:02x}' for i in hex_list])

    def send_hex_cmd(self, hex_cmd):
        try:
            if not self.open_com:
                self.open_com = serial.Serial(self.usb_switch_port, 38400, timeout=0.5)
            logging.info(f"Will wirte cmd = {hex_cmd}")
            self.open_com.write(a2b_hex(hex_cmd))
            # self.open_com.write(hex_cmd)
        except:
            logging.exception(f"Fail to write cmd:{hex_cmd}")

    def port_open(self):
        if not self.open_com.isOpen():
            self.open_com.open()

    def port_close(self):
        self.open_com.close()
        self.open_com = None
        logging.info("Close current port")


    def usb_switch_to(self, index):
        """
        Parameter
            nIndex  : 0     Clear USB
            nIndex  : 1..8  Switch USB
        Return
            none

        Product name : USB switch
        Model number : customization
        Description  : connect the device with pc by serial
                    port [COM11], serial parameter is required
                    by the device with fixed value from datasheet
        """
        if index < 0 or index > 11:
            logging.error("ERROR! Parameter out of range")
            sys.exit(0)
        hex_table = CMDHexTable().cmd_hex_table
        # logging.info(f"hex_table:\n {hex_table}\n")
        cmd = self.get_hex_cmd(hex_table[index])
        self.send_hex_cmd(cmd)

    def switch_to_pc(self):
        """
        plug usb to 'USB1'
        :return:
        """
        time.sleep(self.switch_time)
        self.usb_switch_to(1)
        time.sleep(self.switch_time)
    def switch_to_ecu(self):
        """
        plug usb to 'USB2'
        :return:
        """
        time.sleep(self.switch_time)
        self.usb_switch_to(2)
        time.sleep(self.switch_time)


if __name__ == '__main__':
    """
    steps：
    1. initial，同时给所有port供电，发9
    2. clear all usb，发0
    3. 切到目标port，发1~8
    """
    s = USBSwitch()
    time.sleep(1)
    s.init_usb_switch()
    s.switch_to_ecu()
    # s.switch_to_pc()


    s.port_close()

