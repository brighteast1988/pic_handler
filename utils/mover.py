import shutil
import zipfile
from PIL import Image
import os
from utils import configuration
import glob
picdir = "C:/Users/Administrator/Desktop/manga/2/temp"
savedir = "C:/Users/Administrator/Desktop/manga/2/tempsave"
ori_dir = "C:/Users/Administrator/Desktop/bavel02_mproj/images"


def movePic(pic, saveDir, target_size):   # 设置宽为210像素，高为425像素(对应宽5.5cm,高11cm)
    try:
        img = Image.open(pic)    # 读取图片
        o_width = img.width
        o_height = img.height
        size = [o_width, o_height]
        splitter = str(pic).rsplit('.', 1)
        realname = splitter[0] + '.png'
        # print('图片尺寸为：%s' % size)
        # print('图片名为：%s' % realname)
        # print(o_width,o_height)
        # if o_width == 3840 and o_height == 2160:
        #     img.close()
        #     shutil.move(pic, saveDir)
        for x, size in enumerate(target_size):
            try:
                # if str(o_width) == str(size[0]) and str(o_height) == str(size[1]):
                if int(o_width)/int(o_height) == int(size[0])/int(size[1]):
                    print('宽度为：%s ' % o_width)
                    print('高度为：%s ' % o_height)
                    img.close()
                    shutil.move(pic, saveDir)
                else:
                    continue
            except Exception as f:
                print("出错")
                import traceback  # 打印错误
                traceback.print_exception(f)

    except Exception as e:
        print("出错")
        import traceback         # 打印错误
        traceback.print_exception(e)


def multi(picdir,savedir):
    pic_list = []
    i = 0
    for dir, dir_abs, files in os.walk(picdir):
        for file in files:
            i += 1
            if file.endswith('.png') or file.endswith('.jpg'):
                pic_list.append(os.path.join(dir, file))
    print("共有%s 个文件"% i)

    for z, picture in enumerate(pic_list):
        movePic(picture, savedir, configuration.sizes)

def multimove():
    dirs = os.listdir(ori_dir)
    wow = []
    for dirname in dirs:
        name = dirname + '.zip'
        fullname = os.path.join(ori_dir, name)
        zip_File = zipfile.ZipFile(fullname, 'w')
        for dir, dir_abs, files in os.walk(ori_dir):
            for file in files:
                if not dirname.endswith('.png') and not dirname.endswith('.jpg'):
                    if dirname in file:
                        o_path = os.path.join(dir, file)
                        wow.append(file)
                        zip_File.write(o_path, compress_type=zipfile.ZIP_DEFLATED, arcname=file, )
        zip_File.close()
        if os.path.getsize(fullname) < 100000:
            os.remove(fullname)


                        # try:
                        #
                        #     zip_File.write(o_path, compress_type=zipfile.ZIP_DEFLATED)
                        #     zip_File.close()
                        # except:
                        #     continue


if __name__ == '__main__':
    # multi(picdir, savedir)
    multimove()