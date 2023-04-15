import ttkbootstrap as tk
import shutil
from utils.resize import multi
from utils.resize import multi_ksk
from ttkbootstrap.constants import *
from tkinter.filedialog import (askopenfilename,
                                    askopenfilenames,
                                    askdirectory,
                                    asksaveasfilename)
import main
import os
from utils import configuration
from configparser import ConfigParser
from utils import unziper
filepath = configuration.filepath
targetpath = configuration.targetpath
config_w = configuration.config_w
config_h = configuration.config_h
pic_Path = main.pic_path
save_Path = main.save_path
pathKey = configuration.pathKey

class Window:
    button_list = []
    object_list = []
    def __init__(self):
        '''创建窗口和frame'''
        self.window = tk.Window()
        self.window.title('PDF2IMG')
        self.window.geometry('960x720')
        # 定义欢迎界面的frame
        self.frame_c = tk.Frame(self.window)
        self.frame_c.place(x=460, y=350, anchor='center')
        self.frame_b = tk.Frame(self.frame_c)
        self.frame_b.pack(anchor='center', side='top')
        # 新建标签选项卡
        # 定义按钮操作栏的frame
        self.framebtn = tk.Labelframe(self.window, text='图片缩放处理')
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
        self.frame_listbox = tk.Frame(self.window)
        self.ttframe = tk.LabelFrame(self.frame_listbox, text='修改图片起始页数')
        self.conframe = tk.Frame(self.ttframe)
        self.conframe.pack(anchor='center', side=BOTTOM, expand=True)
        # 定义想要添加起始页数的文件
        self.file_datas = []
        self.text_file = tk.StringVar()
        # 去码操作区
        self.remosaic = tk.Frame(self.window)
        self.remosaic.pack()
        self.remosaic_Label = tk.Labelframe(self.window, text='去马赛克处理')



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
        self.framebtn.pack(anchor='nw', padx=60, pady=100)
        self.frame_listbox.place(x=370, y=100)
        self.remosaic_Label.place(x=360, y=800)
        self.pic_handle()
        self.file_handle()

    def file_handle(self):
        # 按钮们
        self.file_form()
        self.btns = tk.Frame(self.conframe)
        self.btns.pack(side=RIGHT, expand=True, padx=10)
        btn_del = tk.Button(self.btns, text='清空列表', bootstyle=(DANGER, OUTLINE), command=self.emptyList)
        btn_del.pack(side=RIGHT, padx=10)
        self.btn_add = tk.Button(self.btns, text='添加文件', bootstyle=(SUCCESS, OUTLINE), command=self.fill_data)
        self.btn_add.pack(side=RIGHT, padx=10)
        # btnwords = [('清空列表', '(DANGER, OUTLINE)', self.emptyList),
        #             ('添加文件', '(SUCCESS, OUTLINE)', self.fill_data)]
        # for bwords, how in enumerate(btnwords):
        #     bt = tk.Button(btns, text=how[0], bootstyle=how[1], command=how[2])
        #     bt.pack(side=RIGHT, padx=10)

    def remosaic(self):
        btn_remosaic = tk.Button(master=self.remosaic_Label, text='先放个按钮在这里')
        btn_remosaic.pack()

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
        # 修改起始页数
        setUppage = tk.Frame(self.conframe)
        setUppage.pack(side=LEFT, padx=45)
        label_page = tk.Label(setUppage, text='设置起始页数:')
        label_page.pack(pady=10, anchor='nw', side=LEFT)
        self.page_Editer = tk.Entry(setUppage, width=4)
        self.page_Editer.pack(padx=10, pady=10, anchor='nw', side=RIGHT)
        self.page_Editer.bind('<Return>', self.updateItem)
        self.labelNow = tk.Label(self.frame_listbox, textvariable=self.text_file, wraplength=500, justify='left')

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
        self.btn_add.destroy()
        self.btn_add = tk.Button(self.btns, text='添加文件', bootstyle=(SECONDARY, OUTLINE))
        self.btn_add.pack(side=RIGHT, padx=10)
        return self.f_paths

    def selectItem(self, event):
        self.page_Editer.delete(0, 'end')
        for item in self.tv.selection():
            self.item_text = self.tv.item(item, 'value')
            self.page_Editer.insert(0, self.item_text[2])
            filename_Now = self.item_text[1]
            now = filename_Now.rsplit('/', 1)[1]
            self.text_file.set('当前文件名：%s' % now)
            self.labelNow.pack(anchor='sw', fill=X, side=BOTTOM)

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
                print(dir, dir_abs, files)
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
        for item in x:
            self.tv.delete(item)
        # 删除缓存文件
        unziper.del_cache()
        self.btn_add.destroy()
        self.btn_add = tk.Button(self.btns, text='添加文件', bootstyle=(SUCCESS, OUTLINE), command=self.fill_data)
        self.btn_add.pack(side=RIGHT, padx=10)


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
        self.size_Enter_w = tk.Entry(self.frame_enter, width=4)
        self.size_Enter_w.insert(0, config_w)
        self.size_Enter_w.pack(side=LEFT, padx=2)
        labelwidth = tk.Label(self.frame_enter, text='x')
        labelwidth.pack(anchor='center', side=LEFT, padx=2)
        self.size_Enter_h = tk.Entry(self.frame_enter, width=4, )
        self.size_Enter_h.insert(0, config_h)
        self.size_Enter_h.pack(anchor='center', side=RIGHT, padx=2)

    def new_button(self):
        '''创建展示按钮'''"开始检测和显示结果可在此处新添加tk.button"
        self.startbtn = tk.Button(self.frame_b, text='欢迎使用', width=10, bootstyle=PRIMARY,
                  command=self.show_info).pack()

    def del_cache(self):
        unziper.del_cache()

    def run(self):
        '''主程序调用'''
        self.window.mainloop()
        try:
            self.window.protocol('WM_DELETE_WINDOW', self.del_cache())
        except:
            print('程序已退出')


if __name__ == '__main__':
    w = Window()
    w.new_button()
    w.run()