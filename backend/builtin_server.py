#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
纯Python内置服务器 - 使用http.server，零第三方依赖
专为Python 3.13设计，无需安装任何包
"""

import json
import urllib.parse
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
import os

class KnowledgeGraphHandler(BaseHTTPRequestHandler):
    
    def log_message(self, format, *args):
        """自定义日志格式"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {self.address_string()} - {format % args}")
    
    def do_GET(self):
        """处理GET请求"""
        try:
            if self.path == "/":
                self._send_json_response({
                    "message": "学习平台知识图谱系统API服务",
                    "version": "1.0.0",
                    "status": "running",
                    "python_version": "3.13",
                    "mode": "builtin_http_server",
                    "endpoints": {
                        "GET /": "系统信息",
                        "GET /health": "健康检查", 
                        "GET /api/v1/system/stats": "系统统计",
                        "GET /api/v1/knowledge-tree": "知识树结构",
                        "GET /api/v1/nodes/{id}": "节点详情",
                        "GET /api/v1/search?q=关键词": "搜索",
                        "POST /api/v1/knowledge-tree/scan": "开始扫描",
                        "POST /api/v1/documents/{id}/parse": "解析文档"
                    }
                })
            
            elif self.path == "/health":
                self._send_json_response({
                    "status": "healthy",
                    "service": "knowledge_graph_api",
                    "timestamp": datetime.now().isoformat(),
                    "python_version": "3.13",
                    "server": "builtin_http_server"
                })
            
            elif self.path == "/api/v1/system/stats":
                mock_stats = {
                    "total_files": 1247,
                    "total_folders": 156,
                    "supported_docs": 892,
                    "total_size_mb": 2847.5,
                    "parse_success_rate": 94.2,
                    "active_users": 23
                }
                self._send_json_response({
                    "code": 200,
                    "message": "success",
                    "data": mock_stats,
                    "timestamp": datetime.now().isoformat()
                })
            
            elif self.path.startswith("/api/v1/knowledge-tree"):
                mock_tree = [
                    {
                        "id": 1,
                        "name": "知识库根目录",
                        "path": "D:/zyfdownloadanalysis",
                        "type": "folder",
                        "children": [
                            {
                                "id": 2,
                                "name": "机器学习教程",
                                "path": "D:/zyfdownloadanalysis/machine-learning",
                                "type": "folder",
                                "children": [
                                    {
                                        "id": 3,
                                        "name": "深度学习基础.pdf",
                                        "path": "D:/zyfdownloadanalysis/machine-learning/deep-learning.pdf",
                                        "type": "file",
                                        "size": 2048576,
                                        "extension": ".pdf"
                                    },
                                    {
                                        "id": 4,
                                        "name": "神经网络原理.docx",
                                        "path": "D:/zyfdownloadanalysis/machine-learning/neural-networks.docx",
                                        "type": "file",
                                        "size": 1536000,
                                        "extension": ".docx"
                                    }
                                ]
                            },
                            {
                                "id": 5,
                                "name": "编程资料",
                                "path": "D:/zyfdownloadanalysis/programming",
                                "type": "folder",
                                "children": [
                                    {
                                        "id": 6,
                                        "name": "Python进阶.md",
                                        "path": "D:/zyfdownloadanalysis/programming/python-advanced.md",
                                        "type": "file",
                                        "size": 51200,
                                        "extension": ".md"
                                    }
                                ]
                            }
                        ]
                    }
                ]
                self._send_json_response({
                    "code": 200,
                    "message": "success",
                    "data": mock_tree,
                    "timestamp": datetime.now().isoformat()
                })
            
            elif self.path.startswith("/api/v1/nodes/"):
                # 提取节点ID
                node_id = self.path.split("/")[-1]
                mock_node = {
                    "id": int(node_id),
                    "name": f"示例文档_{node_id}.pdf",
                    "path": f"D:/zyfdownloadanalysis/example_{node_id}.pdf",
                    "type": "file",
                    "size": 2048576,
                    "extension": ".pdf",
                    "bookname": "示例文档",
                    "modified_time": "2024-02-11 14:30:25",
                    "parse_status": "completed",
                    "keywords": ["机器学习", "人工智能", "算法", "深度学习", "神经网络"],
                    "abstract": "这是一份关于机器学习和人工智能的示例文档，包含了基础理论和实际应用案例。文档涵盖了监督学习、无监督学习、强化学习等主要概念，并提供了丰富的代码示例和实践指导。通过学习本文档，读者可以掌握机器学习的核心思想和应用方法。"
                }
                self._send_json_response({
                    "code": 200,
                    "message": "success",
                    "data": mock_node,
                    "timestamp": datetime.now().isoformat()
                })
            
            elif self.path.startswith("/api/v1/search"):
                # 解析查询参数
                query_params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
                q = query_params.get('q', [''])[0]
                
                results = [
                    {
                        "id": 3,
                        "name": "深度学习基础.pdf",
                        "type": "file",
                        "path": "D:/zyfdownloadanalysis/machine-learning/deep-learning.pdf",
                        "match_score": 0.95
                    }
                ] if q else []
                
                self._send_json_response({
                    "code": 200,
                    "message": "success",
                    "data": {
                        "query": q,
                        "results": results,
                        "total": len(results)
                    },
                    "timestamp": datetime.now().isoformat()
                })
            
            else:
                self._send_error(404, "接口不存在")
                
        except Exception as e:
            self._send_error(500, f"服务器内部错误: {str(e)}")
    
    def do_POST(self):
        """处理POST请求"""
        try:
            if self.path == "/api/v1/knowledge-tree/scan":
                self._send_json_response({
                    "code": 200,
                    "message": "扫描任务已开始",
                    "data": {
                        "task_id": "scan_task_" + datetime.now().strftime("%Y%m%d_%H%M%S"),
                        "status": "processing",
                        "estimated_time": "30秒",
                        "message": "系统正在扫描文件系统，请稍候..."
                    },
                    "timestamp": datetime.now().isoformat()
                })
            
            elif self.path.startswith("/api/v1/documents/"):
                doc_id = self.path.split("/")[-1]
                self._send_json_response({
                    "code": 200,
                    "message": "解析任务已开始",
                    "data": {
                        "task_id": f"parse_task_{doc_id}_" + datetime.now().strftime("%Y%m%d_%H%M%S"),
                        "status": "processing",
                        "estimated_time": "2分钟",
                        "document_id": int(doc_id),
                        "message": f"正在解析文档 ID:{doc_id}，请稍候..."
                    },
                    "timestamp": datetime.now().isoformat()
                })
            
            else:
                self._send_error(404, "接口不存在")
                
        except Exception as e:
            self._send_error(500, f"服务器内部错误: {str(e)}")
    
    def _send_json_response(self, data):
        """发送JSON响应"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        response_text = json.dumps(data, ensure_ascii=False, indent=2)
        self.wfile.write(response_text.encode('utf-8'))
    
    def _send_error(self, code, message):
        """发送错误响应"""
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        error_data = {
            "code": code,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
        response_text = json.dumps(error_data, ensure_ascii=False)
        self.wfile.write(response_text.encode('utf-8'))
    
    def do_OPTIONS(self):
        """处理预检请求"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def run_server(port=8000):
    """启动服务器"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, KnowledgeGraphHandler)
    
    print("🎉 学习平台知识图谱系统 - 纯Python内置服务器")
    print("="*60)
    print(f"📍 Python版本: {os.sys.version}")
    print(f"🌐 服务地址: http://localhost:{port}")
    print(f"💡 运行模式: 纯Python标准库 (零依赖)")
    print(f"⏰ 启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    print("📚 可用接口:")
    print("   GET  /                           - 系统信息")
    print("   GET  /health                     - 健康检查")
    print("   GET  /api/v1/system/stats        - 系统统计")
    print("   GET  /api/v1/knowledge-tree      - 知识树结构")
    print("   GET  /api/v1/nodes/{id}          - 节点详情")
    print("   GET  /api/v1/search?q=关键词      - 搜索功能")
    print("   POST /api/v1/knowledge-tree/scan  - 开始扫描")
    print("   POST /api/v1/documents/{id}/parse - 解析文档")
    print("="*60)
    print("⏹️  按 Ctrl+C 停止服务器")
    print()
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
        httpd.shutdown()

if __name__ == "__main__":
    run_server()