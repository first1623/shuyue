#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号发布系统 - Web API 服务器
提供前端界面和后端API
"""

import sys
import os

# 设置 Windows 控制台编码
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from datetime import datetime
import json
import threading
import time

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 存储任务状态
tasks = {}

# 初始化系统
system = None
try:
    from wechat_main import WeChatContentSystem
    system = WeChatContentSystem()
    print("=" * 60)
    print("系统初始化成功")
    print("=" * 60)
except Exception as e:
    print(f"系统初始化失败: {e}")
    system = None

@app.route('/')
def index():
    """返回前端页面"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    """返回静态文件"""
    return send_from_directory('.', path)

@app.route('/api/status', methods=['GET'])
def api_status():
    """获取系统状态"""
    from config import Config
    return jsonify({
        'success': True,
        'ai_provider': Config.AI_PROVIDER,
        'wechat_appid': Config.WECHAT_APP_ID[:10] + '...' if Config.WECHAT_APP_ID else None,
        'wechat_status': '已连接' if Config.WECHAT_APP_ID else '未配置'
    })

@app.route('/api/test_config', methods=['POST'])
def api_test_config():
    """测试配置"""
    try:
        from agents.wechat_publisher import WeChatPublisher
        publisher = WeChatPublisher()
        token = publisher.get_access_token()

        return jsonify({
            'success': True,
            'ai_status': '已连接',
            'wechat_status': '已连接'
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        })

@app.route('/api/generate_preview', methods=['POST'])
def api_generate_preview():
    """生成预览 - 异步处理"""
    try:
        data = request.json
        theme = data.get('theme')
        need_image = data.get('need_image', False)

        if not theme:
            return jsonify({'success': False, 'message': '主题不能为空'})

        print(f"\n收到生成预览请求: {theme}")

        # 创建任务ID
        task_id = f"task_{int(time.time() * 1000)}"
        tasks[task_id] = {'status': 'processing', 'result': None}

        # 启动后台线程处理
        def process_theme():
            try:
                if system is None:
                    raise Exception("系统未初始化")
                
                content_package = system.process_theme(theme)
                tasks[task_id] = {
                    'status': 'completed',
                    'result': {
                        'success': True,
                        'article': content_package['article'],
                        'content_package': content_package
                    }
                }
                print(f"任务 {task_id} 完成")
            except Exception as e:
                print(f"任务 {task_id} 失败: {e}")
                tasks[task_id] = {
                    'status': 'failed',
                    'result': {'success': False, 'message': str(e)}
                }

        thread = threading.Thread(target=process_theme)
        thread.daemon = True
        thread.start()

        # 立即返回任务ID
        return jsonify({
            'success': True,
            'task_id': task_id,
            'message': '任务已启动，请轮询查询结果'
        })

    except Exception as e:
        print(f"生成预览失败: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': f'生成失败: {str(e)}'
        })

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
    """快速发布 - 异步处理"""
    try:
        data = request.json
        theme = data.get('theme')
        need_image = data.get('need_image', False)

        if not theme:
            return jsonify({'success': False, 'message': '主题不能为空'})

        print(f"\n收到快速发布请求: {theme}")

        # 创建任务ID
        task_id = f"pub_{int(time.time() * 1000)}"
        tasks[task_id] = {'status': 'processing', 'result': None}

        # 启动后台线程处理
        def process_publish():
            try:
                if system is None:
                    raise Exception("系统未初始化")
                
                result = system.full_workflow(theme)
                tasks[task_id] = {
                    'status': 'completed',
                    'result': result
                }
                print(f"发布任务 {task_id} 完成")
            except Exception as e:
                print(f"发布任务 {task_id} 失败: {e}")
                tasks[task_id] = {
                    'status': 'failed',
                    'result': {'success': False, 'message': str(e)}
                }

        thread = threading.Thread(target=process_publish)
        thread.daemon = True
        thread.start()

        # 立即返回任务ID
        return jsonify({
            'success': True,
            'task_id': task_id,
            'message': '发布任务已启动，请轮询查询结果'
        })

    except Exception as e:
        print(f"快速发布失败: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': f'发布失败: {str(e)}'
        })

@app.route('/api/publish_preview', methods=['POST'])
def api_publish_preview():
    """发布预览"""
    try:
        data = request.json
        article = data.get('article')

        if not article:
            return jsonify({'success': False, 'message': '文章内容不能为空'})

        print(f"\n收到发布预览请求: {article.get('title')}")

        # 创建任务ID
        task_id = f"pub_{int(time.time() * 1000)}"
        tasks[task_id] = {'status': 'processing', 'result': None}

        # 启动后台线程处理
        def process_publish():
            try:
                if system is None:
                    raise Exception("系统未初始化")
                
                # 构建内容包
                content_package = {
                    'theme': article.get('title'),
                    'article': article,
                    'image_paths': []
                }
                
                # 发布
                result = system.publish(content_package)
                tasks[task_id] = {
                    'status': 'completed',
                    'result': result
                }
                print(f"发布任务 {task_id} 完成")
            except Exception as e:
                print(f"发布任务 {task_id} 失败: {e}")
                tasks[task_id] = {
                    'status': 'failed',
                    'result': {'success': False, 'message': str(e)}
                }

        thread = threading.Thread(target=process_publish)
        thread.daemon = True
        thread.start()

        # 立即返回任务ID
        return jsonify({
            'success': True,
            'task_id': task_id,
            'message': '发布任务已启动，请轮询查询结果'
        })

    except Exception as e:
        print(f"发布预览失败: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': f'发布失败: {str(e)}'
        })

@app.route('/api/batch_publish', methods=['POST'])
def api_batch_publish():
    """批量发布"""
    try:
        data = request.json
        themes = data.get('themes', [])

        if not themes:
            return jsonify({'success': False, 'message': '主题列表不能为空'})

        print(f"\n收到批量发布请求: {len(themes)} 个主题")

        # 创建任务ID
        task_id = f"batch_{int(time.time() * 1000)}"
        tasks[task_id] = {'status': 'processing', 'result': None}

        # 启动后台线程处理
        def process_batch():
            results = []
            for theme in themes:
                print(f"\n处理主题: {theme}")
                try:
                    if system is None:
                        raise Exception("系统未初始化")
                    
                    result = system.full_workflow(theme)
                    results.append({
                        'theme': theme,
                        'success': result.get('success', False),
                        'message': result.get('message', '')
                    })
                except Exception as e:
                    results.append({
                        'theme': theme,
                        'success': False,
                        'message': str(e)
                    })

            tasks[task_id] = {
                'status': 'completed',
                'result': {
                    'success': True,
                    'results': results,
                    'total': len(themes),
                    'success_count': sum(1 for r in results if r['success'])
                }
            }
            print(f"批量任务 {task_id} 完成")

        thread = threading.Thread(target=process_batch)
        thread.daemon = True
        thread.start()

        # 立即返回任务ID
        return jsonify({
            'success': True,
            'task_id': task_id,
            'message': '批量任务已启动，请轮询查询结果'
        })

    except Exception as e:
        print(f"批量发布失败: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': f'批量发布失败: {str(e)}'
        })

@app.route('/api/records', methods=['GET'])
def api_records():
    """获取发布记录"""
    try:
        import glob
        records_dir = "wechat_publish_records"

        if not os.path.exists(records_dir):
            return jsonify({'success': True, 'records': []})

        # 读取所有记录文件
        record_files = glob.glob(os.path.join(records_dir, "*.json"))
        all_records = []

        for file in record_files:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    records = json.load(f)
                    all_records.extend(records)
            except Exception as e:
                print(f"读取记录文件失败 {file}: {e}")

        # 按时间倒序排序
        all_records.sort(key=lambda x: x.get('timestamp', ''), reverse=True)

        return jsonify({
            'success': True,
            'records': all_records,
            'total': len(all_records)
        })

    except Exception as e:
        print(f"获取记录失败: {e}")
        return jsonify({
            'success': False,
            'message': f'获取记录失败: {str(e)}'
        })

if __name__ == '__main__':
    try:
        print("\n" + "="*60)
        print("微信公众号发布系统 - Web服务器")
        print("="*60)
        print("\n访问地址: http://localhost:5000")
        print("按 Ctrl+C 停止服务器")
        print("="*60 + "\n")
    except:
        pass

    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
