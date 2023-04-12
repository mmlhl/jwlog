import subprocess

from config import config


# -*- coding : utf-8 -*-
# @Time      : 2023/4/11 18:29
# @Author    : 木木
# Love       : 苏·IKUN·温柔·美丽·宝
# @FileName  : encode.py
# description:根据配置文件自动运行加密端口


def start():
    b_open = config['encode']['open']
    port = config['encode']['port']
    end = config['encode']['end']
    if b_open:
        a = subprocess.run(['npm', 'run', 'encode', str(port), end], stderr=subprocess.PIPE, stdout=subprocess.PIPE,
                           shell=True, cwd='./encode')
        print('加密进程错误信息', a.stderr)
    print('加密进程退出')


def encode(s, key, psw):
    return s.get(
        "http://127.0.0.1:{}{}?key={}=&psw={}".format(config['encode']['port'], config['encode']['end'], key, psw),
        timeout=1).text

