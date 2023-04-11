# -*- coding: utf-8 -*-
# @Time    : 2023/4/11 16:56
# @Author  : 木木
# Love : 苏·IKUN·温柔·美丽·宝
# @FileName: login.py
# @Software: PyCharm
import requests
from lxml import etree
from encode import encode
from config import config


def ty_login(msg, acc: str, psw: str, s: requests.Session):
    try:
        c = s.cookies.copy()
        header = {
            "Host": config['other']['ty']['host'],
            "Referer": config['other']['ty']['login_index'],
            "user-agent":"com.huawei.browser/12.1.4.302 (Linux; Android 10; TEL-AN00a) RestClient/6.0.4.300"
        }
        s.get('https://{}/sso.jsp'.format(config['other']['ty']['host']),timeout=1)
        main_html_resp = s.get(config['other']['ty']['login_index'])
        html = etree.HTML(main_html_resp.text)
        login_page_flowkey = html.xpath('//p[@id="login-page-flowkey"]/text()')[0]
        login_croypto = html.xpath('//p[@id="login-croypto"]/text()')[0]
        encode_result = encode(s, login_croypto, psw)
        print("encode响应时间：", main_html_resp.elapsed.seconds)
        csrf_js = s.get("https://sso.nnnu.edu.cn/public/deploy/deploy.js?" + get_millisecond())

        # print(csrf_js.text)
        csrf_key, csrf_value = get_csrf_key_value(csrf_js.text)
        header["Csrf-Key"] = csrf_key
        header["Csrf-Value"] = csrf_value
        print("atrust响应时间：", main_html_resp.elapsed.seconds)
        login_result = s.post("https://sso.nnnu.edu.cn/login",
                              data={"_eventId": "submit", "type": "UsernamePassword",
                                    "execution": login_page_flowkey, "geolocation": "",
                                    "username": acc, "croypto": login_croypto,
                                    "password": encode_result, "passwordPre": psw}
                              , headers=header, allow_redirects=False,timeout=1)
        print("登录响应时间：", main_html_resp.elapsed.seconds)
        h = login_result.headers
        if 'Location' in h.keys():
            s.headers=header['Host']='jw-nnnu-edu-cn.atrust.nnnu.edu.cn'
            coo = requests.cookies.RequestsCookieJar()
            url=h['Location']
            while True:
                resp = s.get(url, allow_redirects=False, cookies=coo.copy(),timeout=1)
                for item in resp.cookies.keys():
                    coo.set(item[0], item[1])
                if '/xsMain.htmlx' in resp.url:
                    print(acc,'登录成功')
                    return True
                elif 'Location' in resp.headers.keys():
                    url=resp.headers['Location']
                else:
                    break
        login_result.close()
        s.cookies = c
        return False
    except:
        return False
