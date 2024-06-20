# -*- coding: utf-8 -*-
# @Time    : 2023/4/11 16:56
# @Author  : 木木
# @FileName: login.py
# @Software: PyCharm6
import requests
from lxml import etree
from config import config
import time
import base64
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad
def get_millisecond():
    return str(int(round(time.time() * 1000)))


# 从js中截取csrf key和value（需要在请求头带上这两个东西才可以访问）
def get_csrf_key_value(response_text):
    key_index = response_text.find("Csrf-Key")
    value_index = response_text.find("Csrf-Value")
    return response_text[key_index + 12:key_index + 44], response_text[value_index + 14:value_index + 46]


# 传统教务系统加密，将账号密码进行编码
def usr_encode(acc, psw):
    return base64.b64encode(acc.encode()).decode() + '%%%' + base64.b64encode(psw.encode()).decode()
def ty_login(acc: str, psw: str, s: requests.Session):
    c = s.cookies.copy()
    try:
        header = {
            "Host": "sso.nnnu.edu.cn",
            "Referer":config['other']['ty']['login_index'],
        }
        main_html_resp = s.get(config['other']['ty']['login_index'])
        html = etree.HTML(main_html_resp.text)
        login_page_flowkey = html.xpath('//p[@id="login-page-flowkey"]/text()')[0]
        login_croypto = html.xpath('//p[@id="login-croypto"]/text()')[0]
        cipher = DES.new(base64.b64decode(login_croypto), DES.MODE_ECB)
        en = cipher.encrypt(pad(psw.encode('utf-8'), DES.block_size, style='pkcs7'))
        encode_result = base64.b64encode(en).decode('utf-8')

        csrf_js = s.get("https://sso.nnnu.edu.cn/public/deploy/deploy.js?" + get_millisecond())
        csrf_key, csrf_value = get_csrf_key_value(csrf_js.text)
        header["Csrf-Key"] = csrf_key
        header["Csrf-Value"] = csrf_value
        login_result = s.post("https://sso.nnnu.edu.cn/login",
                              data={"_eventId": "submit", "type": "UsernamePassword",
                                    "execution": login_page_flowkey, "geolocation": "",
                                    "username": acc, "croypto": login_croypto,
                                    "password": encode_result, "passwordPre": psw}
                              , headers=header, allow_redirects=False, timeout=1)
        h = login_result.headers
        if not 'Location' in h.keys():
            s.headers = header['Host'] = 'jw-nnnu-edu-cn.atrust.nnnu.edu.cn'
            url = h['Location']
            while True:
                if 'jsessionid' in url:
                    url, new_cookie = url.split(';')
                    name, value = new_cookie.split('=')
                    s.cookies.set(name=name, value=value)
                resp = s.get(url, headers=header, allow_redirects=False, timeout=1)
                if '/xsMain.htmlx' in resp.url:
                    return True
                elif 'Location' in resp.headers.keys():
                    url = resp.headers['Location']
                else:
                    break
        s.cookies.clear()
        s.cookies.update(c)
        return False
    except Exception as ee:
        s.cookies.clear()
        s.cookies.update(c)
        print(ee)
        return False
