# -*- coding: utf-8 -*-
"""调试微信公众号配置"""
import sys
import io

# 修复 Windows 控制台编码问题
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from config import Config
from agents.wechat_publisher import WeChatPublisher
import requests

def debug_config():
    print("="*60)
    print("微信公众号配置调试")
    print("="*60)
    print()

    # 步骤1：检查配置文件
    print("【步骤1】检查配置")
    print(f"AppID: {Config.WECHAT_APP_ID}")
    print(f"AppSecret: {'已配置' if Config.WECHAT_APP_SECRET else '未配置'}")
    print(f"AppSecret长度: {len(Config.WECHAT_APP_SECRET) if Config.WECHAT_APP_SECRET else 0}")

    if not Config.WECHAT_APP_ID or not Config.WECHAT_APP_SECRET:
        print("\n[错误] AppID 或 AppSecret 未配置！")
        print("请检查 .env 文件中的 WECHAT_APP_ID 和 WECHAT_APP_SECRET")
        return False
    print()

    # 步骤2：测试API连接
    print("【步骤2】测试API连接")
    url = "https://api.weixin.qq.com/cgi-bin/token"
    params = {
        'grant_type': 'client_credential',
        'appid': Config.WECHAT_APP_ID,
        'secret': Config.WECHAT_APP_SECRET
    }

    print(f"请求URL: {url}")
    print(f"参数: grant_type=client_credential, appid={Config.WECHAT_APP_ID}, secret=***")
    print()

    try:
        print("正在发送请求...")
        response = requests.get(url, params=params, timeout=10)

        print(f"HTTP状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        print()

        result = response.json()

        if 'access_token' in result:
            print("[成功] 获取到 access_token")
            print(f"Access Token: {result['access_token'][:10]}...")
            print(f"过期时间: {result.get('expires_in', 0)} 秒")
            print()
            print("="*60)
            print("配置正确！可以正常使用")
            print("="*60)
            return True
        else:
            print("[失败] API返回错误")
            print(f"错误码: {result.get('errcode', 'N/A')}")
            print(f"错误信息: {result.get('errmsg', 'N/A')}")
            print()
            print("可能的原因:")
            print("1. AppID 或 AppSecret 错误")
            print("2. IP地址不在白名单中（如公众号设置了IP白名单）")
            print("3. 公众号类型不正确（需要认证服务号）")
            print("4. API接口权限不足")
            return False

    except requests.exceptions.Timeout:
        print("[错误] 请求超时")
        print("请检查网络连接")
        return False
    except requests.exceptions.ConnectionError:
        print("[错误] 无法连接到微信服务器")
        print("请检查网络连接")
        return False
    except Exception as e:
        print(f"[错误] 发生异常: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = debug_config()
    print()
    input("按回车键退出...")
