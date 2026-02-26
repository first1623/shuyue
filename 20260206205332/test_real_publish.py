#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
一键验证真实发布到微信公众号
用法: py test_real_publish.py
"""
import requests
import time
import sys

BASE_URL = "http://localhost:5000"

def start_publish():
    """发起批量发布任务"""
    url = f"{BASE_URL}/api/batch_publish"
    payload = {
        "themes": ["小朋友总是发脾气"],
        "publish_mode": "batch",
        "auto_publish": False  # 只创建草稿，不直接群发
    }
    resp = requests.post(url, json=payload, timeout=60)
    if resp.status_code != 200:
        print(f"[FAIL] 请求失败: HTTP {resp.status_code}")
        print(resp.text)
        return None
    data = resp.json()
    if not data.get("success"):
        print(f"[FAIL] 创建任务失败: {data.get('message')}")
        return None
    task_id = data["task_id"]
    print(f"[OK] 任务已创建: {task_id}")
    return task_id

def poll_task(task_id):
    """轮询任务状态"""
    url = f"{BASE_URL}/api/task/{task_id}"
    print("[WAIT] 轮询任务状态...")
    while True:
        resp = requests.get(url, timeout=30)
        if resp.status_code != 200:
            print(f"[FAIL] 查询任务失败: HTTP {resp.status_code}")
            return None
        data = resp.json()
        status = data.get("status")
        print(f"[{time.strftime('%H:%M:%S')}] 状态: {status}")
        if status == "completed":
            return data
        elif status == "failed":
            print(f"[FAIL] 任务失败: {data.get('error')}")
            return None
        time.sleep(2)

def main():
    print("=== 微信公众号真实发布验证 ===")
    # 1. 发起发布
    task_id = start_publish()
    if not task_id:
        sys.exit(1)

    # 2. 轮询结果
    result = poll_task(task_id)
    if not result:
        sys.exit(1)

    # 3. 解析微信 API 返回
    results = result.get("results", [])
    if not results:
        print("[FAIL] 无发布结果")
        sys.exit(1)

    r = results[0]
    print("\n=== 微信 API 响应 ===")
    print(f"成功: {r['success']}")
    print(f"消息: {r['message']}")
    if r.get("media_id"):
        print(f"MediaID: {r['media_id']}")
    if r.get("article_id"):
        print(f"ArticleID: {r['article_id']}")

    # 4. 提示
    if r["success"]:
        print("\n[SUCCESS] 发布成功！请登录微信公众平台 -> 草稿箱 查看文章。")
    else:
        print("\n[FAIL] 发布失败，请检查：")
        print("  1. 服务器 IP 是否在微信公众平台 IP 白名单")
        print("  2. WECHAT_APP_ID / WECHAT_APP_SECRET 是否正确")
        print("  3. 网络是否能访问 https://api.weixin.qq.com")

if __name__ == "__main__":
    main()
