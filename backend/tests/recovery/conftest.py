#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
异常恢复测试配置
"""

import pytest
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


@pytest.fixture(scope="session")
def recovery_test_config():
    """恢复测试配置"""
    return {
        "max_retries": 5,
        "retry_delay": 0.1,
        "timeout": 30,
        "circuit_breaker_threshold": 3,
        "recovery_timeout": 1.0
    }


@pytest.fixture
def mock_external_service():
    """模拟外部服务"""
    class MockService:
        def __init__(self):
            self.is_available = True
            self.call_count = 0
        
        def call(self):
            self.call_count += 1
            if not self.is_available:
                raise Exception("Service unavailable")
            return {"status": "success"}
        
        def set_available(self, available):
            self.is_available = available
    
    return MockService()


def pytest_configure(config):
    """配置pytest"""
    config.addinivalue_line(
        "markers", "recovery: mark test as a recovery test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
