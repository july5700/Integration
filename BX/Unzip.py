import zipfile
import os
from tqdm import tqdm
from loguru import logger


def unzip_file_with_progress(zip_path, output_path):
    try:
        # cfg = IniConfig('download.ini')
        # version = cfg.read_cfg('version', 'current_version')

        # 打开 ZIP 文件
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # 获取 ZIP 文件中的所有文件名
            file_list = zip_ref.namelist()

            # 创建目标目录（如果不存在）
            if not os.path.exists(output_path):
                os.makedirs(output_path)

            # 使用 tqdm 创建进度条
            with tqdm(total=len(file_list), desc='Extracting', unit='file') as pbar:
                for file in file_list:
                    # 解压单个文件
                    zip_ref.extract(file, output_path)
                    # 更新进度条
                    pbar.update(1)

        logger.info(f"ZIP 文件 {zip_path} 已解压到 {output_path}")
        return True
    except Exception as e:
        logger.exception(e)
        raise


# 调用函数
if __name__ == "__main__":
    zip_path = r"F:\DCEU_测试_Secure boot.zip"  # ZIP 文件的路径
    output_path = r"F:\try_to_unzip_here\test"  # 解压后的文件存放路径

    unzip_file_with_progress(zip_path, output_path)