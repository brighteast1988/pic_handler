import os
from configparser import ConfigParser
if os.path.exists('config.ini'):
    pass
else:
    with open('config.ini', 'w+', encoding='utf-8') as file:
        configure = f"""
[folder]
pic_path = C:/Users/Administrator/Desktop/manga/2/temp
save_path = C:/Users/Administrator/Desktop/manga/2/tempsave

[size]
size1_w = 1920
size1_h = 1080
size2_w = 2560
size2_h = 1440
size3_w = 3840
size3_h = 2160



[mode]
type = resize"""
        file.write(configure)
        file.close()

# 读取配置文件
key_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
pathKey = ConfigParser()
pathKey.read('config.ini', encoding='utf-8')
# 读取目录
pic_path = pathKey.get('folder', 'pic_path')
save_path = pathKey.get('folder', 'save_path')
# 尺寸清单（用于筛选尺寸模式）
sizes = []
size1 = [pathKey.get('size', 'size1_w'), pathKey.get('size', 'size1_h')]
size2 = [pathKey.get('size', 'size2_w'), pathKey.get('size', 'size2_h')]
size3 = [pathKey.get('size', 'size3_w'), pathKey.get('size', 'size3_h')]
size4 = [pathKey.get('size', 'size4_w'), pathKey.get('size', 'size4_h')]
size5 = [pathKey.get('size', 'size5_w'), pathKey.get('size', 'size5_h')]
sizes.append(size1)
sizes.append(size2)
sizes.append(size3)
sizes.append(size4)
sizes.append(size5)
# 读取模式
mode = pathKey.get('mode', 'type')


if __name__ == '__main__':
    print(sizes)