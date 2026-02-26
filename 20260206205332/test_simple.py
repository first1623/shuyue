# -*- coding: utf-8 -*-
import sys
import io

# 修复 Windows 控制台编码问题
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import os
from dotenv import load_dotenv

load_dotenv()

print("Step 1: 测试 print")
print("=" * 50)

print("Step 2: 加载配置")
from config import Config

print("Step 3: 检查 AI 配置")
api_key = Config.get_current_api_key()
print(f"AI Provider: {Config.AI_PROVIDER}")
print(f"API Key: {api_key[:10] if api_key else 'None'}...")

print("Step 4: 检查微信配置")
print(f"WeChat AppID: {Config.WECHAT_APP_ID}")
print(f"WeChat Secret: {Config.WECHAT_APP_SECRET[:10] if Config.WECHAT_APP_SECRET else 'None'}...")

print("Step 5: 导入智能体")
from agents.planner import ContentPlanner
from agents.wechat_writer import WeChatArticleWriter
from agents.designer import ImageDesigner
from agents.reviewer import ContentReviewer
from agents.wechat_publisher import WeChatPublisher

print("Step 6: 创建系统")
class WeChatContentSystem:
    def __init__(self):
        print("正在初始化智能体...")
        self.agents = {
            'planner': ContentPlanner(),
            'writer': WeChatArticleWriter(),
            'designer': ImageDesigner(),
            'reviewer': ContentReviewer(),
            'publisher': WeChatPublisher()
        }
        print("智能体初始化完成")

system = WeChatContentSystem()

print("=" * 50)
print("系统初始化成功！")
print("=" * 50)

input("\n按回车键退出...")
