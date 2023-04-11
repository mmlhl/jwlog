# -*- coding: utf-8 -*-
# @Time    : 2023/4/11 16:50
# @Author  : 木木
# Love : 苏·IKUN·温柔·美丽·宝
# @FileName: main.py
# @Software: PyCharm
import _thread
import encode

_thread.start_new_thread(encode.start, ())
