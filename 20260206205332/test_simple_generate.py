#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os

if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Step 1: 导入模块...")
from agents.wechat_writer import WeChatArticleWriter
from agents.planner import ContentPlanner

print("Step 2: 初始化 Writer...")
writer = WeChatArticleWriter()
print("Writer 初始化完成")

print("Step 3: 初始化 Planner...")
planner = ContentPlanner()
print("Planner 初始化完成")

print("Step 4: 生成策略...")
strategy = {
    "target_audience": "家长",
    "content_angles": ["实用技巧", "情感共鸣"],
    "keywords": ["#育儿", "#情绪管理"],
    "tone": "亲切自然",
    "emojis": ["💡", "❤️"],
    "best_time": "18:00-22:00",
    "content_type": "干货分享",
    "author": "心理Z导航"
}
print("策略:", strategy)

print("\nStep 5: 生成文章...")
theme = "小朋友总是发脾气"
try:
    article = writer.generate_article(theme, strategy)
    print("\n生成成功!")
    print(f"标题: {article['title']}")
    print(f"摘要: {article['digest'][:100]}...")
    print(f"内容长度: {len(article['content'])} 字符")
except Exception as e:
    print(f"生成失败: {e}")
    import traceback
    traceback.print_exc()

print("\n测试完成!")
