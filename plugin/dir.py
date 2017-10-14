#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Copyright (c) 2017-2017 01 Security Team
"""

import webbrowser

wordlist = []


def sprider(url, wordlist):
    pass


def row_click(event,tv):
    if tv.selection():
    #tv.item(tv.selection())['values'][0]
    #print(tv.selection())
        webbrowser.open(tv.item(tv.selection())['values'][0])