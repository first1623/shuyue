# -*- coding: utf-8 -*-
"""测试微信公众号配置"""
import sys
import io

# 修复 Windows 控制台编码问题
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from config import Config
from agents.wechat_publisher import WeChatPublisher

def test_config():
    print("="*60)
    print("微信公众号配置测试")
    print("="*60)
    print()

    # 检查配置
    print("【1. 检查配置】")
    print(f"公众号名称：心理Z导航")
    print(f"AppID：{Config.WECHAT_APP_ID}")
    print(f"AppSecret：{'已配置' if Config.WECHAT_APP_SECRET else '未配置'}")
    print()

    # 测试连接
    print("【2. 测试API连接】")
    try:
        publisher = WeChatPublisher()
        print("正在获取access_token...")
        token = publisher.get_access_token()

        if token:
            print(f"成功！Access Token：{token[:10]}...")
            print()
            print("="*60)
            print("配置测试通过！")
            print("="*60)
            return True
        else:
            print("失败：无法获取access_token")
            return False

    except Exception as e:
        print(f"失败：{str(e)}")
        print()
        print("可能的原因：")
        print("1. AppID 或 AppSecret 错误")
        print("2. 公众号未认证或权限不足")
        print("3. 网络连接问题")
        return False

if __name__ == '__main__':
    success = test_config()
    print()
    if success:
        print("现在可以运行: python wechat_main.py")
    else:
        print("请检查配置后重试")
    input("\n按回车键退出...")
