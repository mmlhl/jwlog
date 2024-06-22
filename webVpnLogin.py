# -*- coding : utf-8 -*-
# @Time      : 2024/6/20 21:19
# @Love      : 小菜包
# @Author    : 木木
# @FileName  : webVpnLogin.py
# description:用于获取webvpn登录二维码，扫码后将cookie保存。
import json
import re
import time
from datetime import datetime
from urllib import parse

from requests import session

s = session()
s.headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en;q=0.7',
    'Referer': 'https://atrust.nnnu.edu.cn:1443/portal/service_center.html'}

r = s.get('https://atrust.nnnu.edu.cn:1443/portal/')
s.get(r'https://atrust.nnnu.edu.cn:1443/portal/theme/manifest.json?rnd=' + str(datetime.now().timestamp()))

authConfig = s.get(
    'https://atrust.nnnu.edu.cn:1443/passport/v1/public/authConfig?clientType=SDPBrowserClient&platform=Windows&lang=zh-CN&needTicket=1').json()
state = authConfig['data']['qyWechatQrcodeConf']['state']
s.headers.update({'Referer': 'https://atrust.nnnu.edu.cn:1443/'})
k = s.get('https://open.work.weixin.qq.com/wwopen/sso/qrConnect',
          params={'state': state, 'appid': 'wx67d184a38985867a', 'agentid': '1000038',
                  'redirect_uri': 'https://atrust.nnnu.edu.cn:1443/passport/v1/auth/qywechat', 'login_type': 'jssdk',
                  'href': 'https://atrust.nnnu.edu.cn:1443/portal/wechat_qrcode.css?portal_rnd=664194665'})
key = re.search(r'key..."([^"]+)"', k.text).group(1)
qr_img = s.get(f'https://open.work.weixin.qq.com/wwopen/sso/qrImg?key={key}')
with open('qr.png', 'wb') as f:
    f.write(qr_img.content)
    print('保存二维码成功')
timestamp = datetime.now().timestamp()
for i in range(5):
    data = {'callback': 'jsonCallback', 'key': key, 'appid': '',
            'redirect_uri': 'https://atrust.nnnu.edu.cn:1443/passport/v1/auth/qywechat', '_': timestamp + i}
    callback_response = s.get('https://open.work.weixin.qq.com/wwopen/sso/l/qrConnect', params=data).text
    callback = callback_response[14:-1]
    print(callback_response)
    callback_json = json.loads(callback)
    if callback_json['status'] == 'QRCODE_SCAN_ERR':
        print('扫码超时')
        break
    if callback_json['status'] == 'QRCODE_SCAN_ING':
        data['statusCode'] = 'QRCODE_SCAN_ING'
        data['lastStatus'] = 'QRCODE_SCAN_ING'
    if callback_json['status'] == 'QRCODE_SCAN_SUCC':
        auth_code = callback_json['auth_code']
        yz_r = s.get('https://atrust.nnnu.edu.cn:1443/passport/v1/auth/qywechat',
                     params={'code': auth_code, 'state': state, 'appid': 'wx67d184a38985867a'})
        rr=s.get(yz_r.url.replace('qrcode_middle', 'shortcut'))

        d = parse.parse_qs(parse.urlparse(yz_r.url).query)
        username = d['username'][0]
        data = d['data'][0]
        ticket=json.loads(data)['ticket']
        s.headers.update({'Referer':rr.url})
        s.get('https://atrust.nnnu.edu.cn:1443/passport/v1/public/authConfig',params={
            'clientType':'SDPBrowserClient',
            'platform':'Windows',
            'lang':'zh-CN',
            'mod':'1',
        })
        s.post('https://atrust.nnnu.edu.cn:1443/controller/v1/public/reportEnv',params={
            'clientType':'SDPBrowserClient',
            'platform':'Windows',
            'lang':'zh-CN'
        }, data={
            "ticket": ticket,
            "deviceId": "001e45c998a51a3e44658fdc2b993f885471e2451bf639c182d509af3383b36638",
            "env": {
                "endpoint": {
                    "device_id": "001e45c998a51a3e44658fdc2b993f885471e2451bf639c182d509af3383b36638",
                    "device": {
                        "type": "browser"
                    }
                }
            }
        })
        s.get('https://atrust.nnnu.edu.cn:1443/passport/v1/auth/authCheck?clientType=SDPBrowserClient&platform=Windows&lang=zh-CN')
        home = s.get('http://jw-nnnu-edu-cn.atrust.nnnu.edu.cn/')
        print(home.url)
        break
    time.sleep(2)
print(r.cookies.get_dict())
