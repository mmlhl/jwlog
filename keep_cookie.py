# -*- coding : utf-8 -*-
# @Time      : 2023/4/11 20:57
# @Author    : 木木
# Love       : 苏·IKUN·温柔·美丽·宝
# @FileName  : keep_cookie.py
# description:用来保持atrust的cookie
import time
import _thread
import requests

from requests.cookies import RequestsCookieJar


jw_cookie = requests.cookies.RequestsCookieJar()
s = requests.session()
c = requests.cookies.RequestsCookieJar()
cookie_str = 'language=zh-CN; lang=zh-cn; enableBrowserAccess=1; showClientDownloadUrl=1; restrictionImgPath=access_restriction_default.png; sid-legacy=cf2697f1-b784-482c-b566-b833287b7883_47180206-ef9a-4e83-8426-70663d9d9d88; sid-legacy.sig=qvqWqm_y6l_yckJiFkyCf55S0nvpRiwzftPjnX1ZuJI; sid=cf2697f1-b784-482c-b566-b833287b7883_47180206-ef9a-4e83-8426-70663d9d9d88; sid.sig=EWyNgQ7htVclAFgY1tC9wDoE7OOFPLd8BiAdeXb0M9M; online=1'
split_list = cookie_str.split('; ')
for kv in split_list:
    k, v = kv.split('=')
    c.set(k, v)
s.cookies.update(c)

def remove_host(ses:requests.Session):
    items=ses.cookies.items()
    cookiejar = requests.cookies.RequestsCookieJar()
    for item in items:
        cookiejar.set(item[0],item[1])
    return cookiejar
def keep_cookie():
    while True:
        keep_s = s.get('http://ca-gxtc-edu-cn.atrust.nnnu.edu.cn:80/zfca/login')
        url = keep_s.url
        # print(url)
        # 如果cookie过期了（重定向到了登录界面）
        if not url.startswith('http://ca-gxtc-edu-cn.atrust.nnnu.edu.cn'):
            print('cookie过期')
            # TODO 通知cookie过期
            return
        time.sleep(60)


def my_session():
    new_session = requests.session()
    new_session.cookies.update(c.copy())
    return new_session


try:
    _thread.start_new_thread(keep_cookie, ())
except:
    print('keep thread err')

