# -*- coding: utf-8 -*-
# @Time    : 2023/4/11 16:56
# @Author  : 木木
# @FileName: login.py
# @Software: PyCharm6
import ddddocr
import requests
from lxml import etree
from config import config
import time
import base64
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad

def get_millisecond():
    return str(int(round(time.time() * 1000)))

ocr = ddddocr.DdddOcr()
# 从js中截取csrf key和value（需要在请求头带上这两个东西才可以访问）
def get_csrf_key_value(response_text):
    key_index = response_text.find("Csrf-Key")
    value_index = response_text.find("Csrf-Value")
    return response_text[key_index + 12:key_index + 44], response_text[value_index + 14:value_index + 46]


# 传统教务系统加密，将账号密码进行编码
def usr_encode(acc, psw):
    return base64.b64encode(acc.encode()).decode() + '%%%' + base64.b64encode(psw.encode()).decode()

def normal_login(msg, acc: str, psw: str, s: requests.Session):
    c = s.cookies.copy()
    try:

        # 本来打算访问主页获取cookie，后来发现可以省去，因为下一步获取验证码也会获取cookie
        # s.get(host + Holder.index)
        # 获取验证码文件
        res_verifycode = s.get(config + '/jsxsd/verifycode.servlet',timeout=3)
        verifycode = ocr.classification(res_verifycode.content)
        # ocr识别验证码


        # 构建登录请求体
        login_body = {'loginMethod': 'LoginToXk', 'userAccount': acc,
                      'userPassword': psw, 'RANDOMCODE': verifycode,
                      'encoded': usr_encode(acc, psw)}
        # 发起登录请求
        login_result = s.post(url=host + '/jsxsd/xk/LoginToXk', data=login_body,timeout=3)
        # 通过网页后缀判断是否登录成功，如果不成功会回到当前界面，登录成功则重定向到/jsxsd/framework/xsMain.htmlx
        # 登录成功则返回true，其他情况都会跑到最后，返回false
        if login_result.url.endswith('htmlx'):
            return True,None
        else:
            return False,None
    except Exception as e:
        s.cookies.update(c)
        return False ,e
def ty_login(acc: str, psw: str, s: requests.Session):
    c = s.cookies.copy()
    try:
        header = {
            "Host": "sso.nnnu.edu.cn",
            "Referer": "https://sso.nnnu.edu.cn/login?service=http:%2F%2Fjw.nnnu.edu.cn%2Fsso.jsp",
        }
        main_html_resp = s.get("https://sso.nnnu.edu.cn/login?service=http:%2F%2Fjw.nnnu.edu.cn%2Fsso.jsp")
        html = etree.HTML(main_html_resp.text)
        login_page_flowkey = html.xpath('//p[@id="login-page-flowkey"]/text()')[0]
        login_croypto = html.xpath('//p[@id="login-croypto"]/text()')[0]
        cipher = DES.new(base64.b64decode(login_croypto), DES.MODE_ECB)
        en = cipher.encrypt(pad(psw.encode('utf-8'), DES.block_size, style='pkcs7'))
        encode = base64.b64encode(en).decode('utf-8')
        # csrf_js = s.get("http://sso-nnnu-edu-cn-s.atrust.nnnu.edu.cn/public/deploy/deploy.js?" + get_millisecond())
        csrf_js = s.get("https://sso.nnnu.edu.cn/public/deploy/deploy.js?" + get_millisecond())

        csrf_key, csrf_value = get_csrf_key_value(csrf_js.text)
        header["Csrf-Key"] = csrf_key
        header["Csrf-Value"] = csrf_value

        login_result = s.post(
            # "http://sso-nnnu-edu-cn-s.atrust.nnnu.edu.cn/login",
            "https://sso.nnnu.edu.cn/login",
            data={"_eventId": "submit", "type": "UsernamePassword",
                  "execution": login_page_flowkey, "geolocation": "",
                  "username": acc, "croypto": login_croypto,
                  "password": encode, "passwordPre": psw}
            , headers=header, allow_redirects=False, timeout=5)
        h = login_result.headers
        if 'Location' in h.keys():
            s.headers = header['Host'] = 'jw-nnnu-edu-cn.atrust.nnnu.edu.cn'
            url = h['Location']
            while True:
                if 'jsessionid' in url:
                    url, new_cookie = url.split(';')
                    name, value = new_cookie.split('=')
                    s.cookies.set(name=name, value=value)
                resp = s.get(url, headers=header, allow_redirects=False, timeout=1)
                if '/xsMain.htmlx' in resp.url:
                    return True,None
                elif 'Location' in resp.headers.keys():
                    url = resp.headers['Location']
                else:
                    break
        s.cookies.clear()
        s.cookies.update(c)
        return False,None
    except requests.exceptions.ReadTimeout as ee:
        s.cookies.clear()
        s.cookies.update(c)
        return False,ee