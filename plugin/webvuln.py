#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Copyright (c) 2017-2017 01 Security Team
GET AND POST
"""

import os, urllib, configparser
from tkinter import *
from tkinter import messagebox

config = configparser.ConfigParser()
config.read('testini.ini')
cf = config.sections()
for i in cf:
    print(config.get(i, 'CMS'))


def load_exp(event, tree_web, name, cms, text_path, text_post, method, code):
    try:
        # 获取完整路径
        exp_dir = tree_web.getvar(tree_web.identify_row(event.y))
        if os.path.isfile(exp_dir):
            config = configparser.ConfigParser()
            config.read(exp_dir)
            cf = config.sections()
            for i in cf:
                name.set(config.get(i, 'NAME', raw=True))
                cms.set(config.get(i, 'CMS', raw=True))
                text_path.delete(0.0, END)
                text_path.insert(END, config.get(i, 'PATH', raw=True) + '\n')
                text_post.delete(0.0, END)
                text_post.insert(END, config.get(i, 'POST', raw=True) + '\n')
                method.set(config.get(i, 'METHOD', raw=True))
                code.set(config.get(i, 'CODE', raw=True))
    except Exception as e:
        print(e)
        pass


def exploit(event, url, text_path, text_post, text_cookie, method, code, text_resp):
    url = url.get()
    if not url:
        messagebox.showinfo('01Sec', 'input')
        return
    path = text_path.get('1.0', END)
    post = text_post.get('1.0', END)
    cookie = text_cookie.get('1.0', END)
    method = method.get()
    code = code.get()

    # 构造请求
    # path等于路径加上get参数
    # 如果path不为空  请求加上path
    # 如果post不为空 ...
    # 如果cookie不为空
    # 请求方式method
    # code编码

    # 构造完成 发送请求

    # 获取相应写入gui

    # text_resp.delete(0.0, END)
    # text_resp.insert(END, 响应+'\n')

    print('test')

    pass
