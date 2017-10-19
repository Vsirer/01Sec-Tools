#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Copyright (c) 2017-2017 01 Security Team
"""

__product__ = '多人聊天客户端'

import socket, time, threading, hashlib
from tkinter import *

sock = None
my_name = ''
_flag = 0


def join_server(event, host, port, nickName, chat_result):
    global sock
    global _flag
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        chat_result.delete(0.0, END)
        sock.connect((host, port))
        sock.send(b'1')
        _flag = 0
        # nickName = input('[*] INFO: Input You Name：')
        sock.send(nickName.encode())  # 发送名字
        chat_result.insert(END, '[*] INFO: Login Successful，' + nickName + '\n')
        global my_name
        my_name = nickName
        t = threading.Thread(target=recvThreadFunc, args=(chat_result,))
        t.start()
    except Exception as e:
        chat_result.insert(END, '[*] INFO: Login Failed\n')
        print(e)


def logout_server(event, chat_result):
    global sock
    global _flag
    _flag = 1
    sock.shutdown(socket.SHUT_RDWR)  # 关闭socket所有功能
    sock.close()

    chat_result.insert(END, '[*] INFO: logoff current user' + '\n')


def sendThreadFunc(event, chat_result, chat_msg):
    try:
        # myword = input('[root@01Sec ~]# ')
        msg_temp = chat_msg.get('1.0', END)[16:]
        sock.send(msg_temp.encode())
        LocalTime = time.strftime('%H:%M:%S', time.localtime(time.time()))  # 获取本地当前时间
        chat_result.insert(END, LocalTime + ' ' + my_name + ' :' + msg_temp + '\n')
        # print(sock.recv(1024).decode())
        chat_msg.delete(0.0, END)
        chat_msg.insert(1.0, '[root@01Sec ~]# ')
    except ConnectionAbortedError:
        pass
        # chat_result.insert(END, '[*] WARNING: Server Closed This Connection!\n')
        # print('[*] WARNING: Server Closed This Connection!')
    except ConnectionResetError:
        chat_result.insert(END, '[*] WARNING: Server Is Closed!\n')
        print('[*] WARNING: Server Is Closed!')


def recvThreadFunc(chat_result):
    while True:
        try:
            if _flag == 1:
                return
            otherword = sock.recv(4096)
            if otherword:
                LocalTime = time.strftime('%H:%M:%S', time.localtime(time.time()))  # 获取本地当前时间
                chat_result.insert(END, LocalTime + ' ' + otherword.decode() + '\n')
                print(LocalTime + ' ' + otherword.decode())
            else:
                pass
        except:
            pass
            # chat_result.insert(END, '[*] WARNING: Server Closed This Connection!\n')
            # print('[*] WARNING: Server Closed This Connection!')
            # sock.close()
            # return
