#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Copyright (c) 2017-2017 01 Security Team
"""

import urllib.request
import base64
import codecs

from tkinter import *
from tkinter import messagebox


def encode(event, type_code, text_top, text_bottom):
    en_str = text_top.get('1.0', END).replace('\n', '')
    if en_str == '':
        messagebox.showinfo('01Sec', 'input')
        return
    if type_code == 'url':
        encodestr = url_encode(en_str)
        text_bottom.delete(0.0, END)
        text_bottom.insert(END, encodestr)
    elif type_code == 'base16':
        encodestr = base16_encode(en_str)
        text_bottom.delete(0.0, END)
        text_bottom.insert(END, encodestr)
    elif type_code == 'base32':
        encodestr = base32_encode(en_str)
        text_bottom.delete(0.0, END)
        text_bottom.insert(END, encodestr)
    elif type_code == 'base64':
        encodestr = base64_encode(en_str)
        text_bottom.delete(0.0, END)
        text_bottom.insert(END, encodestr)
    elif type_code == 'base85':
        encodestr = base85_encode(en_str)
        text_bottom.delete(0.0, END)
        text_bottom.insert(END, encodestr)
    elif type_code == 'unicode':
        encodestr = unicode_encode(en_str)
        text_bottom.delete(0.0, END)
        text_bottom.insert(END, encodestr)
    elif type_code == 'hex':
        encodestr = hex_encode(en_str)
        text_bottom.delete(0.0, END)
        text_bottom.insert(END, encodestr)
    else:
        return


def decode(event, type_code, text_top, text_bottom):
    de_str = text_top.get('1.0', END).replace('\n', '')
    print(type(de_str))
    if de_str == '':
        messagebox.showinfo('01Sec', 'input')
        return
    if type_code == 'url':
        decodestr = url_decode(de_str)
        text_bottom.delete(0.0, END)
        text_bottom.insert(END, decodestr)
    elif type_code == 'base16':
        decodestr = base16_decode(de_str)
        text_bottom.delete(0.0, END)
        text_bottom.insert(END, decodestr)
    elif type_code == 'base32':
        decodestr = base32_decode(de_str)
        text_bottom.delete(0.0, END)
        text_bottom.insert(END, decodestr)
    elif type_code == 'base64':
        decodestr = base64_decode(de_str)
        text_bottom.delete(0.0, END)
        text_bottom.insert(END, decodestr)
    elif type_code == 'base85':
        decodestr = base85_decode(de_str)
        text_bottom.delete(0.0, END)
        text_bottom.insert(END, decodestr)
    elif type_code == 'unicode':
        decodestr = unicode_decode(de_str)
        text_bottom.delete(0.0, END)
        text_bottom.insert(END, decodestr)
    elif type_code == 'hex':
        decodestr = hex_decode(de_str)
        text_bottom.delete(0.0, END)
        text_bottom.insert(END, decodestr)
    else:
        return


def url_encode(strs):
    encodestr = urllib.request.quote(strs)
    return encodestr


def url_decode(strs):
    decodestr = urllib.request.unquote(strs)
    return decodestr


def base16_encode(strs):
    bytestr = strs.encode('utf-8')
    encodestr = base64.b16encode(bytestr).decode()
    return encodestr


def base16_decode(strs):
    bytestr = strs.encode('utf-8')
    decodestr = base64.b16decode(bytestr).decode()
    return decodestr


def base32_encode(strs):
    bytestr = strs.encode('utf-8')
    encodestr = base64.b32encode(bytestr).decode()
    return encodestr


def base32_decode(strs):
    bytestr = strs.encode('utf-8')
    decodestr = base64.b32decode(bytestr).decode()
    return decodestr


def base64_encode(strs):
    bytestr = strs.encode('utf-8')
    encodestr = base64.b64encode(bytestr).decode()
    return encodestr


def base64_decode(strs):
    bytestr = strs.encode('utf-8')
    decodestr = base64.b64decode(bytestr).decode()
    return decodestr


def base85_encode(strs):
    bytestr = strs.encode('utf-8')
    encodestr = base64.b85encode(bytestr).decode()
    return encodestr


def base85_decode(strs):
    bytestr = strs.encode('utf-8')
    decodestr = base64.b85decode(bytestr).decode()
    return decodestr


def unicode_encode(strs):
    encodestr = strs.encode('unicode_escape').decode()
    return encodestr


def unicode_decode(strs):
    decodestr = strs.encode('utf-8').decode('unicode_escape')
    return decodestr


def hex_encode(strs):
    encodestr = codecs.encode(strs.encode('utf-8'), 'hex_codec').decode()
    return encodestr


def hex_decode(strs):
    decodestr = codecs.decode(strs, 'hex_codec').decode()
    return decodestr
