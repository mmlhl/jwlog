# -*- coding : utf-8 -*-
# @Time      : 2023/4/11 20:57
# @Author    : 木木
# @FileName  : keep_cookie.py
# description:用来保持atrust的cookie
import random
import time
import _thread
import requests

from requests.cookies import RequestsCookieJar
from typing import List


class CookieData:
    def __init__(self,username=None,_cookies=None):
        self.cookies:RequestsCookieJar = _cookies
        self.username = username

cookies: List[CookieData]=[]
def add_cookie(cookie:CookieData):
    cookies.append(cookie)



def remove_host(ses:requests.Session):
    items=ses.cookies.items()
    cookiejar = requests.cookies.RequestsCookieJar()
    for item in items:
        cookiejar.set(item[0],item[1])
    return cookiejar
def keep_cookie():
    while True:
        for cookie in cookies:
            keep_s = requests.get('http://ca-gxtc-edu-cn.atrust.nnnu.edu.cn:80/zfca/login',cookies=cookie.cookies)
            url = keep_s.url
            # print(url)
            # 如果cookie过期了（重定向到了登录界面）
            if not url.startswith('http://ca-gxtc-edu-cn.atrust.nnnu.edu.cn'):
                print('cookie过期')
                cookies.remove(cookie)
        time.sleep(60)


def my_session():
    new_session = requests.session()
    count=len(cookies)
    # 从0到count取一个随机数
    if count>0:
        index=random.randint(0,count-1)
        new_session.cookies.update(cookies[index].cookies)
    return new_session

try:
    _thread.start_new_thread(keep_cookie, ())
except:
    print('keep thread err')

