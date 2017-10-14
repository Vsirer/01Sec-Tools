#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Copyright (c) 2017-2017 01 Security Team
Its Support Mysql、Mssql、ssh
"""

import time, queue, threading
from .util import *
# import pymysql
# import pymssql
# import paramiko
from tkinter import filedialog


# 根据下拉框改变默认端口
def change_cbox(event, type, ports):
    if type == 'ssh':
        ports.set(22)
    elif type == 'mysql':
        ports.set(3306)
    elif type == 'mssql':
        ports.set(1433)
    elif type == 'ftp':
        ports.set(21)
    elif type == 'rdp':
        ports.set(3389)
    else:
        return


# 点击开始爆破事件
def crack_port(event, type, ipaddrs, ports, threads, name, filename, crack_result):
    if type == 'ssh':
        # 获取密码 queue格式
        pwd = get_dict(filename)
        for i in range(threads):
            t = threading.Thread(target=crack_ssh, args=(ipaddrs, ports, name, pwd, crack_result))
    elif type == 'mysql':
        for i in range(threads):
            t = threading.Thread()
    else:
        return


def crack_ssh(ipaddrs, port, name, pwd, crack_result):
    # 爆破
    '''
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ipaddrs, int(port), name, pwd)
    ssh.close()
    '''
    # 输出结果
    # crack_result.insert(END, 'xxx\n')


def crack_mysql(host, port, name, pwd):
    pymysql.connect(host=host,
                    port=int(port),
                    user=name,
                    password=pwd)


def crack_mssql(host, port):
    pass
