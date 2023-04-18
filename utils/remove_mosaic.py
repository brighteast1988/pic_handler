# -*- coding: utf-8 -*-
import shutil
import time
from PIL import Image
import cv2
import numpy as np
import os
from utils import configuration
import numpy as np
# from configparser import ConfigParser
# if os.path.exists('config.ini'):
#     pass
# else:
#     with open('config.ini', 'w+', encoding='utf-8') as file:
#         configure = f"""
# [folder]
# old_path = C:/Users/Administrator/Desktop/TEMP/jp
# new_path = C:/Users/Administrator/Desktop/TEMP/en
# target_path = C:/Users/Administrator/Desktop/TEMP/after
# """
#         file.write(configure)
#         file.close()


# 读取配置文件
# key_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
# pathKey = ConfigParser()
# pathKey.read('config.ini', encoding='utf-8')
# # 读取目录
# old_path = pathKey.get('folder', 'old_path')
# new_path = pathKey.get('folder', 'new_path')
# target_path = pathKey.get('folder', 'target_path')
old_path = configuration.old_path
new_path = configuration.new_path
target_path = configuration.target_path




# img = Image.open('C:/Users/Administrator/Desktop/manga/2/test/jp.png')


def remove_mozaic(old, new, target):
    img = cv2.imread(old, 1)
    ori_img = cv2.imread(new, 1)
    # 图像灰度化处理
    grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    grayImage2 = cv2.cvtColor(ori_img, cv2.COLOR_BGR2GRAY)

    gray_h = np.array(grayImage).shape[0]
    gray_w = np.array(grayImage).shape[1]

    img1 = np.array(grayImage)
    img2 = np.array(grayImage2)

    for j in range(gray_h):
        for k in range(gray_w):
            try:
                if img1[j, k] != img2[j, k] and img1[j, k] == 255:
                    img1[j, k] = img2[j, k]
            except:
                continue
    cv2.imwrite(target, img1)

def use_remove():
    # 批量处理文件
    olds = []
    news = []
    names = []
    names_com = []

    # 读取所有新老文件的路径
    for dir, dir_abs, files in os.walk(old_path):
        for file in files:
            if str(file).endswith('.jpg') or str(file).endswith('.png'):
                old_file = os.path.join(dir, file)
                olds.append(old_file)
                names.append(file)
    for dir1, dir_abs1, files1 in os.walk(new_path):
        for file1 in files1:
            if str(file1).endswith('.jpg') or str(file1).endswith('.png'):
                new_file = os.path.join(dir1, file1)
                news.append(new_file)
                names_com.append(file1)


    # 对比差异后移动不一致的文件
    difference = set(names).difference(set(names_com))
    if difference != {}:
        unable_Handle = target_path + '/unhandle'
        if os.path.exists(unable_Handle):
            pass
        else:
            os.mkdir(unable_Handle)
        # 定义移动路径
        for diff_File in difference:
            diff_path = os.path.join(unable_Handle, diff_File)
            ori_diff_path = os.path.join(old_path, diff_File)
            shutil.move(ori_diff_path, diff_path)
            olds.remove(ori_diff_path)

    # 批量运行除码方法
    for a, what in enumerate(olds):
        whatto = news[a]
        target = os.path.join(target_path, names[a])
        remove_mozaic(what, whatto, target)
def GUI_use_Remosaic(old_path, new_path, target_path):
    # 批量处理文件
    olds = []
    news = []
    names = []
    names_com = []
    # 读取所有新老文件的路径
    for dir, dir_abs, files in os.walk(old_path):
        for file in files:
            if str(file).endswith('.jpg') or str(file).endswith('.png'):
                old_file = os.path.join(dir, file)
                olds.append(old_file)
                names.append(file)
    for dir1, dir_abs1, files1 in os.walk(new_path):
        for file1 in files1:
            if str(file1).endswith('.jpg') or str(file1).endswith('.png'):
                new_file = os.path.join(dir1, file1)
                news.append(new_file)
                names_com.append(file1)

    # 对比差异后移动不一致的文件
    difference = set(names).difference(set(names_com))
    if difference != {}:
        unable_Handle = target_path + '/unhandle'
        if os.path.exists(unable_Handle):
            pass
        else:
            os.mkdir(unable_Handle)
        # 定义移动路径
        for diff_File in difference:
            diff_path = os.path.join(unable_Handle, diff_File)
            ori_diff_path = os.path.join(old_path, diff_File)
            shutil.move(ori_diff_path, diff_path)
            olds.remove(ori_diff_path)

    # 批量运行除码方法
    for a, what in enumerate(olds):
        for b, compare in enumerate(news):
            whatto = what.rsplit('\\', 1)[1]
            tocompare = compare.rsplit('\\', 1)[1]
            if whatto == tocompare:
                target = os.path.join(target_path, whatto)
                try:
                    remove_mozaic(what, compare, target)
                except:
                    continue


if __name__ == '__main__':
    use_remove()