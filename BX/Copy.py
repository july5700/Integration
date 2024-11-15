from FindUDisk import find_usb_drives
import os
from tqdm import tqdm

def copy_large_file_to_UDisk(src_path, chunk_size=1024 * 1024):
    try:
        dst_path = find_usb_drives()
        # 检查源路径是否存在
        if not os.path.exists(src_path):
            raise FileNotFoundError(f"源路径 {src_path} 不存在")

        # 检查目标路径是否存在
        if not os.path.isdir(os.path.dirname(dst_path)):
            raise FileNotFoundError(f"目标目录 {os.path.dirname(dst_path)} 不存在")

        if os.path.isfile(src_path):
            # 单个文件复制
            file_size = os.path.getsize(src_path)
            with open(src_path, 'rb') as src_file, open(dst_path, 'wb') as dst_file:
                with tqdm(total=file_size, unit='B', unit_scale=True, desc=f"复制 {os.path.basename(src_path)}") as pbar:
                    while True:
                        data = src_file.read(chunk_size)
                        if not data:
                            break
                        dst_file.write(data)
                        pbar.update(len(data))
            print("文件复制成功")
            return True
        elif os.path.isdir(src_path):
            # 复制整个文件夹
            # 确保目标路径是一个文件夹
            if not dst_path.endswith(os.path.sep):
                dst_path += os.path.sep
            dst_path += os.path.basename(src_path)  # 在目标路径中添加源文件夹的名称

            for root, dirs, files in os.walk(src_path):
                relative_path = os.path.relpath(root, src_path)
                target_dir = os.path.join(dst_path, relative_path)
                os.makedirs(target_dir, exist_ok=True)
                for file in files:
                    src_file_path = os.path.join(root, file)
                    dst_file_path = os.path.join(target_dir, file)
                    file_size = os.path.getsize(src_file_path)
                    with open(src_file_path, 'rb') as src_file, open(dst_file_path, 'wb') as dst_file:
                        with tqdm(total=file_size, unit='B', unit_scale=True, desc=f"复制 {os.path.join(relative_path, file)}") as pbar:
                            while True:
                                data = src_file.read(chunk_size)
                                if not data:
                                    break
                                dst_file.write(data)
                                pbar.update(len(data))
            print("文件夹复制成功")
            return True
        else:
            raise ValueError(f"无效的源路径 {src_path}")
            # return Flase

        print("文件夹复制成功")


    except FileNotFoundError as e:
        print(e)
        return Flase
    except PermissionError:
        print("权限错误：无法访问文件或目录")
        return Flase
    except IsADirectoryError:
        print("目标路径是一个目录，而不是文件")
        return Flase
    except OSError as e:
        print(f"操作系统错误: {e}")
        return Flase
    except Exception as e:
        print(f"未知错误: {e}")
        return False




# 使用示例
# source_file = r"F:\ZeekrPackage\TCPBasicCAPL_Database_test_BX1E_Normal.zip"
# destination_file = r"I:\temp\TCPBasicCAPL_Database_test_BX1E_Normal.zip"  # 假设E:是U盘的驱动器号
# copy_large_file_with_progress(source_file, destination_file)