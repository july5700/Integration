import os
import psutil


def find_usb_drives():
    special_filename = 'Up.flag'
    # 获取所有磁盘分区信息
    partitions = psutil.disk_partitions()
    # 过滤出U盘（通常U盘的文件系统类型为'vfat'或'ntfs'）
    usb_drives = [p.mountpoint for p in partitions if 'removable' in p.opts]
    for drive in usb_drives:
        file_path = os.path.join(drive, special_filename)
        if os.path.exists(file_path):
            print("detected upgrade U disk")
            return drive
    return None




if __name__ == '__main__':
    usb_drives = find_usb_drives()
    print("USB Drives:", usb_drives)
    # flag_u = find_specific_drive()
    # print(flag_u)