import time
from PIL import Image
import cv2
import numpy as np
import os
from utils import configuration
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

    # for j in range(gray_h):
    #     for k in range(gray_w):
    #         try:
    #             if j == 198 and k ==627:
    #                 print(img1[j, k])
    #                 print(img2[j, k])
    #         except:
    #             continue


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


    # 读取所有新老文件的路径
    for dir, dir_abs, files in os.walk(old_path):
        for file in files:
            old_file = os.path.join(dir, file)
            olds.append(old_file)
            names.append(file)
            # print(olds)
    for dir1, dir_abs1, files1 in os.walk(new_path):
        for file1 in files1:
            new_file = os.path.join(dir1, file1)
            news.append(new_file)
            # print(news)

    # 批量运行除码方法
    for a, what in enumerate(olds):
        whatto = news[a]
        target = os.path.join(target_path, names[a])
        remove_mozaic(what, whatto, target)


if __name__ == '__main__':
    use_remove()