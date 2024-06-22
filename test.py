# -*- coding : utf-8 -*-
# @Time      : 2024/6/22 8:22
# @Love      : 小菜包
# @Author    : 木木
# @FileName  : test.py
# description:
from requests import session

r=session().get('http://jw-nnnu-edu-cn.atrust.nnnu.edu.cn/',allow_redirects=True)
print(r.url)