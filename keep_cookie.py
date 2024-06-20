# -*- coding : utf-8 -*-
# @Time      : 2023/4/11 20:57
# @Author    : 木木
# @FileName  : keep_cookie.py
# description:用来保持atrust的cookie
import time
import _thread
import requests

from requests.cookies import RequestsCookieJar


jw_cookie = requests.cookies.RequestsCookieJar()
s = requests.session()
c = requests.cookies.RequestsCookieJar()
cookie_str = 'language=en-US; lang=en-us; enableBrowserAccess=1; showClientDownloadUrl=1; restrictionImgPath=access_restriction_default.png; sid-legacy=cf2697f1-b784-482c-b566-b833287b7883_99b4a8bd-1848-45d9-8320-d5d92fa18f02; sid-legacy.sig=yOeEJ-AQCejrALPAg6j27Y-Mq7PMAJz2kBedffzSfQw; sid=cf2697f1-b784-482c-b566-b833287b7883_99b4a8bd-1848-45d9-8320-d5d92fa18f02; sid.sig=CNkEv4JRlmu3K2Da0MibvpcHXEmbgBLH9xrJvbJcOzg; online=1; sdp_user_token=cf2697f1-b784-482c-b566-b833287b7883_99b4a8bd-1848-45d9-8320-d5d92fa18f02'
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

