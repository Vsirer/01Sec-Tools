#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Copyright (c) 2017-2017 01 Security Team
GET AND POST
"""

import os, urllib.request, base64, configparser
from tkinter import *
from tkinter import messagebox

exp_dir = ''


def load_exp(event, tree_web, name, cms, text_path, text_post, method):
    try:
        global exp_dir
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
                temp_path = config.get(i, 'PATH', raw=True)
                text_path.insert(END, base64.b64decode(temp_path.encode('utf-8')).decode() + '\n')
                text_post.delete(0.0, END)
                temp_post = config.get(i, 'POST', raw=True)
                text_post.insert(END, base64.b64decode(temp_post.encode('utf-8')).decode() + '\n')
                method.set(config.get(i, 'METHOD', raw=True))
                # code.set(config.get(i, 'CODE', raw=True))
    except Exception as e:
        print(e)
        pass


def exploit(event, url, text_path, text_post, text_cookie, method, code, text_resp):
    url = url.get()
    if not url:
        messagebox.showinfo('01Sec', 'input')
        return
    path = text_path.get('1.0', END).replace('\n', '')
    post = text_post.get('1.0', END).replace('\n', '').encode('utf-8')
    cookie = text_cookie.get('1.0', END).replace('\n', '')
    method = method.get()
    code = code.get()

    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0'}

    if path:
        if url[-1:] != '/':
            exp_url = url + '/' + path
        else:
            exp_url = url + path
    if cookie:
        headers['Cookie'] = cookie
    text_resp.delete(0.0, END)
    if method == 'GET':
        r = urllib.request.Request(exp_url, headers=headers)
        req = urllib.request.urlopen(r)
        text_resp.insert(END, str(req.headers) + '\n')
        if code == 'UTF-8':
            text_resp.insert(END, req.read().decode('utf-8') + '\n')
        elif code == 'GBK':
            text_resp.insert(END, req.read().decode('gb2312') + '\n')
    elif method == 'POST':
        r = urllib.request.Request(exp_url, data=post, headers=headers)
        req = urllib.request.urlopen(r)
        text_resp.insert(END, str(req.headers) + '\n')
        if code == 'UTF-8':
            text_resp.insert(END, req.read().decode('utf-8') + '\n')
        elif code == 'GBK':
            text_resp.insert(END, req.read().decode('gb2312') + '\n')


def update(event, text_path, text_post, method):
    try:
        path = text_path.get('1.0', END)
        post = text_post.get('1.0', END)
        method = method.get()
        config = configparser.ConfigParser()
        config.read(exp_dir)
        cf = config.sections()
        for i in cf:
            config.set(i, 'PATH', base64.b64encode(path.encode('utf-8')).decode())
            config.set(i, 'POST', base64.b64encode(post.encode('utf-8')).decode())
            config.set(i, 'METHOD', method)
            config.write(open(exp_dir, 'w'))
        messagebox.showinfo('01Sec', '修改成功')
    except Exception as e:
        print(e)
        messagebox.showinfo('01Sec', '修改失败')


def save(event, ):
    pass

def cleaer(event,):
    pass