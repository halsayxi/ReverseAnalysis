# -*- coding: utf8 -*-
import subprocess
from functools import partial

subprocess.Popen=partial(subprocess.Popen, encoding="utf-8")
import execjs


def password_encrypt(pwd):
    with open('dzdpRSA.js', 'r', encoding='utf8') as f:
        js_obj=execjs.compile(f.read()) # 编译js代码
        enc_res = js_obj.call("getPwd", pwd)
    print(f">>>>>>调用JS代码加密后的密码为：", enc_res)
    return enc_res


def username_encrypt(username):
    with open('dzdpRSA.js', 'r', encoding='utf8') as f:
        js_obj=execjs.compile(f.read()) # 编译js代码
        enc_res = js_obj.call("getMobile", username)
    print(f">>>>>>调用JS代码加密后的手机号为：", enc_res)
    return enc_res


def run(username,pwd):
    username_encrypt(username)
    password_encrypt(pwd)


if __name__ == '__main__':
    username=input(">>>>>>请输入要登陆的用户手机号：")
    pwd=input(">>>>>>请输入登陆密码：")
    run(username,pwd)