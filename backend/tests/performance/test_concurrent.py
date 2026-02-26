#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
并发压力测试
测试目标：
1. 支持100并发用户
2. 支持500并发峰值
3. 系统稳定性测试
"""

import sys
import os

# 添加backend目录到Python路径
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

import pytest
import time
import threading
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


class ConcurrentTestResult:
    """并发测试结果"""
    
    def __init__(self):
        self.response_times: List[float] = []
        self.status_codes: List[int] = []
        self.errors: List[str] = []
        self.lock = threading.Lock()
    
    def record_success(self, response_time: float, status_code: int):
        """记录成功请求"""
        with self.lock:
            self.response_times.append(response_time)
            self.status_codes.append(status_code)
    
    def record_error(self, error: str):
        """记录错误"""
        with self.lock:
            self.errors.append(error)
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        if not self.response_times:
            return {
                "total_requests": 0,
                "errors": len(self.errors),
                "error_rate": 100.0
            }
        
        return {
            "total_requests": len(self.response_times) + len(self.errors),
            "successful_requests": len(self.response_times),
            "failed_requests": len(self.errors),
            "success_rate": len(self.response_times) / (len(self.response_times) + len(self.errors)) * 100,
            "avg_ms": statistics.mean(self.response_times),
            "min_ms": min(self.response_times),
            "max_ms": max(self.response_times),
            "median_ms": statistics.median(self.response_times),
            "p95_ms": statistics.quantiles(self.response_times, n=100)[94] if len(self.response_times) >= 20 else max(self.response_times),
        }


def make_concurrent_requests(
    endpoint: str,
    num_users: int,
    requests_per_user: int = 10
) -> ConcurrentTestResult:
    """
    并发请求测试
    
    Args:
        endpoint: API端点
        num_users: 并发用户数
        requests_per_user: 每个用户的请求数
    
    Returns:
        测试结果
    """
    result = ConcurrentTestResult()
    
    def user_task():
        """单个用户的请求任务"""
        for _ in range(requests_per_user):
            try:
                start_time = time.time()
                response = client.get(endpoint)
                duration = (time.time() - start_time) * 1000
                
                result.record_success(duration, response.status_code)
                
            except Exception as e:
                result.record_error(str(e))
    
    # 创建线程
    threads = [threading.Thread(target=user_task) for _ in range(num_users)]
    
    # 启动所有线程
    start_time = time.time()
    for thread in threads:
        thread.start()
    
    # 等待所有线程完成
    for thread in threads:
        thread.join()
    
    total_duration = time.time() - start_time
    
    return result, total_duration


class TestConcurrentPerformance:
    """并发性能测试"""
    
    @pytest.mark.skipif(client is None, reason="FastAPI app not available")
    def test_10_concurrent_users(self):
        """测试10个并发用户"""
        print("\n🔥 测试10个并发用户...")
        
        result, duration = make_concurrent_requests(
            "/api/v1/graph/stats",
            num_users=10,
            requests_per_user=5
        )
        
        stats = result.get_stats()
        
        print(f"✅ 总请求数: {stats['total_requests']}")
        print(f"✅ 成功请求数: {stats['successful_requests']}")
        print(f"✅ 失败请求数: {stats['failed_requests']}")
        print(f"✅ 成功率: {stats['success_rate']:.2f}%")
        print(f"✅ 平均响应时间: {stats['avg_ms']:.2f}ms")
        print(f"✅ P95响应时间: {stats['p95_ms']:.2f}ms")
        print(f"✅ 总耗时: {duration:.2f}秒")
        
        # 验收标准
        assert stats['success_rate'] >= 99, f"❌ 成功率过低: {stats['success_rate']:.2f}%"
        assert stats['avg_ms'] < 500, f"❌ 平均响应时间过长: {stats['avg_ms']:.2f}ms"
    
    @pytest.mark.skipif(client is None, reason="FastAPI app not available")
    def test_50_concurrent_users(self):
        """测试50个并发用户"""
        print("\n🔥 测试50个并发用户...")
        
        result, duration = make_concurrent_requests(
            "/api/v1/graph/stats",
            num_users=50,
            requests_per_user=5
        )
        
        stats = result.get_stats()
        
        print(f"✅ 总请求数: {stats['total_requests']}")
        print(f"✅ 成功率: {stats['success_rate']:.2f}%")
        print(f"✅ 平均响应时间: {stats['avg_ms']:.2f}ms")
        print(f"✅ P95响应时间: {stats['p95_ms']:.2f}ms")
        print(f"✅ 总耗时: {duration:.2f}秒")
        
        # 验收标准
        assert stats['success_rate'] >= 98, f"❌ 成功率过低: {stats['success_rate']:.2f}%"
        assert stats['avg_ms'] < 1000, f"❌ 平均响应时间过长: {stats['avg_ms']:.2f}ms"
    
    @pytest.mark.skipif(client is None, reason="FastAPI app not available")
    def test_100_concurrent_users(self):
        """测试100个并发用户"""
        print("\n🔥 测试100个并发用户...")
        
        result, duration = make_concurrent_requests(
            "/api/v1/graph/stats",
            num_users=100,
            requests_per_user=3
        )
        
        stats = result.get_stats()
        
        print(f"✅ 总请求数: {stats['total_requests']}")
        print(f"✅ 成功率: {stats['success_rate']:.2f}%")
        print(f"✅ 平均响应时间: {stats['avg_ms']:.2f}ms")
        print(f"✅ P95响应时间: {stats['p95_ms']:.2f}ms")
        print(f"✅ 总耗时: {duration:.2f}秒")
        print(f"✅ 吞吐量: {stats['total_requests'] / duration:.2f} req/s")
        
        # 验收标准
        assert stats['success_rate'] >= 95, f"❌ 成功率过低: {stats['success_rate']:.2f}%"
        assert stats['avg_ms'] < 1500, f"❌ 平均响应时间过长: {stats['avg_ms']:.2f}ms"
    
    @pytest.mark.skipif(client is None, reason="FastAPI app not available")
    def test_500_concurrent_users_stress(self):
        """测试500个并发用户（压力测试）"""
        print("\n🔥🔥🔥 测试500个并发用户（压力测试）...")
        
        result, duration = make_concurrent_requests(
            "/api/v1/graph/stats",
            num_users=500,
            requests_per_user=1
        )
        
        stats = result.get_stats()
        
        print(f"✅ 总请求数: {stats['total_requests']}")
        print(f"✅ 成功请求数: {stats['successful_requests']}")
        print(f"✅ 失败请求数: {stats['failed_requests']}")
        print(f"✅ 成功率: {stats['success_rate']:.2f}%")
        print(f"✅ 平均响应时间: {stats['avg_ms']:.2f}ms")
        print(f"✅ 总耗时: {duration:.2f}秒")
        print(f"✅ 吞吐量: {stats['total_requests'] / duration:.2f} req/s")
        
        # 压力测试的验收标准相对宽松
        assert stats['success_rate'] >= 90, f"❌ 成功率过低: {stats['success_rate']:.2f}%"
        assert stats['avg_ms'] < 3000, f"❌ 平均响应时间过长: {stats['avg_ms']:.2f}ms"
    
    @pytest.mark.skipif(client is None, reason="FastAPI app not available")
    def test_mixed_endpoints_concurrent(self):
        """测试混合API端点并发访问"""
        print("\n🔥 测试混合API端点并发访问...")
        
        endpoints = [
            "/api/v1/graph/stats",
            "/api/v1/knowledge-tree/statistics",
            "/api/v1/graph/data",
        ]
        
        result = ConcurrentTestResult()
        
        def user_task(endpoint: str):
            """单用户任务"""
            try:
                start_time = time.time()
                response = client.get(endpoint)
                duration = (time.time() - start_time) * 1000
                result.record_success(duration, response.status_code)
            except Exception as e:
                result.record_error(str(e))
        
        threads = []
        for endpoint in endpoints:
            for _ in range(20):  # 每个端点20个并发用户
                thread = threading.Thread(target=user_task, args=(endpoint,))
                threads.append(thread)
        
        start_time = time.time()
        for thread in threads:
            thread.start()
        
        for thread in threads:
            thread.join()
        
        duration = time.time() - start_time
        stats = result.get_stats()
        
        print(f"✅ 总请求数: {stats['total_requests']}")
        print(f"✅ 成功率: {stats['success_rate']:.2f}%")
        print(f"✅ 平均响应时间: {stats['avg_ms']:.2f}ms")
        print(f"✅ 总耗时: {duration:.2f}秒")
        print(f"✅ 吞吐量: {stats['total_requests'] / duration:.2f} req/s")
        
        assert stats['success_rate'] >= 98, f"❌ 成功率过低: {stats['success_rate']:.2f}%"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
