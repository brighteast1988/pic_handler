from zipfile import ZipFile
import shutil
import zipfile
import os
from utils import configuration
from tkinter.filedialog import (askopenfilename,
                                    askopenfilenames,
                                    askdirectory,
                                    asksaveasfilename)

filedir = configuration.unzip_path
filenames_new = []
filepaths_new = []
bakup_path = filedir + '/backup'
unzip_path = filedir + '/unzip'


def unzip_file():
    # 批量解压文件
    filenames = os.listdir(filedir)#获取目录下所有文件名
    unzip_paths = []
    f_index = []
    if os.path.exists(bakup_path):
        pass
    else:
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
        path_after = unzip_path +'/' + filename_real
        if os.path.isdir(path_after): # 根据获取的压缩文件的文件名建立相应的文件夹
            pass
        else:
            os.mkdir(path_after)
        for name in zip_file.namelist():# 解压文件
            zip_file.extract(name, path_after)
        zip_file.close()
        Conf = os.path.join(newfilepath,'conf')
        if os.path.exists(Conf):#如存在配置文件，则删除（需要删则删，不要的话不删）
            shutil.rmtree(Conf)
        if os.path.exists(filepath):#删除原先压缩包
            os.remove(filepath)
        f_index.append(y)
        unzip_paths.append(path_after)
    return unzip_paths


def fill_data():
    # 点击添加文件并返回路径
    filenames = askopenfilenames()
    files_data = []
    # f_index = unziper.unzip_file()[0]
    # file_paths = unziper.unzip_file()[1]
    file_datas = []
    file_paths = []
    if filenames is None:
        pass
    else:
        for a, filepath in enumerate(filenames):
            file_paths.append(filepath)
            filename = filepath.rsplit("/", 1)[1]
            copypath = os.path.join(filename, filedir)
            shutil.copy(filepath, copypath)
        files_data = unzip_file()
    return files_data


def del_cache():
    shutil.rmtree(bakup_path)
    shutil.rmtree(unzip_path)


