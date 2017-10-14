#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Copyright (c) 2017-2017 01 Security Team
"""

import urllib.request, threading, webbrowser

from tkinter import messagebox

from .util import *

wordlist = []


def dir_crack(event, domain, threads, time, dirfile, tv_crack):
    print(threads)
    if not domain:
        messagebox.showinfo('01Sec', 'input')
        return
    if 'http://' not in domain:
        domain = 'http://' + domain
    if '/' is not domain[-1]:
        domain = domain + '/'
    dirs = get_dict(dirfile)

    for i in range(threads):
        t = threading.Thread(target=_start_crack, args=(domain, time, dirs, tv_crack))
        t.start()


def _start_crack(domain, time, dirs, tv_crack):
    while not dirs.empty():
        url = domain + dirs.get()
        req = urllib.request.Request(url)
        req.get_method = lambda: 'HEAD'
        try:
            resp_code = urllib.request.urlopen(req, timeout=time).code
            if resp_code is 200 or resp_code is 403 or resp_code is 302:
                tv_crack.insert('', END, value=(url, resp_code))
        except Exception as e:
            print(e)
            pass


# 打开url
def row_click(event, tv):
    if tv.selection():
        # tv.item(tv.selection())['values'][0]
        # print(tv.selection())
        url = tv.item(tv.selection())['values'][0].replace('\n', '')
        webbrowser.open(url)
