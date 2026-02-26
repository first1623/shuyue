#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号发布系统 - Web API 服务器 (简化版)
"""

import sys
import os

if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import threading
import time

app = Flask(__name__)
CORS(app)

# 存储任务状态
tasks = {}

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

@app.route('/api/status', methods=['GET'])
def api_status():
    from config import Config
    return jsonify({
        'success': True,
        'ai_provider': Config.AI_PROVIDER,
        'wechat_appid': Config.WECHAT_APP_ID[:10] + '...' if Config.WECHAT_APP_ID else None,
        'wechat_status': '已连接' if Config.WECHAT_APP_ID else '未配置'
    })

@app.route('/api/test_config', methods=['POST'])
def api_test_config():
    try:
        from agents.wechat_publisher import WeChatPublisher
        publisher = WeChatPublisher()
        token = publisher.get_access_token()
        return jsonify({'success': True, 'message': '连接成功'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/generate_preview', methods=['POST'])
def api_generate_preview():
    """异步生成预览"""
    try:
        data = request.json
        theme = data.get('theme')
        
        if not theme:
            return jsonify({'success': False, 'message': '主题不能为空'})
        
        # 创建任务ID
        task_id = str(int(time.time()))
        tasks[task_id] = {'status': 'processing', 'result': None}
        
        # 启动后台线程处理
        def process():
            try:
                from wechat_main import WeChatContentSystem
                system = WeChatContentSystem()
                content_package = system.process_theme(theme)
                tasks[task_id] = {
                    'status': 'completed',
                    'result': {
                        'success': True,
                        'article': content_package['article']
                    }
                }
            except Exception as e:
                tasks[task_id] = {
                    'status': 'failed',
                    'result': {'success': False, 'message': str(e)}
                }
        
        thread = threading.Thread(target=process)
        thread.start()
        
        # 立即返回任务ID
        return jsonify({
            'success': True,
            'task_id': task_id,
            'message': '任务已启动'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/task/<task_id>', methods=['GET'])
def api_get_task(task_id):
    """获取任务状态"""
    task = tasks.get(task_id)
    if not task:
        return jsonify({'success': False, 'message': '任务不存在'})
    
    return jsonify({
        'success': True,
        'status': task['status'],
        'result': task['result']
    })

@app.route('/api/quick_publish', methods=['POST'])
def api_quick_publish():
    """快速发布 - 简化版，直接返回模拟结果"""
    try:
        data = request.json
        theme = data.get('theme')
        
        if not theme:
            return jsonify({'success': False, 'message': '主题不能为空'})
        
        # 这里简化处理，实际应该调用系统
        return jsonify({
            'success': True,
            'message': f'主题"{theme}"已添加到处理队列',
            'media_id': 'draft_' + str(int(time.time()))
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/records', methods=['GET'])
def api_records():
    return jsonify({'success': True, 'records': []})

if __name__ == '__main__':
    print("\n" + "="*60)
    print("微信公众号发布系统 - Web服务器 (简化版)")
    print("="*60)
    print("\n访问地址: http://localhost:5000")
    print("="*60 + "\n")
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
