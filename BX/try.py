# from USBSwitch import USBSwitch
import os

# Todo
# 1. 修改unzip的代码，无参数化，固定src_zip，从ini文件中读取
# 2. 在笔记本上试运行
# 3. 挂载到服务器上试运行， 添加出发时间的机制
# 4. 完善另外2个BT的case，
# 5. 3个case都挂载到Jenkins上，试运行完整的集成测试
# 6. 尝试在另外一台电脑上抓取最新的代码
# 7. 建立另外一个project，专门放Mylog这些lib库
# 8. change on 05/11
import toml
from collections import OrderedDict

# 1. 读取现有的 TOML 文件
with open('cfg.toml', 'r', encoding='utf-8') as t:
    config = toml.load(t, _dict=OrderedDict)

# 2. 打印读取的内容
print("-" * 50)
print(config)

# 3. 访问和打印特定值
value = config['clients'][0]['name']
print(value)

# 4. 添加新的键值对
if 'test' not in config:
    config['test'] = OrderedDict()
config['test'] = '2023-11-11'

# 5. 修改现有的键值对
if 'database' not in config:
    config['database'] = OrderedDict()

# 确保 'database' 部分是一个 OrderedDict
if not isinstance(config['database'], OrderedDict):
    config['database'] = OrderedDict(config['database'])

# 添加新的键值对
config['database']['name_new123'] = 'dqy'
config['database']['port123'] = '10001123abc'

# 6. 打印修改后的配置
print("-" * 50)
print(config)

# 7. 写回文件
with open('cfg.toml', 'w', encoding='utf-8') as s:
    toml.dump(config, s)

# if __name__ == "__main__":
#     list_serial_ports()
