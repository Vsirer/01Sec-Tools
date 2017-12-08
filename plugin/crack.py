#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Copyright (c) 2017 01 Security Team
Its Support Mysql、Mssql、ssh
"""

import time, socket, queue, threading
import struct, hashlib
from .util import *

import tkinter.messagebox
from ftplib import FTP
import telnetlib

q_pwds = None
_crack_len = 0

_crack_flag = threading.Event()  # 用于暂停线程的标识
_crack_flag.set()  # 将flag设置为True
_crack_running = threading.Event()  # 用于停止线程的标识
_crack_running.set()  # 将running设置为True
_crack_lock = threading.Lock()


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
    elif type == 'telnet':
        ports.set(23)
    else:
        return


# 点击开始爆破事件
def crack_port(type, ipaddrs, ports, threads, name, filename, btn_crack, crack_result, pbar_crack):
    if not ipaddrs or not ports or not name:
        tkinter.messagebox.showinfo('01sec', 'input')
        return
    global q_pwds
    global _crack_len
    global _crack_flag
    global _crack_running
    if type == 'ftp':
        # 获取密码 queue格式
        q_pwds = get_dict(filename)
        _crack_flag.set()
        _crack_running.set()
        pbar_crack['maximum'] = q_pwds.qsize()
        _crack_len = 0
        btn_crack['state'] = DISABLED
        crack_result.delete('0.0', END)
        for i in range(threads):
            t = threading.Thread(target=crack_ftp, args=(ipaddrs, ports, name, q_pwds, crack_result, pbar_crack))
            t.start()
    elif type == 'mysql':
        q_pwds = get_dict(filename)
        _crack_flag.set()
        _crack_running.set()
        pbar_crack['maximum'] = q_pwds.qsize()
        _crack_len = 0
        btn_crack['state'] = DISABLED
        crack_result.delete('0.0', END)
        for i in range(threads):
            t = threading.Thread(target=crack_mysql, args=(ipaddrs, ports, name, q_pwds, crack_result, pbar_crack))
            t.start()
    elif type == 'telnet':
        q_pwds = get_dict(filename)
        _crack_flag.set()
        _crack_running.set()
        pbar_crack['maximum'] = q_pwds.qsize()
        _crack_len = 0
        btn_crack['state'] = DISABLED
        crack_result.delete('0.0', END)
        for i in range(threads):
            t = threading.Thread(target=crack_telnet, args=(ipaddrs, ports, name, q_pwds, crack_result, pbar_crack))
            t.start()
    elif type == 'ssh':
        try:
            global paramiko
            import paramiko
        except:
            tkinter.messagebox.showinfo('01sec', '需安装paramiko模块')
            return
        q_pwds = get_dict(filename)
        _crack_flag.set()
        _crack_running.set()
        pbar_crack['maximum'] = q_pwds.qsize()
        _crack_len = 0
        btn_crack['state'] = DISABLED
        crack_result.delete('0.0', END)
        for i in range(threads):
            t = threading.Thread(target=crack_ssh, args=(ipaddrs, ports, name, q_pwds, crack_result, pbar_crack))
            t.start()
    elif type == 'mssql':
        try:
            global pymssql
            import pymssql
        except:
            tkinter.messagebox.showinfo('01sec', '需安装pymssql模块')
            return
        q_pwds = get_dict(filename)
        _crack_flag.set()
        _crack_running.set()
        pbar_crack['maximum'] = q_pwds.qsize()
        _crack_len = 0
        btn_crack['state'] = DISABLED
        crack_result.delete('0.0', END)
        for i in range(threads):
            t = threading.Thread(target=crack_mssql, args=(ipaddrs, ports, name, q_pwds, crack_result, pbar_crack))
            t.start()
    elif type == 'rdp':
        tkinter.messagebox.showinfo('01sec', '功能正在研发......')
    else:
        return


def crack_ssh(ipaddrs, port, name, pwd, crack_result, pbar_crack):
    ssh = paramiko.SSHClient()
    while _crack_running.isSet():
        while not pwd.empty():
            try:
                _crack_flag.wait()
                temp_pwd = pwd.get().replace('\n', '')
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(ipaddrs, int(port), name, temp_pwd)
                ssh.close()
                result = '[*]INFO：爆破成功' + '>' * 20 + '用户名为：' + name + '  ' + '密码为：' + temp_pwd
                crack_result.insert(END, result + '\n')
                return
            except Exception as e:
                print(e)
                pass
            finally:
                if _crack_lock.acquire():
                    global _crack_len
                    _crack_len = _crack_len + 1
                    pbar_crack['value'] = _crack_len
                    _crack_lock.release()


def crack_mysql(ipaddrs, port, name, pwd, crack_result, pbar_crack):
    while _crack_running.isSet():
        while not pwd.empty():
            try:
                _crack_flag.wait()
                temp_pwd = pwd.get().replace('\n', '')
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((ipaddrs, int(port)))
                packet = sock.recv(254)
                plugin, scramble = get_scramble(packet)
                if not scramble: return
                auth_data = get_auth_data(name, temp_pwd, scramble, plugin)
                sock.send(auth_data)
                result = sock.recv(1024)
                sock.close()
                if result == b'\x07\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00':
                    result = '[*]INFO：爆破成功' + '>' * 20 + '用户名为：' + name + '  ' + '密码为：' + temp_pwd
                    crack_result.insert(END, result + '\n')
                    return

                # db = pymysql.connect(host=str(ipaddrs), port=int(port), user=name, password=temp_pwd)
                # db.close()
                # result = '[*]INFO：爆破成功' + '>' * 20 + '用户名为：' + name + '  ' + '密码为：' + temp_pwd
                # crack_result.insert(END, result + '\n')
                # return
            except Exception as e:
                print(e)
                pass
            finally:
                if _crack_lock.acquire():
                    global _crack_len
                    _crack_len = _crack_len + 1
                    pbar_crack['value'] = _crack_len
                    _crack_lock.release()


def crack_mssql(ipaddrs, port, name, pwd, crack_result, pbar_crack):
    while _crack_running.isSet():
        while not pwd.empty():
            try:
                _crack_flag.wait()
                temp_pwd = pwd.get().replace('\n', '')
                db = pymssql.connect(str(ipaddrs), int(port), name, temp_pwd)
                db.close()
                result = '[*]INFO：爆破成功' + '>' * 20 + '用户名为：' + name + '  ' + '密码为：' + temp_pwd
                crack_result.insert(END, result + '\n')
                return
            except Exception as e:
                print(e)
                pass
            finally:
                if _crack_lock.acquire():
                    global _crack_len
                    _crack_len = _crack_len + 1
                    pbar_crack['value'] = _crack_len
                    _crack_lock.release()


def crack_telnet(ipaddrs, port, name, pwd, crack_result, pbar_crack):
    while _crack_running.isSet():
        while not pwd.empty():
            try:
                _crack_flag.wait()
                temp_pwd = pwd.get().replace('\n', '')

                try:
                    tn = telnetlib.Telnet(ipaddrs, int(port), 5)
                    # tn.set_debuglevel(3)
                    time.sleep(0.5)
                    os = tn.read_some()
                except Exception as e:
                    return
                user_match = b"(?i)(login|user|username)"
                pass_match = b'(?i)(password|pass)'
                login_match = b'#|\$|>'
                if re.search(user_match, os):
                    try:
                        tn.write(name.encode() + b'\r\n')
                        tn.read_until(pass_match, timeout=1)
                        tn.write(temp_pwd.encode() + b'\r\n')
                        login_info = tn.read_until(login_match, timeout=2)
                        tn.close()
                        if re.search(login_match, login_info):
                            result = '[*]INFO：爆破成功' + '>' * 20 + '用户名为：' + name + '  ' + '密码为：' + temp_pwd
                            crack_result.insert(END, result + '\n')
                            return
                    except Exception as e:
                        pass
                else:
                    try:
                        info = tn.read_until(user_match, timeout=1)
                    except Exception as e:
                        return
                    if re.search(user_match, info):
                        try:
                            tn.write(name.encode() + b'\r\n')
                            tn.read_until(pass_match, timeout=1)
                            tn.write(temp_pwd.encode() + b'\r\n')
                            login_info = tn.read_until(login_match, timeout=2)
                            tn.close()
                            if re.search(login_match, login_info):
                                result = '[*]INFO：爆破成功' + '>' * 20 + '用户名为：' + name + '  ' + '密码为：' + temp_pwd
                                crack_result.insert(END, result + '\n')
                                return
                        except Exception as e:
                            return
                    elif re.search(pass_match, info):
                        tn.read_until(pass_match, timeout=1)
                        tn.write(temp_pwd.encode() + b'\r\n')
                        login_info = tn.read_until(login_match, timeout=2)
                        tn.close()
                        if re.search(login_match, login_info):
                            result = '[*]INFO：爆破成功' + '>' * 20 + '密码为：' + temp_pwd
                            crack_result.insert(END, result + '\n')
                            return
            except Exception as e:
                print(e)
                pass
            finally:
                if _crack_lock.acquire():
                    global _crack_len
                    _crack_len = _crack_len + 1
                    pbar_crack['value'] = _crack_len
                    _crack_lock.release()


def crack_ftp(ipaddrs, port, name, pwd, crack_result, pbar_crack):
    ftp = FTP()
    while _crack_running.isSet():
        while not pwd.empty():
            try:
                _crack_flag.wait()

                ftp.connect(str(ipaddrs), int(port), 5)
                temp_pwd = pwd.get().replace('\n', '')
                ftp.login(name, temp_pwd)
                # a = ftp.retrlines('ls')
                # print(a)
                ftp.quit()
                result = '[*]INFO：爆破成功' + '>' * 20 + '用户名为：' + name + '  ' + '密码为：' + temp_pwd
                crack_result.insert(END, result + '\n')
                return
            except Exception as e:
                print(e)
                pass
            finally:
                if _crack_lock.acquire():
                    global _crack_len
                    _crack_len = _crack_len + 1
                    pbar_crack['value'] = _crack_len
                    _crack_lock.release()


def pause_port_crack(event, btn_crack_pause):
    global _crack_flag
    global _crack_running
    state = btn_crack_pause['text']
    if state == '暂停':
        btn_crack_pause['text'] = '继续'
        _crack_flag.clear()  # 设置为False, 让线程阻塞
    elif state == '继续':
        btn_crack_pause['text'] = '暂停'
        _crack_flag.set()  # 设置为True, 让线程停止阻塞


def stop_port_crack(event, btn_crack, btn_crack_pause):
    global _crack_running
    global _crack_flag
    global q_pwds

    _crack_flag.set()  # 将线程从暂停状态恢复, 如何已经暂停的话
    time.sleep(0.01)
    q_pwds.queue.clear()
    _crack_running.clear()  # 设置为False
    btn_crack['state'] = NORMAL
    btn_crack_pause['text'] = '暂停'


def get_scramble(packet):
    scramble, plugin = b'', b''
    try:
        tmp = packet[15:]
        m = re.findall(b"\x00?([\x01-\x7F]{7,})\x00", tmp)
        if len(m) > 3: del m[0]
        scramble = m[0] + m[1]
    except Exception as e:
        print(e)
        return '', ''
    try:
        plugin = m[2]
    except:
        pass
    return plugin, scramble


def get_auth_data(user, password, scramble, plugin):
    user_hex = user.encode()
    pass_hex = get_hash(password, scramble)
    data = b'\x05\xa2+\x00\x01\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' + user_hex + b'\0' + lenenc_int(len(pass_hex)) + pass_hex + plugin + b'\0'
    data = write_packet(data)
    return data


def get_hash(password, scramble):
    hash_stage1 = hashlib.sha1(password.encode()).digest()
    hash_stage2 = hashlib.sha1(hash_stage1).digest()
    to = hashlib.sha1(scramble + hash_stage2).digest()
    # pymysql source code
    #
    # length = len(to)
    # result = b''
    # for i in range(length):
    #     x = (struct.unpack('B', to[i:i + 1])[0] ^
    #          struct.unpack('B', hash_stage1[i:i + 1])[0])
    #     result += struct.pack('B', x)
    reply = [ord(to[i:i + 1]) ^ ord(hash_stage1[i:i + 1]) for i in range(len(to))]
    result = struct.pack('20B', *reply)
    return result

# pymysql source code
def lenenc_int(i):
    if i < 0:
        raise ValueError("Encoding %d is less than 0 - no representation in LengthEncodedInteger" % i)
    elif i < 0xfb:
        return struct.pack("!B", i)
    elif i < (1 << 16):
        return b'\xfc' + struct.pack('<H', i)
    elif i < (1 << 24):
        return b'\xfd' + struct.pack('<I', i)[:3]
    elif i < (1 << 64):
        return b'\xfe' + struct.pack('<Q', i)
    else:
        raise ValueError("Encoding %x is larger than %x - no representation in LengthEncodedInteger" % (i, (1 << 64)))


def write_packet(payload):
    return struct.pack('<I', len(payload))[:3] + struct.pack("!B", 1) + payload
