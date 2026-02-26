#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
异常恢复测试运行器
运行所有异常恢复测试并生成报告
"""

import sys
import os
import time
import pytest
from datetime import datetime

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def run_all_recovery_tests():
    """运行所有异常恢复测试"""
    print("=" * 70)
    print("🧪 异常恢复测试套件")
    print("=" * 70)
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    start_time = time.time()
    
    # 测试文件列表
    test_files = [
        "test_database_recovery.py",
        "test_api_recovery.py",
        "test_service_recovery.py",
        "test_network_recovery.py",
        "test_data_recovery.py",
        "test_recovery_integration.py"
    ]
    
    # 运行每个测试文件
    results = {}
    
    for test_file in test_files:
        test_path = os.path.join(os.path.dirname(__file__), test_file)
        
        if not os.path.exists(test_path):
            print(f"\n⚠️  测试文件不存在: {test_file}")
            results[test_file] = {"status": "skipped", "reason": "file_not_found"}
            continue
        
        print(f"\n{'─' * 70}")
        print(f"📋 运行测试: {test_file}")
        print(f"{'─' * 70}")
        
        file_start = time.time()
        
        # 运行pytest
        exit_code = pytest.main([
            test_path,
            "-v",
            "-s",
            "--tb=short",
            "-W", "ignore::DeprecationWarning"
        ])
        
        file_duration = time.time() - file_start
        
        results[test_file] = {
            "status": "passed" if exit_code == 0 else "failed",
            "exit_code": exit_code,
            "duration": file_duration
        }
    
    total_duration = time.time() - start_time
    
    # 打印汇总报告
    print("\n" + "=" * 70)
    print("📊 测试汇总报告")
    print("=" * 70)
    
    passed = sum(1 for r in results.values() if r["status"] == "passed")
    failed = sum(1 for r in results.values() if r["status"] == "failed")
    skipped = sum(1 for r in results.values() if r["status"] == "skipped")
    
    print(f"\n总测试文件: {len(results)}")
    print(f"  ✅ 通过: {passed}")
    print(f"  ❌ 失败: {failed}")
    print(f"  ⏭️  跳过: {skipped}")
    
    print(f"\n总耗时: {total_duration:.2f}秒")
    
    print("\n详细结果:")
    for test_file, result in results.items():
        status_icon = "✅" if result["status"] == "passed" else ("❌" if result["status"] == "failed" else "⏭️")
        duration = result.get("duration", 0)
        print(f"  {status_icon} {test_file}: {result['status']} ({duration:.2f}s)")
    
    print("\n" + "=" * 70)
    print(f"结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    return 0 if failed == 0 else 1


def run_quick_recovery_test():
    """运行快速恢复测试（仅运行关键测试）"""
    print("\n⚡ 快速恢复测试模式")
    print("=" * 70)
    
    # 只运行集成测试
    test_path = os.path.join(os.path.dirname(__file__), "test_recovery_integration.py")
    
    return pytest.main([
        test_path,
        "-v",
        "-s",
        "-k", "test_full_recovery_workflow or test_graceful_degradation"
    ])


def run_database_recovery_tests():
    """仅运行数据库恢复测试"""
    test_path = os.path.join(os.path.dirname(__file__), "test_database_recovery.py")
    return pytest.main([test_path, "-v", "-s"])


def run_api_recovery_tests():
    """仅运行API恢复测试"""
    test_path = os.path.join(os.path.dirname(__file__), "test_api_recovery.py")
    return pytest.main([test_path, "-v", "-s"])


def run_network_recovery_tests():
    """仅运行网络恢复测试"""
    test_path = os.path.join(os.path.dirname(__file__), "test_network_recovery.py")
    return pytest.main([test_path, "-v", "-s"])


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="异常恢复测试运行器")
    parser.add_argument(
        "--mode",
        choices=["all", "quick", "database", "api", "network"],
        default="all",
        help="测试模式: all=全部测试, quick=快速测试, database=仅数据库, api=仅API, network=仅网络"
    )
    
    args = parser.parse_args()
    
    if args.mode == "all":
        exit_code = run_all_recovery_tests()
    elif args.mode == "quick":
        exit_code = run_quick_recovery_test()
    elif args.mode == "database":
        exit_code = run_database_recovery_tests()
    elif args.mode == "api":
        exit_code = run_api_recovery_tests()
    elif args.mode == "network":
        exit_code = run_network_recovery_tests()
    else:
        exit_code = run_all_recovery_tests()
    
    sys.exit(exit_code)
