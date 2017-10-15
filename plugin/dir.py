#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Copyright (c) 2017-2017 01 Security Team
"""

import urllib.request, time, threading, webbrowser

from tkinter import messagebox

from .util import *

dirs = None
_crack_len = 0

_crack_flag = threading.Event()  # 用于暂停线程的标识
_crack_flag.set()  # 将flag设置为True
_crack_running = threading.Event()  # 用于停止线程的标识
_crack_running.set()  # 将running设置为True
_crack_lock = threading.Lock()


def dir_crack(domain, threads, time, dirfile, tv_crack, btn_crack, pbar_crack):
    if not domain:
        messagebox.showinfo('01Sec', 'input')
        return
    if 'http://' not in domain:
        domain = 'http://' + domain
    if '/' is not domain[-1]:
        domain = domain + '/'

    btn_crack['state'] = DISABLED
    items = tv_crack.get_children()
    [tv_crack.delete(item) for item in items]
    global dirs
    global _crack_len
    global _crack_flag
    global _crack_running
    dirs = get_dict(dirfile)
    _crack_flag.set()
    _crack_running.set()
    pbar_crack['maximum'] = dirs.qsize()
    _crack_len = 0
    for i in range(threads):
        t = threading.Thread(target=_start_crack, args=(domain, time, dirs, tv_crack, pbar_crack))
        t.start()


def _start_crack(domain, time, dirs, tv_crack, pbar_crack):
    while _crack_running.isSet():
        while not dirs.empty():
            try:
                _crack_flag.wait()
                url = domain + dirs.get()
                req = urllib.request.Request(url)
                req.get_method = lambda: 'HEAD'
                resp_code = urllib.request.urlopen(req, timeout=time).code
                if resp_code is 200 or resp_code is 403 or resp_code is 302:
                    if _crack_lock.acquire():
                        tv_crack.insert('', END, value=(url, resp_code))
                        _crack_lock.release()
            except Exception as e:
                # print(e)
                pass
            finally:
                if _crack_lock.acquire():
                    global _crack_len
                    _crack_len = _crack_len + 1
                    pbar_crack['value'] = _crack_len
                    _crack_lock.release()


def pause_crack(event, btn_crack_pause):
    global _crack_flag
    global _crack_running
    state = btn_crack_pause['text']
    if state == '暂停':
        btn_crack_pause['text'] = '继续'
        _crack_flag.clear()  # 设置为False, 让线程阻塞
    elif state == '继续':
        btn_crack_pause['text'] = '暂停'
        _crack_flag.set()  # 设置为True, 让线程停止阻塞


def stop_crack(event, btn_crack, btn_crack_pause):
    global _crack_running
    global _crack_flag
    global dirs

    _crack_flag.set()  # 将线程从暂停状态恢复, 如何已经暂停的话
    time.sleep(0.01)
    dirs.queue.clear()
    _crack_running.clear()  # 设置为False
    btn_crack['state'] = NORMAL
    btn_crack_pause['text'] = '暂停'


# 打开url
def row_click(event, tv):
    if tv.selection():
        # tv.item(tv.selection())['values'][0]
        # print(tv.selection())
        url = tv.item(tv.selection())['values'][0].replace('\n', '')
        webbrowser.open(url)
