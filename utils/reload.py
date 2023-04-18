from configparser import ConfigParser
import os

def reloadconfig():
    current_path = os.path.abspath(__file__)
    key_path = os.path.join((os.path.abspath(os.path.dirname(current_path) + os.path.sep + "..")), 'config.ini')
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
    return target_path
