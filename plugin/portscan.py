#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Copyright (c) 2017-2017 01 Security Team
"""

__product__ = "1-65535 tcp scan"

import socket, time, threading, queue
from tkinter import messagebox
from tkinter import *


def portscan(host, ports, port_result):
    try:

        while not ports.empty():
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # tcp
            s.settimeout(2)
            port = ports.get()
            result = s.connect_ex((host, int(port)))
            if result == 0:
                # print("[*]" + host + ":" + str(port) + ">"*20, "Open")
                port_result.insert(END, "[*]" + host + ":" + str(port) + ">" * 20 + "Open\n")
            else:
                # print("[*]" + host + ":" + str(port) + ">" * 20, "Close")
                port_result.insert(END, "[*]" + host + ":" + str(port) + ">" * 20 + "Close\n")
            # time.sleep(0.5)
            s.close()
    except Exception as e:
        print("scan error")
        print(e)


def scanstart(event, host, ports, port_result, threads):
    try:
        if not host:
            messagebox.showinfo('01Sec', 'input')
            return

        t = time.time()
        q_ports = queue.Queue()

        print(ports)
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

        port_result.delete(0.0, END)
        for i in range(threads):
            x = threading.Thread(target=portscan, args=(host, q_ports, port_result))
            x.start()
    except Exception as e:
        print("scan done")
        print(e)
        # finally:
        # port_result.insert(END, "\n[*]Scan done\n")
