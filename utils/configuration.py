from configparser import ConfigParser
import os




current_path = os.path.abspath(__file__)
# key_path = os.path.join((os.path.abspath(os.path.dirname(current_path) + os.path.sep + "..")), 'config.ini')
key_path = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'config.ini')

if os.path.exists(key_path):
    pass
else:
    with open(key_path, 'w+', encoding='utf-8') as file:
        configure = f"""
[folder]
#For resize Pictures
pic_path = C:/Users/Administrator/Desktop/TEMP/before
save_path = C:/Users/Administrator/Desktop/TEMP/after

#For Reindex Pictures
unzip_path = C:/Users/Administrator/Desktop/TEMP/before
#For Removing mosaic
old_path = C:/Users/Administrator/Desktop/TEMP/jp
new_path = C:/Users/Administrator/Desktop/TEMP/en
target_path = C:/Users/Administrator/Desktop/TEMP/after


[mode]
type = resize

[size]
size1_w = 1920
size1_h = 1080
size2_w = 2560
size2_h = 1440
size3_w = 3840
size3_h = 2160
size4_w = 4096
size4_h = 2304
size5_w = 2048
size5_h = 1152

[size_modify]
size_w = 1360
size_h = 1920


    """
        file.write(configure)
        file.close()




pathKey = ConfigParser()
pathKey.read(key_path, encoding='utf-8')
filepath = pathKey.get('folder', 'pic_path')
targetpath = pathKey.get('folder', 'save_path')
config_w = pathKey.get('size_modify', 'size_w')
config_h = pathKey.get('size_modify', 'size_h')
unzip_path = pathKey.get('folder', 'unzip_path')
# 日文原图片的路径（去码用）
old_path = pathKey.get('folder', 'old_path')
# 英文对比图（待对比）的路径
new_path = pathKey.get('folder', 'new_path')
# 用于去马赛克后的结果文件的存放路径
target_path = pathKey.get('folder', 'target_path')

# 下面这段配置为判断是否为壁纸的，暂没有用
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
# 读取目录
pic_path = pathKey.get('folder', 'pic_path')
save_path = pathKey.get('folder', 'save_path')

def write_w(size_w):
    pathKey.set('size_modify', 'size_w', size_w)
    with open('config.ini', 'w', encoding='utf-8') as f:
        pathKey.write(f)


def write_h(size_h):
    pathKey.set('size_modify', 'size_h', size_h)
    with open('config.ini', 'w', encoding='utf-8') as f:
        pathKey.write(f)


def reload_config():
    key_path = os.path.join((os.path.abspath(os.path.dirname(current_path) + os.path.sep + "..")), 'config.ini')
    pathKey = ConfigParser()
    pathKey.read(key_path, encoding='utf-8')
    reload_w = pathKey.get('size_modify', 'size_w')
    reload_h = pathKey.get('size_modify', 'size_h')
    return reload_w, reload_h

def reload_remsaic_workflow():
    key_path = os.path.join((os.path.abspath(os.path.dirname(current_path) + os.path.sep + "..")), 'config.ini')
    pathKey = ConfigParser()
    pathKey.read(key_path, encoding='utf-8')
    unzip_path = pathKey.get('folder', 'unzip_path')
    old_path = pathKey.get('folder', 'old_path')
    target_path = pathKey.get('folder', 'target_path')
    return unzip_path, old_path, target_path
