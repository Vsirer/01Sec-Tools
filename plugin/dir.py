#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Copyright (c) 2017-2017 01 Security Team
"""

import urllib.request, time, queue, threading, webbrowser
import re
import http.cookiejar
from tkinter import messagebox

from .util import *

dirs = None
_crack_len = 0

old_urls = set()
new_urls = set()
flag = 0

_crack_flag = threading.Event()  # 用于暂停线程的标识
_crack_flag.set()  # 将flag设置为True
_crack_running = threading.Event()  # 用于停止线程的标识
_crack_running.set()  # 将running设置为True
_crack_lock = threading.Lock()

_sprider_flag = threading.Event()  # 用于暂停线程的标识
_sprider_flag.set()  # 将flag设置为True
_sprider_running = threading.Event()  # 用于停止线程的标识
_sprider_running.set()  # 将running设置为True
_sprider_lock = threading.Lock()


def dir_sprider(domain, threads, time, tv_sprider, btn_sprider):
    if not domain:
        messagebox.showinfo('01Sec', 'input')
        return
    if 'http://' not in domain:
        domain = 'http://' + domain
    if '/' is not domain[-1]:
        domain = domain + '/'

    btn_sprider['state'] = DISABLED
    items = tv_sprider.get_children()
    [tv_sprider.delete(item) for item in items]

    global _sprider_len
    global _sprider_flag
    global _sprider_running
    global flag
    _sprider_flag.set()
    _sprider_running.set()
    flag = 0

    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    hostname = urllib.parse.urlparse(domain).hostname
    global new_urls
    global old_urls
    new_urls.add(domain)
    old_urls.add(domain)
    for i in range(threads):
        t = threading.Thread(target=_read_url, args=(hostname, opener, time, tv_sprider))
        t.start()


def pause_sprider(event, btn_sprider_pause):
    global _sprider_flag
    global _sprider_running
    state = btn_sprider_pause['text']
    if state == '暂停':
        btn_sprider_pause['text'] = '继续'
        _sprider_flag.clear()  # 设置为False, 让线程阻塞
    elif state == '继续':
        btn_sprider_pause['text'] = '暂停'
        _sprider_flag.set()  # 设置为True, 让线程停止阻塞


def stop_sprider(event, btn_sprider, btn_sprider_pause):
    global _sprider_running
    global _sprider_flag
    global new_urls
    global old_urls
    global flag

    flag = 1
    _sprider_flag.set()  # 将线程从暂停状态恢复, 如何已经暂停的话
    time.sleep(0.01)
    new_urls.clear()
    old_urls.clear()
    _sprider_running.clear()  # 设置为False
    btn_sprider['state'] = NORMAL
    btn_sprider_pause['text'] = '暂停'


def _start_crack(domain, time, dirs, tv_crack, pbar_crack):
    while _crack_running.isSet():
        while not dirs.empty():
            try:
                _crack_flag.wait()
                url = domain + dirs.get()
                req = urllib.request.Request(url,headers=headers)
                # req.get_method = lambda: 'HEAD'
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
        url = tv.item(tv.selection())['values'][0].replace('\n', '').replace('\r','')
        webbrowser.open(url)


def _read_url(hostname, opener, time, tv_sprider):
    global old_urls
    global new_urls
    while _sprider_running.isSet():
        while len(new_urls) != 0:
            _sprider_flag.wait()
            url = new_urls.pop()
            old_urls.add(url)
            _get_urls(url, hostname, opener, time, tv_sprider)


def _get_urls(url, hostname, opener, timed, tv_sprider):
    # urllib.request.install_opener(opener)
    global new_urls
    reqs = urllib.request.Request(url, headers=headers)
    o = opener.open(reqs, timeout=timed)
    # o = urllib.request.urlopen(reqs)
    r = o.read().decode('utf-8')
    links = re.findall(r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')", r, re.I | re.S | re.M)
    temp_urls = set()
    for link in links:
        if flag == 1:
            return
        _sprider_flag.wait()
        if hostname == urllib.parse.urlparse(link).hostname:
            new_url = urllib.parse.urljoin(url, link)
            # temp_urls.add(new_url)
            # for i in temp_urls:
            if new_url not in new_urls and new_url not in old_urls:
                # time.sleep(1)
                new_urls.add(new_url)
                tv_sprider.insert('', END, value=(new_url, o.code))
                # new_url = urllib.parse.urljoin(url, link)
                # if hostname == urllib.parse.urlparse(new_url).hostname:
                #     if new_url not in new_urls and new_url not in old_urls:
                #         new_urls.add(new_url)
                #         tv_sprider.insert('', END, value=(new_url, o.code))
