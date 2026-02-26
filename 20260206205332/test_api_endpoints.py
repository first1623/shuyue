# -*- coding: utf-8 -*-
import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import json
import requests
from config import Config

print("="*60)
print("测试不同的API端点")
print("="*60)
print()

# 获取access_token
print("正在获取access_token...")
url = "https://api.weixin.qq.com/cgi-bin/token"
params = {
    'grant_type': 'client_credential',
    'appid': Config.WECHAT_APP_ID,
    'secret': Config.WECHAT_APP_SECRET
}
response = requests.get(url, params=params)
result = response.json()

if 'access_token' not in result:
    print(f"获取token失败: {result}")
    input("按回车键退出...")
    sys.exit(1)

token = result['access_token']
print(f"Access Token: {token[:10]}...\n")

# 测试数据
article = {
    'title': '测试文章',
    'author': '测试',
    'digest': '测试摘要',
    'content': '<p>这是测试内容</p>',
    'content_source_url': '',
    'show_cover_pic': 0,
    'need_open_comment': 0,
    'only_fans_can_comment': 0
}

# 尝试不同的API端点
endpoints = [
    ('draft/add', '添加草稿'),
    ('material/add_news', '添加素材（add_news）'),
]

for endpoint, name in endpoints:
    print(f"\n{'='*60}")
    print(f"测试: {name}")
    print(f"端点: {endpoint}")
    print(f"{'='*60}\n")

    url = f"https://api.weixin.qq.com/cgi-bin/{endpoint}?access_token={token}"

    # 根据不同的端点调整payload格式
    if endpoint == 'material/add_news':
        # add_news 需要不同的格式
        payload = {
            'articles': [article]
        }
    else:
        payload = {'articles': [article]}

    print("发送的数据:")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    print()

    try:
        response = requests.post(url, json=payload, timeout=30)
        result = response.json()

        print("API返回:")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        print()

        if result.get('errcode') == 0:
            print(f"成功！Media ID: {result.get('media_id')}")
        else:
            print(f"失败！错误码: {result.get('errcode')}")
            print(f"错误信息: {result.get('errmsg')}")

    except Exception as e:
        print(f"异常: {str(e)}")

print()
print("="*60)
input("按回车键退出...")
