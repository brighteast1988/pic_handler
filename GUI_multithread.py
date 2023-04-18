# -*- coding: utf-8 -*-
import threading
import time

import ttkbootstrap as tk
import shutil
from utils.resize import multi
from utils.resize import multi_ksk
from ttkbootstrap.constants import *
from tkinter.filedialog import (askopenfilename,
                                    askopenfilenames,
                                    askdirectory,
                                    asksaveasfilename)
import os
from utils import configuration, unziper, reload, remove_mosaic
from configparser import ConfigParser

filepath = configuration.filepath
targetpath = configuration.targetpath
config_w = configuration.config_w
config_h = configuration.config_h
pic_Path = configuration.pic_path
save_Path = configuration.save_path
pathKey = configuration.pathKey


class GUI():
    button_list = []
    object_list = []
    def __init__(self, root):
        '''创建窗口和frame'''
        self.initGUI(root)

    def initGUI(self, root):
        root.title('Manga Handler')
        root.geometry('960x840')
        # 定义欢迎界面的frame
        self.frame_c = tk.Frame(root)
        self.frame_c.place(x=460, y=350, anchor='center')
        self.frame_b = tk.Frame(self.frame_c)
        self.frame_b.pack(anchor='center', side='top')
        # 新建标签选项卡
        # 定义按钮操作栏的frame
        self.framebtn = tk.Labelframe(root, text='图片缩放处理')
        # Labelbtns = tk.Label(self.framebtn, background='cyan')
        # Labelbtns.pack(anchor='w')
        # 所有属于按钮操作栏的子frame
        self.frame = tk.Frame(self.framebtn)
        self.frame.place(anchor='center')
        self.framer = tk.Frame(self.framebtn)
        self.framer.place(anchor='center')
        self.frame_l = tk.Frame(self.framebtn)
        self.frame_l.pack(anchor='center')
        self.frame_btns = tk.Frame(self.framebtn)
        self.frame_btns.pack()
        # 宽高设置输入栏
        self.frame_enter = tk.Frame(self.framebtn)
        self.frame_enter.pack(anchor='center', side='bottom')
        self.text = tk.StringVar()
        self.text1 = tk.StringVar()
        # 右侧列表操作栏
        self.frame_listbox = tk.Frame(root)
        self.ttframe = tk.LabelFrame(self.frame_listbox, text='修改图片起始页数')
        self.conframe = tk.Frame(self.ttframe)
        self.conframe.pack(anchor='center', side=BOTTOM, expand=True)
        # 按钮栏
        self.btns = tk.Frame(self.conframe)
        self.btn_add = tk.Button(self.btns, text='添加文件', bootstyle=(SUCCESS, OUTLINE), command=self.t_file_handle)
        self.btn_unable_add = tk.Button(master=self.btns, text='添加文件', bootstyle=(SECONDARY, OUTLINE))
        self.btn_del = tk.Button(self.btns, text='清空列表', bootstyle=(DANGER, OUTLINE), command=self.emptyList)
        self.btns.pack(side=RIGHT, expand=True, padx=10)
        self.btn_del.pack(side=RIGHT, padx=10)
        self.btn_add.pack(side=RIGHT, padx=10)
        # 定义想要添加起始页数的文件
        self.file_datas = []
        self.text_file = tk.StringVar()
        self.labelNow = tk.Label(self.frame_listbox, textvariable=self.text_file, wraplength=500, justify='left')
        # 去码操作区
        self.remosaicFrame = tk.Frame(root, width=77)
        # self.labeltemp = tk.Label(self.remosaicFrame, background='blue', width=77)
        # self.labeltemp.pack(side=TOP)
        self.remosaic_Label = tk.Labelframe(master=self.remosaicFrame, text='去马赛克处理')
        self.label_remosaic = tk.Label(self.remosaic_Label, width=80)
        self.text_ori_root = tk.StringVar()
        self.text_com_root = tk.StringVar()
        # 定义去码信息列表
        self.rtv = tk.Treeview(master=self.label_remosaic, columns=[0, 1, 2, 3], show=HEADINGS, height=5)
        # 文件信息标签（去码路径）
        self.original_root_r = tk.Label(self.remosaicFrame, textvariable=self.text_ori_root, justify='left',
                                        wraplength=865)
        self.compare_root_r = tk.Label(self.remosaicFrame, textvariable=self.text_com_root, justify='left',
                                       wraplength=750)
        # UI交互
        self.btn_add_ori = tk.Button(master=self.remosaic_Label, text='添加源文件', command=self.fill_remosaic_data)
        self.btn_unable_add_ori = tk.Button(master=self.remosaic_Label, text='添加源文件',
                                            bootstyle=(SECONDARY, OUTLINE))
        self.btn_add_com = tk.Button(master=self.remosaic_Label, text='添加对比文件', command=self.fill_compare_data)
        self.btn_unable_add_com = tk.Button(master=self.remosaic_Label, text='添加对比文件',
                                            bootstyle=(SECONDARY, OUTLINE))
        self.btn_remosaic = tk.Button(master=self.remosaic_Label, text='开始去码', command=self.start_Remosiac)
        self.btn_unable_start_remosaic = tk.Button(master=self.remosaic_Label, text='开始去码',
                                                   bootstyle=(SECONDARY, OUTLINE))
        self.btn_config_Remosaic_target = tk.Button(master=self.remosaic_Label, text='修改缓存路径(重启生效)',
                                                    command=self.re_Modify)

        self.show_info()
        try:
            root.protocol('WM_DELETE_WINDOW', self.del_cache())
        except:
            print('程序已退出')

    def resize_pic(self):
        now_size = configuration.reload_config()
        now_h = int(now_size[1])
        multi(pic_Path, save_Path, now_h)

    def resize_ksk(self):
        now_size = configuration.reload_config()
        now_w = int(now_size[0])
        now_h = int(now_size[1])
        multi_ksk(pic_Path, save_Path, now_w, now_h)

    def input_size(self):
        # 输入并保存宽度设置
        size_w = self.size_Enter_w.get()
        configuration.write_w(size_w)
        # 输入并保存宽度设置
        size_h = self.size_Enter_h.get()
        configuration.write_h(size_h)
        # 判断宽高值是否缺省
        now_size = configuration.reload_config()
        if now_size == ('', ''):
            configuration.write_w('1418')
            configuration.write_h('2000')
        elif now_size[1] == '':
            configuration.write_w('1418')
            configuration.write_h('2000')

    def change_pic_Path(self):
        # 选择文件并更新显示当前配置
        directory = askdirectory()
        if directory == '':
            pass
        else:
            pathKey.set('folder', 'pic_path', directory)
            self.text.set(directory)
        with open('config.ini', 'w', encoding='utf-8') as f:
            pathKey.write(f)

    def change_save_Path(self):
        directory1 = askdirectory()
        if directory1 == '':
            pass
        else:
            pathKey.set('folder', 'save_path', directory1)
            self.text.set(directory1)
        with open('config.ini', 'w', encoding='utf-8') as f:
            pathKey.write(f)

    def show_info(self):
        self.frame_c.destroy()
        # 加载左侧窗口
        self.framebtn.pack(anchor='nw', padx=60, pady=60)
        self.frame_listbox.place(x=370, y=60)
        self.remosaicFrame.place(x=60, y=490)
        self.remosaic_Label.pack(side=TOP)
        self.pic_handle()
        self.file_handle()
        self.remosaic()
        root.mainloop()

    def file_handle(self):
        # 按钮们
        self.file_form()

    def t_file_handle(self):
        T = threading.Thread(target=self.fill_data)
        x = self.tv.get_children()
        print(x)
        if str(x) != '()':
            self.btn_add.destroy()
            self.btn_unable_add = tk.Button(master=self.btns, text='添加文件', bootstyle=(SECONDARY, OUTLINE))
            self.btn_unable_add.pack(side=RIGHT, padx=10)
        T.start()

    def remosaic(self):
        # 定义列表表头
        tree_index = '序号'
        tree_head_root = '源文件路径'
        tree_head_count = '对比路径'
        tree_head_control = '运行状态'
        self.label_remosaic.pack()
        # 定义列表格式
        self.rtv.heading(0, text=tree_index)
        self.rtv.heading(1, text=tree_head_root)
        self.rtv.heading(2, text=tree_head_count)
        self.rtv.heading(3, text=tree_head_control)
        self.rtv.column(0, width=50, anchor='center')
        self.rtv.column(1, width=330, anchor='center')
        self.rtv.column(2, width=330, anchor='center')
        self.rtv.column(3, width=120, anchor='center')
        self.rtv.pack()
        # 按钮布局
        self.btn_config_Remosaic_target.pack(side=RIGHT, padx=10)
        self.btn_unable_add_com.pack(side=RIGHT, padx=10)
        self.btn_add_ori.pack(side=RIGHT, padx=10)
        self.rtv.bind('<Double-1>', self.open_Target)
        self.rtv.bind('<ButtonRelease-1>', self.selectItemremosaic)
        self.rtv.bind('<2>', self.open_Original)
        self.rtv.bind('<3>', self.open_Compare)

    def file_form(self):
        tree_index = '序号'
        tree_head_root = '文件路径'
        tree_head_count = '起始页数'
        tree_head_control = '预留'
        table_data = [
            ("South Island, New Zealand", 1, 1),
            ("Paris", 1,2),
            ("Bora Bora", 1, 3),
            ("Maui", 1, 4),
            ("Tahiti", 1, 5),
        ]
        # 定义列表格式
        self.ttframe.pack(pady=5, fill=X, side=TOP)
        self.tv = tk.Treeview(master=self.ttframe, columns=[0, 1, 2, 3], show=HEADINGS, height=10)
        self.tv.heading(0, text=tree_index)
        self.tv.heading(1, text=tree_head_root)
        self.tv.heading(2, text=tree_head_count)
        self.tv.heading(3, text=tree_head_control)
        self.tv.column(0, width=50, anchor='center')
        self.tv.column(1, width=300, anchor='w')
        self.tv.column(2, width=50, anchor='center')
        self.tv.column(3, width=120, anchor='w')
        self.tv.pack()
        self.tv.bind('<ButtonRelease-1>', self.selectItem)
        self.tv.bind('<Double-1>', self.open_Unzip_dir)
        # 修改起始页数
        setUppage = tk.Frame(self.conframe)
        setUppage.pack(side=LEFT, padx=45)
        label_page = tk.Label(setUppage, text='设置起始页数:')
        label_page.pack(pady=10, anchor='nw', side=LEFT)
        self.page_Editer = tk.Entry(setUppage, width=4, )
        self.page_Editer.pack(padx=10, pady=10, anchor='nw', side=RIGHT)
        self.page_Editer.bind('<Return>', self.updateItem)

    def fill_data(self):
        # 添加文件到列表中
        filenames = unziper.fill_data()
        self.f_paths = []
        self.file_datas.clear()
        # 点击添加文件并返回路径
        if filenames is None:
            pass
        else:
            for a, filepath in enumerate(filenames):
                self.file_datas.append((a + 1, filepath, 0))
                self.f_paths.append(filepath)
        for row in self.file_datas:
            self.tv.insert("", END, values=row)
        if len(self.file_datas) == 0:
            pass
        else:
            return self.f_paths

    def fill_remosaic_data(self):
        # 添加源文件到列表,暂时不支持多源文件添加
        roots = unziper.fill_original()
        self.files_data_ori = []
        self.files_data_real = []
        self.original_folder_names = []
        listdata = []
        for b, real_n_fake in enumerate(roots):
            for d, f_root in enumerate(real_n_fake):
                if d == 0:
                    fake_root = f_root
                    self.original_folder_name = f_root.rsplit('/', 1)[1]
                    self.original_folder_names.append(self.original_folder_name)
                    self.files_data_ori.append(fake_root)
                elif d == 1:
                    ori_list_real_root = f_root
                    self.files_data_real.append(ori_list_real_root)
        if len(self.files_data_real) != 0:
            for c, root in enumerate(self.files_data_real):
                listdata.append((c+1, root, '/', '未运行'))
        else:
            pass
        for row in listdata:
            self.rtv.insert("", END, values=row)
        # 如果列表不为空，屏蔽添加源文件按钮
        if len(listdata) == 0:
            pass
        else:
            self.btn_add_ori.destroy()

    def fill_compare_data(self):
        # 重新加载配置文件
        targetpath = reload.reloadconfig()
        filepath = ''
        default_path = configuration.unzip_path +'/unzip'
        if not os.path.exists(default_path):
            default_path = 'c:/'
        else:
            pass

        # 插入对比文件和路径
        self.file_compare = []
        for item in self.rtv.selection():
            before = list(self.rtv.item(item, 'value'))
            compare_Index = int(before[0]) - 1
            compare_Data = askdirectory(initialdir=default_path)
            if compare_Data == '':
                pass
            else:
                before[2] = str(compare_Data)
                ori_file = before[1]
                self.rtv.delete(item)
                self.rtv.insert("", compare_Index, values=before)
                self.text_com_root.set('对比路径：%s' % str(compare_Data))
                filepath = str(ori_file).rsplit('/', 1)[1]
                # 当对比路径选择完毕时，显示开始去码按钮
                self.btn_remosaic.pack(side=RIGHT, padx=10)
        target_Path = targetpath + '/' + filepath
        if not os.path.exists(target_Path):
            os.mkdir(target_Path)
        else:
            pass

    def re_Modify(self):
        # 修改缓存和输出路径
        directory1 = askdirectory()
        if directory1 == '':
            pass
        else:
            original_path = directory1 + '/original'
            target_path = directory1 + '/target'
            edit_page_path = directory1 + '/page_edit'
            if not os.path.exists(original_path):
                os.mkdir(original_path)
            if not os.path.exists(target_path):
                os.mkdir(target_path)
            if not os.path.exists(edit_page_path):
                os.mkdir(edit_page_path)
            pathKey.set('folder', 'unzip_path', edit_page_path)
            pathKey.set('folder', 'old_path', original_path)
            pathKey.set('folder', 'target_path', target_path)

        with open('config.ini', 'w', encoding='utf-8') as f:
            pathKey.write(f)

    def selectItem(self, event):
        # 选择图片起始页的列表
        self.page_Editer.delete(0, 'end')
        # 展示文件名信息
        self.labelNow.destroy()
        self.labelNow = tk.Label(self.frame_listbox, textvariable=self.text_file, wraplength=500, justify='left')
        for item in self.tv.selection():
            self.item_text = self.tv.item(item, 'value')
            self.page_Editer.insert(0, self.item_text[2])
            filename_Now = self.item_text[1]
            now = filename_Now.rsplit('/', 1)[1]
            self.text_file.set('当前文件名：%s' % now)
            self.labelNow.pack(anchor='sw', fill=X, side=BOTTOM)

    def selectItemremosaic(self, event):
        # 选择去码的列表
        for item in self.rtv.selection():
            item_text_re = self.rtv.item(item, 'value')
            # 更新展示当前路径和对比路径
            self.remosaic_Index = item_text_re[0]
            # 期望展示目录名称（并非解压的目录）
            real_root = self.files_data_ori[int(self.remosaic_Index)-1]
            try:
                root_com = item_text_re[2]
            except:
                root_com = '/'
            self.text_com_root.set('对比路径：%s' % root_com)
            self.text_ori_root.set('源路径：%s' % real_root)
            self.compare_root_r.pack(anchor='sw', fill=X, side=BOTTOM)
            self.original_root_r.pack(anchor='sw', fill=X, side=BOTTOM)
            if root_com == '/':
                self.btn_unable_add_com.destroy()
                self.btn_add_ori.destroy()
                self.btn_add_com.pack(side=RIGHT, padx=10)
                self.btn_add_com.pack(side=RIGHT, padx=10)



    def updateItem(self, event):
        # 更新列表中的起始页数
        for item in self.tv.selection():
            before = list(self.tv.item(item, 'value'))
            page_Now = self.page_Editer.get()
            before[2] = page_Now
            indexnow = int(before[0]) - 1
            self.tv.delete(item)
            self.tv.insert("", indexnow, values=before)
            # 根据页数设置修改文件名
            f_path = self.f_paths[indexnow]
            for dir, dir_abs, files in os.walk(f_path):
                for i, file in enumerate(files):
                    if file.endswith('.png') or file.endswith('.jpg'):
                        old_p = os.path.join(dir, file)
                        ftype = file.rsplit('.', 1)[1]
                        newindex = i + int(page_Now)
                        newname = str(newindex) + 'a.' + ftype
                        new_p = os.path.join(dir, newname)
                        os.rename(old_p, new_p)

    def emptyList(self):
        # 清空列表
        x = self.tv.get_children()
        if str(x) != '()':
            for item in x:
                self.tv.delete(item)
            # 删除缓存文件
            unziper.del_pic_handle_cache()
            self.btn_add.destroy()
            self.btn_unable_add.destroy()
            self.btn_add = tk.Button(self.btns, text='添加文件', bootstyle=(SUCCESS, OUTLINE), command=self.fill_data)
            # 添加文件按钮重见天日
            self.btn_add.pack(side=RIGHT, padx=10)
            # 摧毁路径显示
            self.labelNow.destroy()
            # 清空输入栏
            self.page_Editer.delete(0, 'end')
        else:
            pass

    def open_Original(self, event):
        # 打开临时处理路径（源文件）
        for item in self.rtv.selection():
            item_text_re = self.rtv.item(item, 'value')
            root_ori = item_text_re[1]
            os.startfile(root_ori)

    def open_Compare(self, event):
        # 打开对比路径
        for item in self.rtv.selection():
            item_text_re = self.rtv.item(item, 'value')
            compare_text = item_text_re[2]
            if compare_text == '/':
                pass
            else:
                os.startfile(compare_text)

    def open_Target(self, event):
        # 打开目标路径
        targetpath = reload.reloadconfig()
        for item in self.rtv.selection():
            item_text_re = self.rtv.item(item, 'value')
            list_index = int(item_text_re[0])-1
            filename = self.original_folder_names[list_index].rsplit('.', 1)[0]
            target_Path = targetpath + '/' + filename
            os.startfile(target_Path)

    def open_Unzip_dir(self, event):
        # 打开目标路径
        for item in self.tv.selection():
            self.item_text_unzip = self.tv.item(item, 'value')
            root_ori = self.item_text_unzip[1]
            os.startfile(root_ori)


    def start_Remosiac(self):
        targetpath = reload.reloadconfig()
        for item in self.rtv.selection():
            remosaic_data= self.rtv.item(item, 'value')
            if remosaic_data[2] == '/':
                continue
            else:
                # 从列表获取源路径和对比路径
                remosaic_index = int(remosaic_data[0])
                remosaic_ori = self.files_data_real[remosaic_index-1]
                remosaic_com = remosaic_data[2]
                # 计算出解压路径
                filepath = str(remosaic_ori).rsplit('/', 1)[1]
                realname = self.original_folder_names[remosaic_index-1]

                target_Path = targetpath + '/' + filepath
                real_path = targetpath + '/' + realname.rsplit('.', 1)[0]
                # print(remosaic_ori)
                # print(remosaic_com)
                # print(real_path)
                remove_mosaic.GUI_use_Remosaic(remosaic_ori, remosaic_com, target_Path)
                os.rename(target_Path, real_path)

    def pic_handle(self):
        self.text.set('当前图片路径：%s' % filepath)
        self.text1.set('当前存储路径：%s' % targetpath)
        labelinfo = tk.Label(self.frame_l, text='✳本操作会遍历目录')
        labelinfo.pack()
        # 按钮们
        btnwords = [('点击缩放(原始比例)', 'PRIMARY', self.resize_pic),
                    ('点击缩放(指定尺寸)', 'PRIMARY', self.resize_ksk),
                    ('修改图片路径', '(PRIMARY, OUTLINE)', self.change_pic_Path),
                    ('修改存储路径', '(PRIMARY, OUTLINE)', self.change_save_Path),
                    ('修改宽高设置', '(WARNING, OUTLINE)', self.input_size)]
        for bwords, how in enumerate(btnwords):
            bt = tk.Button(self.frame_l, text=how[0], width=15, bootstyle=how[1], command=how[2])
            bt.pack(pady=10)
        # 宽高输入栏
        labelwidth = tk.Label(self.frame_enter, text='设置宽高:')
        labelwidth.pack(anchor='center', side=LEFT, padx=2)
        self.size_Enter_w = tk.Entry(self.frame_enter, width=4, )
        self.size_Enter_w.insert(0, config_w)
        self.size_Enter_w.pack(side=LEFT, padx=2)
        labelwidth = tk.Label(self.frame_enter, text='x')
        labelwidth.pack(anchor='center', side=LEFT, padx=2)
        self.size_Enter_h = tk.Entry(self.frame_enter, width=4, )
        self.size_Enter_h.insert(0, config_h)
        self.size_Enter_h.pack(anchor='center', side=RIGHT, padx=2)

    def del_cache(self):
        # 删除去码文件缓存
        ori_dir = configuration.old_path
        # 去码文件的源文件解压缓存
        ori_cache = ori_dir + '/unzip'
        shutil.rmtree(ori_cache)
        unziper.del_pic_handle_cache()


if __name__ == '__main__':
    root = tk.Window()
    myGUI = GUI(root)
