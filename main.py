# -*- coding: utf-8 -*-
# @Time    : 2023/4/11 16:50
# @Author  : 木木
# @FileName: main.py
# @Software: PyCharm
import _thread
import time

import encode
from keep_cookie import my_session
from login import ty_login


s = my_session()

b=ty_login('', '', s)
print(b)
while True:
    time.sleep(10)
