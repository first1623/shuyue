# -*- coding: utf-8 -*-
import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import json
from config import Config
from agents.wechat_publisher import WeChatPublisher

print("="*60)
print("测试公众号文章发布")
print("="*60)
print()

# 获取access_token
publisher = WeChatPublisher()
print("正在获取access_token...")
token = publisher.get_access_token()
print(f"Access Token: {token[:10]}...\n")

# 准备最简单的测试数据
article = {
    'title': '测试文章',
    'author': '测试',
    'digest': '测试摘要',
    'content': '<p>这是测试内容</p>',
    'content_source_url': '',  # 原文链接，空字符串
    'show_cover_pic': 0,  # 不显示封面
    'need_open_comment': 0,  # 不开评论
    'only_fans_can_comment': 0
}

print("准备发布的文章数据:")
print(json.dumps(article, ensure_ascii=False, indent=2))
print()

print("检查article中的key-value:")
for key, value in article.items():
    print(f"  {key}: {value}")
print()

# 构建payload
payload = {'articles': [article]}
print("发送给微信API的payload:")
print(json.dumps(payload, ensure_ascii=False, indent=2))
print()

# 发送请求
print("正在发送请求...")
import requests
url = f"{publisher.api_base}/draft/add?access_token={token}"
print(f"URL: {url}\n")

response = requests.post(url, json=payload, timeout=30)
result = response.json()

print("微信API返回:")
print(json.dumps(result, ensure_ascii=False, indent=2))
print()

if result.get('errcode') == 0:
    print("发布成功!")
    print(f"Media ID: {result.get('media_id')}")
else:
    print("发布失败!")
    print(f"错误码: {result.get('errcode')}")
    print(f"错误信息: {result.get('errmsg')}")

print()
print("="*60)
input("按回车键退出...")
