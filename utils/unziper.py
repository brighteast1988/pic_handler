from zipfile import ZipFile
import time
import shutil
import zipfile
import os
from utils import configuration
from tkinter.filedialog import (askopenfilename,
                                    askopenfilenames,
                                    askdirectory,
                                    asksaveasfilename)

filedir = configuration.unzip_path
ori_dir = configuration.old_path
filenames_new = []
filepaths_new = []
bakup_path = filedir + '/backup'
unzip_path = filedir + '/unzip'
# 时间戳

def unzip_file():
    # 批量解压文件
    filenames = os.listdir(filedir)#获取目录下所有文件名
    unzip_paths = []
    f_index = []
    if os.path.exists(bakup_path):
        pass
    else:
        print('创建备份目录')
        os.mkdir(bakup_path)

    if os.path.exists(unzip_path):
        pass
    else:
        os.mkdir(unzip_path)

    for filenamea in filenames:
        if os.path.isdir(filenamea):
            pass
        else:
            filename_new = filenamea.rsplit(".", 1)[0]
            filename_now = filename_new.replace(".", "_")
            path_old = os.path.join(filedir, filenamea)
            path_new = os.path.join(filedir, filename_now)
            filepaths_new.append(path_new)
            os.rename(path_old, path_new)
            backup_path = os.path.join(bakup_path, filenamea)
            shutil.copy(path_new, backup_path)

    for y, filename in enumerate(filepaths_new):
        filename_real = filename.rsplit("\\", 1)[1]
        filepath = os.path.join(filedir,filename_real)
        try:
            zip_file = zipfile.ZipFile(filepath) #获取压缩文件
        except:
            continue
        newfilepath = filename.split(".",1)[0]
        newfilepath = os.path.join(filedir,newfilepath)
        # 解压后的目录
        path_after = unzip_path + '/' + filename_real
        if os.path.isdir(path_after): # 根据获取的压缩文件的文件名建立相应的文件夹
            pass
        else:
            os.mkdir(path_after)
        for name in zip_file.namelist():# 解压文件
            zip_file.extract(name, path_after)
        zip_file.close()
        if os.path.exists(filepath):#删除原先压缩包
            os.remove(filepath)
        f_index.append(y)
        unzip_paths.append(path_after)
    return unzip_paths

def simple_Unzip(whattoUnzip):
    # 普通解压程序，适用于所有指定文件解压
    filename_real = whattoUnzip.rsplit("/", 1)[1]
    file_exact = filename_real.rsplit('.', 1)[0]
    filepath = whattoUnzip.rsplit("/", 1)[0]
    unzip_path = filepath + '/unzip'
    if os.path.exists(unzip_path):
        pass
    else:
        os.mkdir(unzip_path)
    zip_file = zipfile.ZipFile(whattoUnzip)
    newfilepath = whattoUnzip.split(".",1)[0]
    newfilepath = os.path.join(filedir,newfilepath)
    # 解压后的目录
    path_after = unzip_path +'/' + file_exact
    if os.path.isdir(path_after): # 根据获取的压缩文件的文件名建立相应的文件夹
        pass
    else:
        os.mkdir(path_after)
    for n, name in enumerate(zip_file.namelist()):# 解压文件
        if '.jpg' or '.png' in str(name):
            format = name.rsplit('.', 1)[1]
            new_name = str(n+1) + 'a.' + format
            zip_file.extract(name, path_after)
            path_z = os.path.join(path_after, name)
            path_n = os.path.join(path_after, new_name)
            os.rename(path_z, path_n)
        else:
            continue
    zip_file.close()
    if os.path.exists(whattoUnzip):#删除原先压缩包
        os.remove(whattoUnzip)
    return path_after


def fill_original():
    # 选择文件并解压到指定源目录
    filenames = askopenfilenames()
    ori_dir = configuration.old_path
    files_data = []
    file_paths = []
    if filenames is None:
        pass
    else:
        for filename in filenames:
            t = str(time.time()).replace('.', '')
            filename_new = filename.rsplit("/", 1)[1]
            copypath = ori_dir + '/' + filename_new
            copyreal = ori_dir + '/' + str(t)
            shutil.copy(filename, copyreal)
            # 解压到指定目录
            file_data = simple_Unzip(copyreal)
            files_data.append((copypath, file_data))
        return files_data



def fill_data():
    # 点击添加文件并返回路径
    filenames = askopenfilenames()
    files_data = []
    # f_index = unziper.unzip_file()[0]
    # file_paths = unziper.unzip_file()[1]
    file_datas = []
    file_paths = []
    if filenames == '':
        pass
    else:
        for a, filepath in enumerate(filenames):
            file_paths.append(filepath)
            filename = filepath.rsplit("/", 1)[1]
            copypath = os.path.join(filename, filedir)
            shutil.copy(filepath, copypath)
        files_data = unzip_file()
    return files_data



def del_pic_handle_cache():
    # 清除缓存
    shutil.rmtree(bakup_path)
    shutil.rmtree(unzip_path)

