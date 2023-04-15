from PIL import Image
import os
import glob
# picdir = "C:/Users/Administrator/Desktop/manga/2/temp"
# savedir = "C:/Users/Administrator/Desktop/manga/2/tempsave"
from utils import configuration
size_w = configuration.config_w
size_h = configuration.config_h

def convertPic(pic, saveDir, height):   # 设置宽为210像素，高为425像素(对应宽5.5cm,高11cm)
    try:
        img = Image.open(pic)    # 读取图片
        o_width = img.width
        o_height = img.height
        # print(o_width,o_height)
        height_scale = o_width / o_height
        # print(height_scale)
        resized = img.resize((int(height * height_scale), height), Image.ANTIALIAS)
        splitter = str(pic).rsplit('.', 1)
        realname = splitter[0] + '.png'
        resized.save(os.path.join(saveDir, os.path.basename(realname)))  # 保存图片
    except Exception as e:
        print("出错")
        import traceback         # 打印错误
        traceback.print_exception(e)


def convert_ksk(pic, saveDir, width, height):   # 设置宽为210像素，高为425像素(对应宽5.5cm,高11cm)
    try:
        img = Image.open(pic)    # 读取图片
        o_width = img.width
        o_height = img.height
        # print(o_width,o_height)
        height_scale = o_width / o_height
        # print(height_scale)
        resized = img.resize((width, height), Image.ANTIALIAS)
        splitter = str(pic).rsplit('.', 1)
        realname = splitter[0] + '.png'
        resized.save(os.path.join(saveDir, os.path.basename(realname)))  # 保存图片
    except Exception as e:
        print("出错")
        import traceback         # 打印错误
        traceback.print_exception(e)


def multi(picdir,savedir, height):
    pic_list = []
    for dir, dir_abs, files in os.walk(picdir):
        for file in files:
            if file.endswith('.png') or file.endswith('jpg'):
                pic_list.append(os.path.join(dir, file))

    for z, picture in enumerate(pic_list):
        convertPic(picture, savedir, height)


def multi_ksk(picdir, savedir, width, height):
    pic_list = []
    for dir, dir_abs, files in os.walk(picdir):
        for file in files:
            if file.endswith('.png') or file.endswith('jpg'):
                pic_list.append(os.path.join(dir, file))

    for z, picture in enumerate(pic_list):
        convert_ksk(picture, savedir, width, height)


#
# if __name__ == '__main__':
#     multi_ksk(picdir, savedir)