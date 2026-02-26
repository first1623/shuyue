#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API性能基准测试
测试目标：
1. 知识树API响应时间 < 500ms
2. 图谱数据API响应时间 < 1000ms
3. 统计信息API响应时间 < 300ms
"""

import sys
import os

# 添加backend目录到Python路径
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

import pytest
import time
import statistics
from typing import List, Dict
from fastapi.testclient import TestClient

try:
    from main import app
    client = TestClient(app)
except ImportError:
    # 如果main模块不可用，创建一个模拟的测试
    app = None
    client = None


class PerformanceMetrics:
    """性能指标收集器"""
    
    def __init__(self):
        self.response_times: List[float] = []
        self.status_codes: List[int] = []
    
    def record(self, response_time: float, status_code: int):
        """记录响应时间和状态码"""
        self.response_times.append(response_time)
        self.status_codes.append(status_code)
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        if not self.response_times:
            return {}
        
        return {
            "count": len(self.response_times),
            "avg_ms": statistics.mean(self.response_times),
            "min_ms": min(self.response_times),
            "max_ms": max(self.response_times),
            "median_ms": statistics.median(self.response_times),
            "p95_ms": statistics.quantiles(self.response_times, n=100)[94] if len(self.response_times) >= 20 else max(self.response_times),
            "p99_ms": statistics.quantiles(self.response_times, n=100)[98] if len(self.response_times) >= 100 else max(self.response_times),
            "success_rate": sum(1 for code in self.status_codes if code == 200) / len(self.status_codes) * 100
        }


class TestAPIPerformance:
    """API性能基准测试"""
    
    @pytest.mark.skipif(client is None, reason="FastAPI app not available")
    def test_knowledge_tree_api_single_request(self):
        """测试知识树API单次请求性能"""
        print("\n📊 测试知识树API单次请求性能...")
        
        start_time = time.time()
        response = client.get("/api/v1/knowledge-tree/tree")
        duration = (time.time() - start_time) * 1000
        
        assert response.status_code == 200, f"请求失败: {response.status_code}"
        assert duration < 500, f"❌ 响应时间过长: {duration:.2f}ms (目标: <500ms)"
        
        print(f"✅ 知识树API响应时间: {duration:.2f}ms")
    
    @pytest.mark.skipif(client is None, reason="FastAPI app not available")
    def test_knowledge_tree_api_multiple_requests(self):
        """测试知识树API多次请求性能（100次）"""
        print("\n📊 测试知识树API多次请求性能（100次）...")
        
        metrics = PerformanceMetrics()
        
        for i in range(100):
            start_time = time.time()
            response = client.get("/api/v1/knowledge-tree/tree")
            duration = (time.time() - start_time) * 1000
            
            metrics.record(duration, response.status_code)
        
        stats = metrics.get_stats()
        
        print(f"✅ 测试次数: {stats['count']}")
        print(f"✅ 平均响应时间: {stats['avg_ms']:.2f}ms")
        print(f"✅ 最小响应时间: {stats['min_ms']:.2f}ms")
        print(f"✅ 最大响应时间: {stats['max_ms']:.2f}ms")
        print(f"✅ 中位数响应时间: {stats['median_ms']:.2f}ms")
        print(f"✅ P95响应时间: {stats['p95_ms']:.2f}ms")
        print(f"✅ P99响应时间: {stats['p99_ms']:.2f}ms")
        print(f"✅ 成功率: {stats['success_rate']:.2f}%")
        
        # 验收标准
        assert stats['avg_ms'] < 500, f"❌ 平均响应时间过长: {stats['avg_ms']:.2f}ms"
        assert stats['p95_ms'] < 800, f"❌ P95响应时间过长: {stats['p95_ms']:.2f}ms"
        assert stats['success_rate'] >= 99, f"❌ 成功率过低: {stats['success_rate']:.2f}%"
    
    @pytest.mark.skipif(client is None, reason="FastAPI app not available")
    def test_graph_data_api_single_request(self):
        """测试图谱数据API单次请求性能"""
        print("\n📊 测试图谱数据API单次请求性能...")
        
        start_time = time.time()
        response = client.get("/api/v1/graph/data")
        duration = (time.time() - start_time) * 1000
        
        assert response.status_code == 200, f"请求失败: {response.status_code}"
        assert duration < 1000, f"❌ 响应时间过长: {duration:.2f}ms (目标: <1000ms)"
        
        print(f"✅ 图谱数据API响应时间: {duration:.2f}ms")
    
    @pytest.mark.skipif(client is None, reason="FastAPI app not available")
    def test_graph_stats_api_performance(self):
        """测试统计信息API性能"""
        print("\n📊 测试统计信息API性能...")
        
        metrics = PerformanceMetrics()
        
        for i in range(50):
            start_time = time.time()
            response = client.get("/api/v1/graph/stats")
            duration = (time.time() - start_time) * 1000
            
            metrics.record(duration, response.status_code)
        
        stats = metrics.get_stats()
        
        print(f"✅ 平均响应时间: {stats['avg_ms']:.2f}ms")
        print(f"✅ P95响应时间: {stats['p95_ms']:.2f}ms")
        
        assert stats['avg_ms'] < 300, f"❌ 平均响应时间过长: {stats['avg_ms']:.2f}ms"
    
    @pytest.mark.skipif(client is None, reason="FastAPI app not available")
    def test_node_detail_api_performance(self):
        """测试节点详情API性能"""
        print("\n📊 测试节点详情API性能...")
        
        # 先获取一个节点ID
        tree_response = client.get("/api/v1/knowledge-tree/tree")
        assert tree_response.status_code == 200
        
        tree_data = tree_response.json()
        nodes = tree_data.get('tree', [])
        
        if not nodes:
            print("⚠️ 没有可测试的节点，跳过测试")
            return
        
        node_id = nodes[0]['id']
        
        metrics = PerformanceMetrics()
        
        for i in range(50):
            start_time = time.time()
            response = client.get(f"/api/v1/knowledge-tree/node/{node_id}")
            duration = (time.time() - start_time) * 1000
            
            metrics.record(duration, response.status_code)
        
        stats = metrics.get_stats()
        
        print(f"✅ 节点详情API平均响应时间: {stats['avg_ms']:.2f}ms")
        
        assert stats['avg_ms'] < 200, f"❌ 平均响应时间过长: {stats['avg_ms']:.2f}ms"
    
    @pytest.mark.skipif(client is None, reason="FastAPI app not available")
    def test_api_response_size(self):
        """测试API响应数据大小"""
        print("\n📊 测试API响应数据大小...")
        
        # 测试知识树API
        tree_response = client.get("/api/v1/knowledge-tree/tree")
        tree_size = len(tree_response.content)
        print(f"✅ 知识树API响应大小: {tree_size / 1024:.2f}KB")
        
        # 测试图谱数据API
        graph_response = client.get("/api/v1/graph/data")
        graph_size = len(graph_response.content)
        print(f"✅ 图谱数据API响应大小: {graph_size / 1024:.2f}KB")
        
        # 验收标准：响应数据不应过大
        assert tree_size < 5 * 1024 * 1024, f"❌ 知识树API响应过大: {tree_size / 1024 / 1024:.2f}MB"
        assert graph_size < 10 * 1024 * 1024, f"❌ 图谱数据API响应过大: {graph_size / 1024 / 1024:.2f}MB"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
