#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Copyright (c) 2017-2017 01 Security Team
"""

import os,queue
from tkinter import *
from tkinter import filedialog

# 获取字典
def get_dict(filename):
    q_crack = queue.Queue()
    with open(filename) as f:
        for i in f.readlines():
            q_crack.put(i)
    return q_crack

# 获取目录文件
def get_dir(tree, parent, loadfile):
    # 遍历目录下的子目录
    for p in os.listdir(loadfile):
        # 构建路径
        path = os.path.join(loadfile, p)
        isdir = os.path.isdir(path)
        oid = tree.insert(parent, END, p, text=p, open=False)
        tree.setvar(p, path)
        if isdir:
            get_dir(tree, oid, path)

# 文件选择框
def choose_file(self, event, filename):
    name = filedialog.askopenfilename(filetypes=[("text file", "*.txt")])
    filename.set(name)