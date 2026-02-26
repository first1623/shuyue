# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv
import requests

load_dotenv()

print("="*60)
print("测试微信API连接")
print("="*60)
print()

app_id = os.getenv('WECHAT_APP_ID')
app_secret = os.getenv('WECHAT_APP_SECRET')

print(f"AppID: {app_id}")
print(f"AppSecret: {app_secret[:10]}...")
print()

url = "https://api.weixin.qq.com/cgi-bin/token"
params = {
    'grant_type': 'client_credential',
    'appid': app_id,
    'secret': app_secret
}

print("正在请求微信API...")
print(f"URL: {url}")
print()

try:
    response = requests.get(url, params=params, timeout=10)
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.text}")
    print()

    result = response.json()

    if 'access_token' in result:
        print("【成功】获取到access_token")
        print(f"Token: {result['access_token'][:10]}...")
    else:
        print(f"【失败】错误码: {result.get('errcode')}")
        print(f"错误信息: {result.get('errmsg')}")

except Exception as e:
    print(f"【错误】{str(e)}")

print()
print("="*60)
input("按回车键退出...")
