#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Copyright (c) 2017-2017 01 Security Team
"""

__product__ = '多人聊天服务端'

import socket, threading, time, os

LocalTime = time.strftime('%H:%M:%S', time.localtime(time.time()))  # 获取本地当前时间
Host = '0.0.0.0'
Port = 5901
Buf = 4096  # 接收数据大小
mydict = dict()
mylist = list()
Filepath = ('C:\%s' % LocalTime)  # 保存即时解码后数据，windows不支持:符号，待完善

# print(type(Host))

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((Host, Port))
print('[*]' + 'INFO' + ':' + 'Socket Create Success')
sock.listen(5)
print('[*]' + 'INFO' + ':' + 'Socket Listening Success')
print('[*]' + 'INFO' + ':' + 'Current Time', LocalTime)


# 把whatToSay传给除了exceptNum的所有人
def tellOthers(exceptNum, whatToSay):
    for c in mylist:
        if c.fileno() != exceptNum:
            try:
                c.send(whatToSay.encode())
            except:
                pass


def subThreadIn(myconnection, connNumber):
    try:
        nickname = myconnection.recv(Buf).decode()  # 获取名字
        mydict[myconnection.fileno()] = nickname
        mylist.append(myconnection)
    except ConnectionError as e:
        print(e)
    # print('[*]' + 'INFO' + ':' + int(connNumber) + ' Has Name :', str(nickname))
    # tellOthers(connNumber, '[*]' + 'INFO' + ':' + mydict[connNumber] + ' ' + 'Join In The Server')
    while True:
        try:
            recvedMsg = myconnection.recv(Buf).decode()  # 接收消息
            print(recvedMsg)
            if recvedMsg:
                # print(mydict[connNumber], ':', recvedMsg)
                tellOthers(connNumber, mydict[connNumber] + ' :' + recvedMsg)
                # if
            '''
            elif recvedMsg == b'0':
                print('close')
                connection.close()
            '''

        except (OSError, ConnectionResetError):
            try:
                mylist.remove(myconnection)
            except:
                pass
                # sock.send(b'')
                # sock.close()
                # return
                # print(mydict[connNumber], '[*]' + 'INFO' + ':' + len(mylist) + 'Left')
                # tellOthers(connNumber, '[*]' + 'INFO' + ':' + mydict[connNumber] + 'Left')
    myconnection.close()
    return


while True:
    connection, addr = sock.accept()
    print('[*] INFO: Accept A New Connection', connection.getsockname(), connection.fileno())
    try:
        # connection.settimeout(5)
        buf = connection.recv(Buf).decode()
        print(type(buf))
        if buf == '1':
            connection.send(b'[*] INFO: Welcome Logging In Server')  # btyes类型

            # 为当前连接开辟一个新的线程
            mythread = threading.Thread(target=subThreadIn, args=(connection, connection.fileno()))
            mythread.setDaemon(True)  # 守护进程
            mythread.start()

            # elif buf[-1:] == '0':
            # print('close')
            # connection.shutdown(socket.SHUT_RDWR)
        else:
            connection.send(b'[*] INFO: Please Logging Out')
            connection.close()
    except:
        pass
