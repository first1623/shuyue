#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库性能测试
测试目标：
1. PostgreSQL查询性能
2. Neo4j查询性能
3. 数据库连接池性能
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

try:
    from sqlalchemy import text
    from app.core.database import get_db, get_neo4j_session
    from app.models.data_overview import DataOverview, DataBookDetail
    DB_AVAILABLE = True
except ImportError:
    DB_AVAILABLE = False


class TestDatabasePerformance:
    """数据库性能测试"""
    
    @pytest.mark.skipif(not DB_AVAILABLE, reason="Database modules not available")
    def test_postgresql_connection_time(self):
        """测试PostgreSQL连接时间"""
        print("\n📊 测试PostgreSQL连接时间...")
        
        times = []
        for i in range(10):
            start_time = time.time()
            with get_db() as db:
                db.execute(text("SELECT 1"))
            duration = (time.time() - start_time) * 1000
            times.append(duration)
        
        avg_time = statistics.mean(times)
        print(f"✅ 平均连接时间: {avg_time:.2f}ms")
        
        assert avg_time < 50, f"❌ 连接时间过长: {avg_time:.2f}ms"
    
    @pytest.mark.skipif(not DB_AVAILABLE, reason="Database modules not available")
    def test_postgresql_query_performance(self):
        """测试PostgreSQL查询性能"""
        print("\n📊 测试PostgreSQL查询性能...")
        
        with get_db() as db:
            # 测试简单查询
            start_time = time.time()
            db.query(DataOverview).filter(DataOverview.is_deleted == False).limit(100).all()
            duration = (time.time() - start_time) * 1000
            print(f"✅ 简单查询时间: {duration:.2f}ms")
            assert duration < 100, f"❌ 查询时间过长: {duration:.2f}ms"
            
            # 测试统计查询
            start_time = time.time()
            db.query(DataOverview).filter(
                DataOverview.is_deleted == False
            ).count()
            duration = (time.time() - start_time) * 1000
            print(f"✅ 统计查询时间: {duration:.2f}ms")
            assert duration < 200, f"❌ 统计查询时间过长: {duration:.2f}ms"
            
            # 测试关联查询
            start_time = time.time()
            db.query(DataOverview).join(
                DataBookDetail,
                DataOverview.id == DataBookDetail.file_id
            ).limit(50).all()
            duration = (time.time() - start_time) * 1000
            print(f"✅ 关联查询时间: {duration:.2f}ms")
            assert duration < 200, f"❌ 关联查询时间过长: {duration:.2f}ms"
    
    @pytest.mark.skipif(not DB_AVAILABLE, reason="Database modules not available")
    def test_neo4j_connection_time(self):
        """测试Neo4j连接时间"""
        print("\n📊 测试Neo4j连接时间...")
        
        times = []
        for i in range(5):
            start_time = time.time()
            with get_neo4j_session() as session:
                session.run("RETURN 1")
            duration = (time.time() - start_time) * 1000
            times.append(duration)
        
        avg_time = statistics.mean(times)
        print(f"✅ 平均连接时间: {avg_time:.2f}ms")
        
        assert avg_time < 100, f"❌ 连接时间过长: {avg_time:.2f}ms"
    
    @pytest.mark.skipif(not DB_AVAILABLE, reason="Database modules not available")
    def test_neo4j_query_performance(self):
        """测试Neo4j查询性能"""
        print("\n📊 测试Neo4j查询性能...")
        
        with get_neo4j_session() as session:
            # 测试节点查询
            start_time = time.time()
            result = session.run("MATCH (n) RETURN count(n)")
            result.single()
            duration = (time.time() - start_time) * 1000
            print(f"✅ 节点统计时间: {duration:.2f}ms")
            assert duration < 500, f"❌ 节点统计时间过长: {duration:.2f}ms"
            
            # 测试关系查询
            start_time = time.time()
            result = session.run("MATCH ()-[r]->() RETURN count(r)")
            result.single()
            duration = (time.time() - start_time) * 1000
            print(f"✅ 关系统计时间: {duration:.2f}ms")
            assert duration < 500, f"❌ 关系统计时间过长: {duration:.2f}ms"
    
    @pytest.mark.skipif(not DB_AVAILABLE, reason="Database modules not available")
    def test_database_connection_pool(self):
        """测试数据库连接池性能"""
        print("\n📊 测试数据库连接池性能...")
        
        import threading
        
        def query_task():
            with get_db() as db:
                db.query(DataOverview).limit(10).all()
        
        # 50个并发查询
        threads = [threading.Thread(target=query_task) for _ in range(50)]
        
        start_time = time.time()
        for thread in threads:
            thread.start()
        
        for thread in threads:
            thread.join()
        
        duration = time.time() - start_time
        print(f"✅ 50个并发查询总耗时: {duration:.2f}秒")
        print(f"✅ 平均每个查询: {duration / 50 * 1000:.2f}ms")
        
        assert duration < 5, f"❌ 并发查询时间过长: {duration:.2f}秒"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
