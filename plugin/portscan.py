#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Copyright (c) 2017-2017 01 Security Team
"""

__product__ = "1-65535 tcp scan"

import socket, time, threading, queue
from tkinter import messagebox
from tkinter import *

q_ports = None
_port_len = 0

_port_flag = threading.Event()  # 用于暂停线程的标识
_port_flag.set()  # 将flag设置为True
_port_running = threading.Event()  # 用于停止线程的标识
_port_running.set()  # 将running设置为True
_port_lock = threading.Lock()


def portscan(host, ports, port_result, pbar_port):
    while _port_running.isSet():
        while not ports.empty():
            try:
                _port_flag.wait()
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # tcp
                s.settimeout(2)
                port = ports.get()
                result = s.connect_ex((host, int(port)))
                if _port_lock.acquire():
                    if result == 0:
                        port_result.insert(END, "[*]" + host + ":" + str(port) + ">" * 20 + "Open\n")
                    # else:
                    #     port_result.insert(END, "[*]" + host + ":" + str(port) + ">" * 20 + "Close\n")
                    _port_lock.release()
                s.close()
            except Exception as e:
                print("scan error")
                print(e)
                pass
            finally:
                if _port_lock.acquire():
                    global _port_len
                    _port_len = _port_len + 1
                    pbar_port['value'] = _port_len
                    _port_lock.release()


def scanstart(host, ports, port_result, threads, btn_port, pbar_port):
    try:
        if not host:
            messagebox.showinfo('01Sec', 'input')
            return

        t = time.time()
        global q_ports
        q_ports = queue.Queue()

        if '-' in ports and ports.count('-') is 1:
            port_temp = ports.split('-')
            for p in range(int(port_temp[0]), int(port_temp[-1]) + 1):
                q_ports.put(p)
        elif ',' in ports:
            port_temp = ports.split(',')
            for p in port_temp:
                q_ports.put(p)
        else:
            q_ports.put(ports)

        btn_port['state'] = DISABLED
        port_result.delete(0.0, END)

        global _port_len
        global _port_flag
        global _port_running
        _port_flag.set()
        _port_running.set()
        pbar_port['maximum'] = q_ports.qsize()
        _port_len = 0

        for i in range(threads):
            x = threading.Thread(target=portscan, args=(host, q_ports, port_result, pbar_port))
            x.start()
    except Exception as e:
        print("scan done")
        print(e)
        # finally:
        # port_result.insert(END, "\n[*]Scan done\n")


def pause_port(event, btn_port_pause):
    global _port_flag
    global _port_running
    state = btn_port_pause['text']
    if state == '暂停':
        btn_port_pause['text'] = '继续'
        _port_flag.clear()  # 设置为False, 让线程阻塞
    elif state == '继续':
        btn_port_pause['text'] = '暂停'
        _port_flag.set()  # 设置为True, 让线程停止阻塞


def stop_port(event, btn_port, btn_port_pause):
    global _port_running
    global _port_flag
    global q_ports

    _port_flag.set()  # 将线程从暂停状态恢复, 如何已经暂停的话
    time.sleep(0.01)
    q_ports.queue.clear()
    _port_running.clear()  # 设置为False
    btn_port['state'] = NORMAL
    btn_port_pause['text'] = '暂停'
