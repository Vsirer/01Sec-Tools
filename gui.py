#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Copyright (c) 2017-2017 01 Security Team
"""

import os
from tkinter import *
from tkinter import ttk, Canvas, filedialog
import tkinter.messagebox
# from idlelib.TreeWidget import TreeItem,TreeNode,FileTreeItem

from plugin.util import *
from plugin.portscan import *
from plugin.chatclient import *
from plugin.crack import *
from plugin.dir import *
from plugin.webvuln import *
from plugin.code import *


# 主类
class MainWindows:
    def __init__(self):
        self.root = Tk()
        self.root.title("01Sec Tools v0.1.1")
        # self.root.attributes('-alpha', 0.8)
        # self.root.geometry("580x450")
        # self.root.iconbitmap('favicon.ico')

        '''
        menu
        '''
        # self.menuBar = Menu(self.root)
        # self.menu_set = Menu(self.menuBar,tearoff=0)

        '''
        tab
        '''
        tabControl = ttk.Notebook(self.root)
        self.tab_web = Frame(tabControl)
        self.tab_dir = Frame(tabControl)
        self.tab_port = Frame(tabControl)
        # self.tab_vuln = Frame(tabControl)
        self.tab_crack = Frame(tabControl)
        self.tab_code = Frame(tabControl)
        self.tab_chat = Frame(tabControl)
        # self.tab_music = Frame(tabControl)
        self.tab_explain = Frame(tabControl)

        tabControl.add(self.tab_web, text='漏洞测试')
        tabControl.add(self.tab_dir, text='目录收集')
        tabControl.add(self.tab_port, text='端口扫描')
        # tabControl.add(self.tab_vuln,text='VulnList')
        tabControl.add(self.tab_crack, text='服务爆破')
        tabControl.add(self.tab_code, text='编码解码')
        tabControl.add(self.tab_chat, text='即时通讯')
        # tabControl.add(self.tab_music, text='Music')
        tabControl.add(self.tab_explain, text='说明')
        tabControl.pack(expand=1, fill='both')

        self.show_webvuln()
        self.show_dir()
        self.show_portscan()
        self.show_crack()
        self.show_code()
        self.show_chat()
        self.show_explain()

        # self.root.config(menu=self.menuBar)
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.mainloop()

    def close(self):
        if tkinter.messagebox.askyesno("01Sec Tools", "是否要退出当前程序？"):
            self.root.quit()

    '''
    PortScan
    '''

    def show_portscan(self):
        frame_port = LabelFrame(self.tab_port, text='01Sec')
        frame_port.pack(expand=1, fill='both')

        fm1 = Frame(frame_port)  # 按钮文本框容器
        Label(fm1, text='目标IP:').pack(side=LEFT, expand=1, fill=BOTH)
        ipaddrs = StringVar()
        entry_ip = Entry(fm1, textvariable=ipaddrs).pack(side=LEFT, expand=1, fill=BOTH)
        Label(fm1, text='端口:').pack(side=LEFT, expand=1, fill=BOTH)
        ports = StringVar()
        entry_port = Entry(fm1, textvariable=ports).pack(side=LEFT, expand=1, fill=BOTH)
        ports.set('1-1024')
        Label(fm1, text='线程:').pack(side=LEFT, expand=1, fill=BOTH)
        threads = StringVar()
        entry_thread = Entry(fm1, textvariable=threads).pack(side=LEFT, expand=1, fill=BOTH)
        threads.set(1)

        # 扫描按钮绑定事件
        btn_port = Button(fm1, text='扫描',
                          command=lambda: scanstart(ipaddrs.get(), '1-1024' if ports.get() is '' else ports.get(),
                                                    port_result, 1 if threads.get() is '' else int(threads.get()),
                                                    btn_port, pbar_port))
        btn_port.pack(side=LEFT, expand=1)
        # btn_port.bind('<ButtonRelease>',
        #               lambda x: scanstart(x, ipaddrs.get(), '1-1024' if ports.get() is '' else ports.get(),
        #                                   port_result, 1 if threads.get() is '' else int(threads.get())))

        btn_port_pause = Button(fm1, text='暂停')
        btn_port_pause.pack(side=LEFT, expand=1)
        btn_port_pause.bind('<ButtonRelease>', lambda x: pause_port(x, btn_port_pause))

        btn_port_stop = Button(fm1, text='停止')
        btn_port_stop.pack(side=LEFT, expand=1)
        btn_port_stop.bind('<ButtonRelease>', lambda x: stop_port(x, btn_port, btn_port_pause))

        fm1.pack(side=TOP, fill=BOTH, pady=5)

        fm2 = Frame(frame_port)
        fm2.pack(side=TOP, expand=1, fill=BOTH)
        # 显示扫描结果
        port_result = Text(fm2, bg='black', fg='green', insertbackground='green', selectbackground='green',
                           insertwidth=3)
        # 滚动条
        ysb_port = ttk.Scrollbar(fm2, orient='vertical', command=port_result.yview)
        ysb_port.pack(side=RIGHT, fill=Y)
        port_result.configure(yscroll=ysb_port.set)
        port_result.pack(side=TOP, expand=1, fill=BOTH)

        # 最下面进度条
        pbar_port = ttk.Progressbar(frame_port, mode="determinate")
        pbar_port.pack(side=TOP, expand=0, fill=X)

        '''
        Dir
        '''

    '''
    Code
    '''

    def show_code(self):
        frame_code = LabelFrame(self.tab_code, text='01Sec')
        frame_code.pack(expand=1, fill='both')

        text_top = Text(frame_code, height=1, bg='black', fg='green', insertbackground='green',
                        selectbackground='green',
                        insertwidth=3)
        text_top.pack(side=TOP, expand=1, fill=BOTH)
        fm1 = Frame(frame_code)
        fm1.pack(side=TOP, expand=0, fill=Y)
        type_code = StringVar()
        cbox_type = ttk.Combobox(fm1, textvariable=type_code, width=7)
        cbox_type['values'] = ('...', 'url', 'base16', 'base32', 'base64', 'base85', 'unicode', 'hex')
        cbox_type.current(0)
        cbox_type.pack(side=LEFT, padx=10, pady=5, expand=1, fill=BOTH)

        btn_encode = Button(fm1, text='编码')
        btn_encode.pack(side=LEFT, padx=10, pady=5, expand=1, fill=BOTH)
        btn_encode.bind('<ButtonRelease>', lambda x: encode(x, type_code.get(), text_top, text_bottom))

        btn_decode = Button(fm1, text='解码')
        btn_decode.pack(side=LEFT, padx=10, pady=5, expand=1, fill=BOTH)
        btn_decode.bind('<ButtonRelease>', lambda x: decode(x, type_code.get(), text_top, text_bottom))

        text_bottom = Text(frame_code, height=1, bg='black', fg='green', insertbackground='green',
                           selectbackground='green',
                           insertwidth=3)
        text_bottom.pack(side=TOP, expand=1, fill=BOTH)

    '''
    Dir
    '''

    def show_dir(self):
        frame_dir = LabelFrame(self.tab_dir, text='01Sec')
        frame_dir.pack(expand=1, fill='both')

        # 上层
        fm1 = Frame(frame_dir)
        fm1.pack(side=TOP, expand=0)

        # 下层
        fm2 = Frame(frame_dir)
        fm2.pack(side=TOP, expand=1, fill=BOTH)

        # 最下面进度条
        pbar_crack = ttk.Progressbar(frame_dir, mode="determinate")
        pbar_crack.pack(side=TOP, expand=0, fill=X)

        # 上层控件
        Label(fm1, text='目标域名:').pack(side=LEFT, expand=1, fill=BOTH)
        domain = StringVar()
        entry_ip = Entry(fm1, textvariable=domain).pack(side=LEFT, expand=1, fill=BOTH)
        Label(fm1, text='目录字典:').pack(side=LEFT, expand=1, fill=BOTH)
        dirfile = StringVar()
        entry_dict = Entry(fm1, textvariable=dirfile)
        entry_dict.pack(side=LEFT, expand=1, fill=BOTH)
        dirfile.set(os.getcwd() + '/exploit/dir/dir.txt')
        entry_dict.bind('<ButtonRelease>', lambda x: choose_file(x, dirfile))

        # 下层分左右两边
        frame_left = LabelFrame(fm2, text='目录爆破')
        frame_left.pack(side=LEFT, expand=1, fill=BOTH)
        frame_right = LabelFrame(fm2, text='目录爬取')
        frame_right.pack(side=LEFT, expand=1, fill=BOTH)

        fm_left_top = Frame(frame_left)
        fm_left_top.pack(side=TOP, expand=0, fill=BOTH, pady=5)

        Label(fm_left_top, text='线程:').pack(side=LEFT, expand=1, fill=BOTH)
        threads_left = StringVar()
        entry_threads_left = Entry(fm_left_top, textvariable=threads_left, width=1).pack(side=LEFT, expand=1, fill=X)
        threads_left.set(1)
        Label(fm_left_top, text='超时:').pack(side=LEFT, expand=1, fill=BOTH)
        time_left = StringVar()
        entry_time_left = Entry(fm_left_top, textvariable=time_left, width=1).pack(side=LEFT, expand=1, fill=X)
        time_left.set(3)
        btn_crack = Button(fm_left_top, text='爆破', command=lambda: dir_crack(domain.get(), int(threads_left.get()),
                                                                             int(time_left.get()),
                                                                             dirfile.get(),
                                                                             tv_crack,
                                                                             btn_crack, pbar_crack))
        btn_crack.pack(side=LEFT, expand=1)
        # btn_crack.bind('<ButtonRelease>',
        #                lambda x: dir_crack(x, domain.get(), int(threads_left.get()), int(time_left.get()),
        #                                    dirfile.get(),
        #                                    tv_crack,btn_crack))

        btn_crack_pause = Button(fm_left_top, text='暂停')
        btn_crack_pause.pack(side=LEFT, expand=1)
        btn_crack_pause.bind('<ButtonRelease>', lambda x: pause_crack(x, btn_crack_pause))

        btn_crack_stop = Button(fm_left_top, text='停止')
        btn_crack_stop.pack(side=LEFT, expand=1)
        btn_crack_stop.bind('<ButtonRelease>', lambda x: stop_crack(x, btn_crack, btn_crack_pause))

        fm_right_top = Frame(frame_right)
        fm_right_top.pack(side=TOP, expand=0, fill=BOTH, pady=5)

        Label(fm_right_top, text='线程:').pack(side=LEFT, expand=1, fill=BOTH)
        threads_right = StringVar()
        entry_threads_right = Entry(fm_right_top, textvariable=threads_right, width=1).pack(side=LEFT, expand=1, fill=X)
        threads_right.set(1)
        Label(fm_right_top, text='超时:').pack(side=LEFT, expand=1, fill=BOTH)
        time_right = StringVar()
        entry_time_right = Entry(fm_right_top, textvariable=time_right, width=1).pack(side=LEFT, expand=1, fill=X)
        time_right.set(3)
        btn_sprider = Button(fm_right_top, text='爬取',
                             command=lambda: dir_sprider(domain.get(), int(threads_right.get()), int(time_right.get()),
                                                         tv_sprider, btn_sprider))
        btn_sprider.pack(side=LEFT, expand=1)

        btn_sprider_pause = Button(fm_right_top, text='暂停')
        btn_sprider_pause.pack(side=LEFT, expand=1)
        btn_sprider_pause.bind('<ButtonRelease>', lambda x: pause_sprider(x, btn_sprider_pause))

        btn_sprider_stop = Button(fm_right_top, text='停止')
        btn_sprider_stop.pack(side=LEFT, expand=1)
        btn_sprider_stop.bind('<ButtonRelease>', lambda x: stop_sprider(x, btn_sprider, btn_sprider_pause))

        tv_crack = ttk.Treeview(frame_left, show="headings", columns=('url', 'resp'))
        # 滚动条
        ysb_crack = ttk.Scrollbar(frame_left, orient='vertical', command=tv_crack.yview)
        ysb_crack.pack(side=RIGHT, fill=Y)
        tv_crack.configure(yscroll=ysb_crack.set)
        tv_crack.column('url', width=320, anchor=W)
        tv_crack.column('resp', width=10, anchor=CENTER)
        tv_crack.heading('url', text='url')
        tv_crack.heading('resp', text='resp')
        tv_crack.pack(side=TOP, expand=1, fill=BOTH)
        tv_crack.bind('<Double-Button-1>', lambda x: row_click(x, tv_crack))

        # c = a.get_children()
        # for i in range(len(c)):
        #     a.item(c[i],tags=('ccc'))
        # a.tag_configure('ccc',background='black', foreground='green')

        # text_scan = Text(frame_left, width=50, bg='black', fg='green', insertbackground='green', selectbackground='green',
        #                    insertwidth=3)
        # text_scan.pack(side=TOP, expand=1, fill=BOTH)
        #
        # text_sprider = Text(frame_right,width=50, bg='black', fg='green', insertbackground='green', selectbackground='green',
        #                  insertwidth=3)
        # text_sprider.pack(side=TOP, expand=1, fill=BOTH)


        # lb_crack = Listbox(frame_left, bg='black', fg='green', selectbackground='green')
        # lb_crack.insert(END, 'aaa')
        # lb_crack.insert(END, 'bbb')
        # lb_crack.pack(side=TOP, expand=1,fill=BOTH)

        # lb_sprider = Listbox(frame_right, bg='black', fg='green', selectbackground='green')
        # lb_sprider.insert(END, 'aaaaaaaaaaaa\t\t\t403')
        # lb_sprider.insert(END, 'bbb\t\t\t200')
        # lb_sprider.pack(side=TOP, expand=1, fill=BOTH)


        tv_sprider = ttk.Treeview(frame_right, show="headings", columns=('url', 'resp'))
        # 滚动条
        ysb_sprider = ttk.Scrollbar(frame_right, orient='vertical', command=tv_sprider.yview)
        ysb_sprider.pack(side=RIGHT, fill=Y)
        tv_sprider.configure(yscroll=ysb_sprider.set)
        tv_sprider.column('url', width=320, anchor=W)
        tv_sprider.column('resp', width=10, anchor=CENTER)
        tv_sprider.heading('url', text='url')
        tv_sprider.heading('resp', text='resp')
        tv_sprider.pack(side=TOP, expand=1, fill=BOTH)
        tv_sprider.bind('<Double-Button-1>', lambda x: row_click(x, tv_sprider))

    '''
    Crack
    '''

    def show_crack(self):
        frame_crack = LabelFrame(self.tab_crack, text='01Sec')
        frame_crack.pack(expand=1, fill='both')

        # 最外层 第一层
        # 输入框 按钮控件整体布局容器
        fm1 = Frame(frame_crack)

        # 第二层
        # 下拉框布局容器 左
        fm1_1 = Frame(fm1, padx=10)
        fm1_1.pack(side=LEFT, expand=0, fill=BOTH)

        # 输入框布局容器 中
        fm1_2 = Frame(fm1)
        fm1_2.pack(side=LEFT, expand=1, fill=BOTH)

        # 按钮布局容器 右
        fm1_3 = Frame(fm1, padx=6)
        fm1_3.pack(side=LEFT, expand=0, fill=BOTH)

        # 下拉框
        type = StringVar()
        cbox_type = ttk.Combobox(fm1_1, textvariable=type, width=5)
        cbox_type['values'] = ('...', 'ssh', 'rdp', 'ftp', 'mysql', 'mssql', 'telnet', 'postgresql')
        cbox_type.current(0)
        cbox_type.pack(side=LEFT, expand=1, fill=X)
        cbox_type.bind('<<ComboboxSelected>>', lambda x: change_cbox(x, type.get(), ports))

        # 第三层 第二层里在进行布局
        # 输入框容器里在将控件整体分为两行
        # 第一行容器
        fm1_2_1 = Frame(fm1_2)
        fm1_2_1.pack(side=TOP, expand=1, fill=BOTH)
        Label(fm1_2_1, text='目标IP:').pack(side=LEFT)
        ipaddrs = StringVar()
        entry_ip = Entry(fm1_2_1, textvariable=ipaddrs).pack(side=LEFT, expand=1, fill=BOTH)
        Label(fm1_2_1, text='端口:').pack(side=LEFT)
        ports = StringVar()
        entry_port = Entry(fm1_2_1, textvariable=ports, width=1).pack(side=LEFT, expand=1, fill=BOTH)
        Label(fm1_2_1, text='线程:').pack(side=LEFT)
        threads = StringVar()
        entry_thread = Entry(fm1_2_1, textvariable=threads, width=1).pack(side=LEFT, expand=1, fill=BOTH)
        threads.set(1)

        # 第二行容器
        fm1_2_2 = Frame(fm1_2)
        fm1_2_2.pack(side=TOP, expand=1, fill=BOTH, pady=5)
        Label(fm1_2_2, text='账号:').pack(side=LEFT)
        name = StringVar()
        entry_name = Entry(fm1_2_2, textvariable=name).pack(side=LEFT, expand=1, fill=BOTH)
        Label(fm1_2_2, text='密码字典:').pack(side=LEFT)
        filename = StringVar()
        entry_file = Entry(fm1_2_2, textvariable=filename)
        entry_file.pack(side=LEFT, expand=1, fill=BOTH)
        filename.set(os.getcwd() + '/exploit/dict/default.txt')
        entry_file.bind('<ButtonRelease>', lambda x: choose_file(x, filename))

        # 按钮绑定事件
        btn_crack = Button(fm1_3, text='爆破',
                           command=lambda: crack_port(type.get(), ipaddrs.get(), ports.get(), int(threads.get()),
                                                      name.get(),
                                                      filename.get(), btn_crack, crack_result, pbar_crack))
        btn_crack.pack(side=LEFT, padx=3, expand=1)
        # btn_crack.pack(side=TOP, expand=1)
        # btn_crack.bind('<ButtonRelease>',
        #                lambda x: crack_port(x, type.get(), ipaddrs.get(), ports.get(), int(threads.get()), name.get(),
        #                                     filename.get(), crack_result,pbar_crack))

        btn_crack_pause = Button(fm1_3, text='暂停')
        btn_crack_pause.pack(side=LEFT, padx=3, expand=1)
        btn_crack_pause.bind('<ButtonRelease>', lambda x: pause_port_crack(x, btn_crack_pause))

        btn_crack_stop = Button(fm1_3, text='停止')
        btn_crack_stop.pack(side=LEFT, padx=3, expand=1)
        btn_crack_stop.bind('<ButtonRelease>', lambda x: stop_port_crack(x, btn_crack, btn_crack_pause))

        fm1.pack(side=TOP, expand=0, fill=BOTH)

        # 显示扫描结果
        crack_result = Text(frame_crack, bg='black', fg='green', insertbackground='green', selectbackground='green',
                            insertwidth=3)
        crack_result.pack(side=TOP, expand=1, fill=BOTH)

        # 最下面进度条
        pbar_crack = ttk.Progressbar(frame_crack, mode="determinate")
        pbar_crack.pack(side=TOP, expand=0, fill=X)

    '''
    WebVuln
    '''

    def show_webvuln(self):
        frame_web = LabelFrame(self.tab_web, text='01Sec')
        frame_web.pack(expand=1, fill=BOTH)

        '''
        canvas_web = Canvas(frame_web,width=200)
        canvas_web.pack(side=TOP, expand=0, fill=BOTH)
        item_web = FileTreeItem(os.curdir+'/exp')
        node_web = TreeNode(canvas_web,None,item_web)
        node_web.update()
        node_web.expand()
        canvas_web.bind('<ButtonRelease>', lambda x: self.test_click(x, item_web))
        '''

        # 左边布局容器 目录树
        fm1 = Frame(frame_web)
        fm1.pack(side=LEFT, expand=0, fill=BOTH)
        tree_web = ttk.Treeview(fm1)
        # 滚动条
        ysb_tree = ttk.Scrollbar(fm1, orient='vertical', command=tree_web.yview)
        ysb_tree.pack(side=RIGHT, fill=Y)
        # xsb = ttk.Scrollbar(fm1, orient='horizontal', command=tree_web.xview)
        # xsb.pack(side=BOTTOM,fill=X)
        tree_web.configure(yscroll=ysb_tree.set)  # , xscroll=xsb.set
        tree_web.heading('#0', text='Vnlu', anchor=CENTER)
        # 根结点
        loadfile = 'exploit/web'
        root_node = tree_web.insert('', END, 'web', text='web', open=True)
        # 调用方法：获取目录并显示
        get_dir(tree_web, root_node, loadfile)
        # 遍历子节点 默认展开
        for i in tree_web.get_children():
            tree_web.item(i, open=True)
        # 布局
        tree_web.pack(side=LEFT, expand=0, fill=BOTH)
        # 绑定事件
        tree_web.bind('<ButtonRelease>', lambda x: load_exp(x, tree_web, name, cms, text_path, text_post, method))

        # 配置文件对应的设置控件 中间布局控件
        fm2 = Frame(frame_web)
        fm2.pack(side=LEFT, expand=1, fill=BOTH)

        # 第一行 设置exp名称和所属cms／框架
        fm2_1 = Frame(fm2)
        fm2_1.pack(side=TOP, expand=1, fill=X, padx=5)
        # fm2_1.pack(side=TOP, padx=5, pady=3, expand=0, fill=BOTH)
        Label(fm2_1, text='名称:').pack(side=LEFT)
        name = StringVar()
        entry_name = Entry(fm2_1, width=16, textvariable=name).pack(side=LEFT, expand=1, fill=BOTH)
        Label(fm2_1, text='模块:').pack(side=LEFT)
        cms = StringVar()
        entry_cms = Entry(fm2_1, width=16, textvariable=cms).pack(side=LEFT, expand=1, fill=BOTH)

        # 第二行 设置攻击地址
        fm2_2 = Frame(fm2)
        fm2_2.pack(side=TOP, expand=1, fill=X, padx=5)
        # fm2_2.pack(side=TOP, padx=5, pady=3, expand=0, fill=BOTH)
        Label(fm2_2, text='地址:').pack(side=LEFT)
        url = StringVar()
        entry_url = Entry(fm2_2, textvariable=url).pack(side=LEFT, expand=1, fill=BOTH)

        # 第三行 设置路径+get参数
        fm2_3 = Frame(fm2)
        fm2_3.pack(side=TOP, expand=1, fill=X, padx=5)
        # fm2_3.pack(side=TOP, padx=5, pady=3, expand=0, fill=BOTH)
        Label(fm2_3, text='路径:').pack(side=LEFT)
        # path = StringVar()
        # entry_path = Entry(fm2_3, textvariable=path).pack(side=LEFT, expand=1, fill=BOTH)
        text_path = Text(fm2_3, width=1, height=4)
        text_path.pack(side=LEFT, expand=1, fill=BOTH)

        # 第四行 设置post参数
        fm2_4 = Frame(fm2)
        fm2_4.pack(side=TOP, expand=1, fill=X, padx=5)
        # fm2_4.pack(side=TOP, padx=5, pady=3, expand=0, fill=BOTH)
        Label(fm2_4, text='参数:').pack(side=LEFT)
        text_post = Text(fm2_4, width=1, height=8)
        text_post.pack(side=LEFT, expand=1, fill=BOTH)

        # 第五行 设置cookie
        fm2_5 = Frame(fm2)
        fm2_5.pack(side=TOP, expand=1, fill=X, padx=5)
        # fm2_5.pack(side=TOP, padx=5, pady=3, expand=0, fill=BOTH)
        Label(fm2_5, text='身份:').pack(side=LEFT)
        text_cookie = Text(fm2_5, width=1, height=4)
        text_cookie.pack(side=LEFT, expand=1, fill=BOTH)

        # 第六行
        fm2_6 = Frame(fm2)
        fm2_6.pack(side=TOP, expand=1, fill=X, padx=5)
        # fm2_6.pack(side=TOP, expand=1, fill=X)
        Label(fm2_6, text='请求方式:').pack(side=LEFT)
        # 下拉框 请求方式
        method = StringVar()
        cbox_method = ttk.Combobox(fm2_6, textvariable=method, width=1)
        cbox_method['values'] = ('GET', 'POST')
        cbox_method.pack(side=LEFT, expand=1, fill=BOTH)
        cbox_method.current(0)
        Label(fm2_6, text='编码方式:').pack(side=LEFT)
        # 下拉框 编码
        code = StringVar()
        cbox_code = ttk.Combobox(fm2_6, textvariable=code, width=1)
        cbox_code['values'] = ('UTF-8', 'GBK')
        cbox_code.current(0)
        cbox_code.pack(side=LEFT, expand=1, fill=BOTH)

        # 第七行 按钮
        fm2_7 = Frame(fm2)
        fm2_7.pack(side=TOP, expand=1, fill=X, padx=5)
        # fm2_7.pack(side=TOP, padx=5, pady=3, expand=0, fill=BOTH)
        # 攻击
        btn_exp = Button(fm2_7, text='测试')
        btn_exp.pack(side=LEFT, expand=1)
        btn_exp.bind("<ButtonRelease>",
                     lambda x: exploit(x, url, text_path, text_post, text_cookie, method, code, text_resp))
        # 修改当前exp
        btn_update = Button(fm2_7, text='更新')
        btn_update.pack(side=LEFT, expand=1)
        btn_update.bind("<ButtonRelease>",
                        lambda x: update(x, text_path, text_post, method))

        # 新增新exp
        btn_add = Button(fm2_7, text='新增')
        btn_add.pack(side=LEFT, expand=1)
        btn_add.bind("<ButtonRelease>",
                     lambda x: save(x, name, cms, method, text_path, text_post, tree_web, root_node, loadfile))

        # 清空控件内容
        btn_clear = Button(fm2_7, text='清空')
        btn_clear.pack(side=LEFT, expand=1)
        btn_clear.bind("<ButtonRelease>",
                       lambda x: clear(x, name, cms, url, text_path, text_post, text_cookie, method, code))

        # 右边布局控件
        fm3 = Frame(frame_web)
        fm3.pack(side=LEFT, expand=1, fill=BOTH)
        # 展示resp内容
        text_resp = Text(fm3, width=57, height=8, bg='black', fg='green', insertbackground='green',
                         selectbackground='green', insertwidth=3)
        text_resp.pack(side=LEFT, expand=1, fill=BOTH)

    '''
    def get_dir(self,tree):
        loadfile = ['exploit/web']
        while (loadfile):
            try:
                path = loadfile.pop()
                # print path
                for x in os.listdir(path):
                    if os.path.isfile(os.path.join(path, x)):
                        if '/' in path:
                            # 写到gui上
                            tree.insert(path[path.rfind('/') + 1:], END, x, text=x)
                            # 保存完整路径
                            tree.setvar(x,path+'/'+x)

                        else:
                            tree.insert(path, END, x, text=x)
                    else:
                        loadfile.append(os.path.join(path, x))
                        if '/' in path:
                            tree.insert(path[path.rfind('/') + 1:], END, x, text=x)
                        else:
                            tree.insert(path, END, x, text=x)
            except:
                pass
    '''

    # 临时测试类 后面会删掉
    # def test_click(self,event,tree_web,ttt):
    #     #value = tree_web.selection()[0]
    #     try:
    #         # 获取完整路径
    #         exp_dir = tree_web.getvar(tree_web.identify_row(event.y))
    #         # 是否为文件
    #         if os.path.isfile(exp_dir):
    #             with open(exp_dir) as f:
    #                 ttt.insert(END,f.read()+'\n')
    #     except:
    #         pass



    '''
    Chat
    '''

    def show_chat(self):
        frame_chat = LabelFrame(self.tab_chat, text='01Sec')
        frame_chat.pack(expand=1, fill='both')

        # 第一层
        fm1 = Frame(frame_chat)  # 按钮文本框容器
        Label(fm1, text='Server IP:').pack(side=LEFT, expand=1, fill=BOTH)
        IP_addr = StringVar()
        entry_ip = Entry(fm1, textvariable=IP_addr).pack(side=LEFT, expand=1, fill=BOTH)
        # IP_addr.set('192.168.0.102')
        Label(fm1, text='Server Port:').pack(side=LEFT, expand=1, fill=BOTH)
        Port_num = StringVar()
        entry_port = Entry(fm1, textvariable=Port_num).pack(side=LEFT, expand=1, fill=BOTH)
        Port_num.set('5901')
        Label(fm1, text='Your ID:').pack(side=LEFT, expand=1, fill=BOTH)
        ID_name = StringVar()
        entry_id = Entry(fm1, textvariable=ID_name).pack(side=LEFT, expand=1, fill=BOTH)

        # 第二层
        chat_result = Text(frame_chat, bg='black', fg='green', insertbackground='green', selectbackground='green',
                           insertwidth=3)

        # 第三层
        fm3 = Frame(frame_chat)
        fm3_2 = Frame(fm3, padx=18)
        chat_msg = Text(fm3, height=8, bg='black', fg='green', insertbackground='green', selectbackground='green',
                        insertwidth=3)
        chat_msg.insert(1.0, '[root@01Sec ~]# ')

        # 登录
        btn_login = Button(fm1, text='登入')
        btn_login.pack(side=LEFT, expand=1)
        btn_login.bind("<ButtonRelease>",
                       lambda x: join_server(x, IP_addr.get(), int(Port_num.get()), ID_name.get(), chat_result))
        # 登出
        btn_logout = Button(fm1, text='登出')
        btn_logout.pack(side=LEFT, expand=1)
        btn_logout.bind("<ButtonRelease>", lambda x: logout_server(x, chat_result))
        # 发送
        btn_send = Button(fm3_2, text='发送')
        btn_send.pack(side=TOP, expand=1)
        btn_send.bind("<ButtonRelease>", lambda x: sendThreadFunc(x, chat_result, chat_msg))
        # 保存
        btn_save = Button(fm3_2, text='保存')
        btn_save.pack(side=TOP, expand=1)

        # 布局
        # 第一层
        fm1.pack(side=TOP, fill=BOTH, pady=5)
        # 第二层
        chat_result.pack(side=TOP, expand=1, fill=BOTH)
        # 第三层
        fm3.pack(side=TOP, expand=0, fill=X)
        chat_msg.pack(side=LEFT, expand=1, fill=BOTH)
        fm3_2.pack(side=LEFT, expand=0, fill=BOTH)

    '''
    Explain
    '''

    def show_explain(self):
        frame_explain = LabelFrame(self.tab_explain, text='01Sec')
        frame_explain.pack(expand=1, fill='both')

        text_explain = Text(frame_explain, height=8, bg='black', fg='green', insertbackground='green',
                            selectbackground='green',
                            insertwidth=3)
        text_explain.pack(expand=1, fill=BOTH)

        text_explain.insert(END, '\n  0x00 退出程序前先点击停止按钮,将各功能线程退出\n\n')
        text_explain.insert(END, '  0x01 交流群：553724737\n\n')
        text_explain.insert(END, '  0x02 程序仅供学习\n\n')
        text_explain.insert(END,
                            '\n   ______________________________________________________________________________\n')
        text_explain.insert(END, '  |                                                                              |\n')
        text_explain.insert(END, '  |                              Hello Master !                                  |\n')
        text_explain.insert(END, '  |______________________________________________________________________________|\n')
        text_explain.insert(END, '  |                                                                              |\n')
        text_explain.insert(END, '  |                                                                              |\n')
        text_explain.insert(END, '  |                                                                              |\n')
        text_explain.insert(END, '  |                 Username:           [   security    ]                        |\n')
        text_explain.insert(END, '  |                                                                              |\n')
        text_explain.insert(END, '  |                 Password:           [    ******     ]                        |\n')
        text_explain.insert(END, '  |                                                                              |\n')
        text_explain.insert(END, '  |                                                                              |\n')
        text_explain.insert(END, '  |                                                                              |\n')
        text_explain.insert(END, '  |                                [ Login ]                                     |\n')
        text_explain.insert(END, '  |______________________________________________________________________________|\n')
        text_explain.insert(END, '  |                                                                              |\n')
        text_explain.insert(END, '  |                                                                        01Sec |\n')
        text_explain.insert(END, '  |______________________________________________________________________________|\n')

    '''
    def 01Secwindow(self, window):
        window = tkinter.Toplevel(self.root)
        label = tkinter.Label(window, text="01Sec")
        label.pack(side="top", fill="both", padx=5, pady=10)
    '''
