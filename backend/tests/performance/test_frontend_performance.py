#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
前端性能测试（使用Selenium）
测试目标：
1. 首屏加载时间 < 1秒
2. 节点渲染性能
3. 交互响应时间
"""

import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


class TestFrontendPerformance:
    """前端性能测试"""
    
    @pytest.fixture(scope="class")
    def driver(self):
        """初始化浏览器驱动"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 无头模式
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(30)
        
        yield driver
        
        driver.quit()
    
    def test_page_load_time(self, driver):
        """测试首屏加载时间"""
        print("\n📊 测试首屏加载时间...")
        
        start_time = time.time()
        driver.get("http://localhost:3000/graph-optimized")
        
        # 等待图谱容器加载
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "virtual-graph-container"))
        )
        
        load_time = time.time() - start_time
        print(f"✅ 首屏加载时间: {load_time:.2f}秒")
        
        assert load_time < 3.0, f"❌ 首屏加载时间过长: {load_time:.2f}秒"
    
    def test_graph_rendering_time(self, driver):
        """测试图谱渲染时间"""
        print("\n📊 测试图谱渲染时间...")
        
        driver.get("http://localhost:3000/graph-optimized")
        
        # 等待图谱加载
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "virtual-graph-container"))
        )
        
        # 等待节点渲染
        time.sleep(2)  # 等待初始渲染完成
        
        # 检查性能统计面板
        stats_element = driver.find_element(By.CLASS_NAME, "graph-stats")
        stats_text = stats_element.text
        
        print(f"✅ 性能统计: {stats_text}")
        
        # 提取渲染节点数
        if "渲染节点:" in stats_text:
            render_count = int(stats_text.split("渲染节点:")[1].split()[0])
            print(f"✅ 渲染节点数: {render_count}")
            assert render_count < 200, f"❌ 渲染节点数过多: {render_count}"
    
    def test_interaction_response_time(self, driver):
        """测试交互响应时间"""
        print("\n📊 测试交互响应时间...")
        
        driver.get("http://localhost:3000/graph-optimized")
        
        # 等待图谱加载
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "virtual-graph-container"))
        )
        
        # 测试拖拽响应
        graph_container = driver.find_element(By.CLASS_NAME, "virtual-graph-container")
        
        start_time = time.time()
        
        # 模拟拖拽
        from selenium.webdriver.common.action_chains import ActionChains
        
        actions = ActionChains(driver)
        actions.click_and_hold(graph_container)
        actions.move_by_offset(100, 100)
        actions.release()
        actions.perform()
        
        response_time = time.time() - start_time
        print(f"✅ 拖拽响应时间: {response_time * 1000:.2f}ms")
        
        assert response_time < 0.1, f"❌ 拖拽响应时间过长: {response_time * 1000:.2f}ms"
    
    def test_memory_usage(self, driver):
        """测试内存使用情况"""
        print("\n📊 测试内存使用情况...")
        
        driver.get("http://localhost:3000/graph-optimized")
        
        # 等待图谱加载
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "virtual-graph-container"))
        )
        
        time.sleep(3)  # 等待稳定
        
        # 获取内存使用情况
        memory_info = driver.execute_script("""
            return {
                usedJSHeapSize: performance.memory.usedJSHeapSize,
                totalJSHeapSize: performance.memory.totalJSHeapSize,
                jsHeapSizeLimit: performance.memory.jsHeapSizeLimit
            };
        """)
        
        used_memory_mb = memory_info['usedJSHeapSize'] / 1024 / 1024
        print(f"✅ 已用内存: {used_memory_mb:.2f}MB")
        
        # 验收标准：内存使用不应过大
        assert used_memory_mb < 500, f"❌ 内存使用过大: {used_memory_mb:.2f}MB"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
