#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
性能测试报告生成器
自动运行所有性能测试并生成报告
"""

import sys
import io

# 设置标准输出编码为UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import pytest
import time
import json
import os
from datetime import datetime
from typing import Dict, List


class PerformanceReport:
    """性能测试报告"""
    
    def __init__(self):
        self.test_results = []
        self.start_time = None
        self.end_time = None
    
    def add_result(self, test_name: str, category: str, metrics: Dict):
        """添加测试结果"""
        self.test_results.append({
            "test_name": test_name,
            "category": category,
            "metrics": metrics,
            "timestamp": datetime.now().isoformat()
        })
    
    def generate_report(self) -> Dict:
        """生成完整报告"""
        return {
            "report_title": "知识图谱系统性能测试报告",
            "test_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "duration": (self.end_time - self.start_time) if self.end_time and self.start_time else 0,
            "total_tests": len(self.test_results),
            "summary": self._generate_summary(),
            "details": self.test_results
        }
    
    def _generate_summary(self) -> Dict:
        """生成摘要"""
        categories = {}
        
        for result in self.test_results:
            category = result["category"]
            if category not in categories:
                categories[category] = {
                    "total": 0,
                    "passed": 0,
                    "failed": 0
                }
            
            categories[category]["total"] += 1
            
            # 判断测试是否通过
            metrics = result["metrics"]
            if "success_rate" in metrics:
                if metrics["success_rate"] >= 95:
                    categories[category]["passed"] += 1
                else:
                    categories[category]["failed"] += 1
            elif "avg_ms" in metrics:
                # 简单判断：平均响应时间小于目标即通过
                target_ms = metrics.get("target_ms", 500)
                if metrics["avg_ms"] < target_ms:
                    categories[category]["passed"] += 1
                else:
                    categories[category]["failed"] += 1
        
        return categories
    
    def save_to_file(self, filename: str = "performance_report.json"):
        """保存报告到文件"""
        report = self.generate_report()
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 性能测试报告已保存到: {filename}")


def run_performance_tests():
    """运行所有性能测试"""
    # 获取当前脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("=" * 80)
    print("知识图谱系统性能基准测试")
    print("=" * 80)
    
    report = PerformanceReport()
    report.start_time = time.time()
    
    # 运行API性能测试
    print("\n📊 运行API性能测试...")
    exit_code = pytest.main([
        os.path.join(script_dir, "test_api_performance.py"),
        "-v",
        "-s",
        "--tb=short"
    ])
    
    # 运行并发测试
    print("\n🔥 运行并发压力测试...")
    pytest.main([
        os.path.join(script_dir, "test_concurrent.py"),
        "-v",
        "-s",
        "--tb=short"
    ])
    
    # 运行数据库性能测试
    print("\n🗄️ 运行数据库性能测试...")
    pytest.main([
        os.path.join(script_dir, "test_database_performance.py"),
        "-v",
        "-s",
        "--tb=short"
    ])
    
    report.end_time = time.time()
    
    # 生成报告
    report_json = report.generate_report()
    
    print("\n" + "=" * 80)
    print("性能测试摘要")
    print("=" * 80)
    print(f"测试时间: {report_json['test_date']}")
    print(f"总测试数: {report_json['total_tests']}")
    print(f"测试耗时: {report_json['duration']:.2f}秒")
    
    report_path = os.path.join(script_dir, "performance_report.json")
    report.save_to_file(report_path)
    
    return report_json


if __name__ == "__main__":
    run_performance_tests()
