#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import threading
import time

if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def run_with_timeout(func, args=(), kwargs={}, timeout=120):
    """运行函数带超时"""
    result = [None]
    exception = [None]
    
    def target():
        try:
            result[0] = func(*args, **kwargs)
        except Exception as e:
            exception[0] = e
    
    thread = threading.Thread(target=target)
    thread.start()
    thread.join(timeout)
    
    if thread.is_alive():
        print(f"函数执行超时 ({timeout}秒)")
        return None
    
    if exception[0]:
        raise exception[0]
    
    return result[0]

print("开始测试...")
try:
    from wechat_main import WeChatContentSystem
    
    print("初始化系统...")
    system = WeChatContentSystem()
    print("系统初始化完成")
    
    print("\n调用 process_theme...")
    start = time.time()
    
    result = run_with_timeout(system.process_theme, ("测试主题",), timeout=60)
    
    elapsed = time.time() - start
    print(f"\n执行完成，耗时: {elapsed:.2f}秒")
    
    if result:
        print(f"标题: {result['article']['title']}")
    else:
        print("返回结果为 None")
        
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()
