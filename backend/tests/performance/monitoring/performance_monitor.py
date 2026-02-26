#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
实时性能监控脚本
持续监控系统性能指标
"""

import time
import psutil
import threading
from typing import Dict, List
import json
from datetime import datetime


class PerformanceMonitor:
    """性能监控器"""
    
    def __init__(self, interval: int = 5):
        """
        初始化监控器
        
        Args:
            interval: 监控间隔（秒）
        """
        self.interval = interval
        self.metrics: List[Dict] = []
        self.running = False
        self.monitor_thread = None
    
    def collect_metrics(self) -> Dict:
        """收集性能指标"""
        return {
            "timestamp": datetime.now().isoformat(),
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory": {
                "total_mb": psutil.virtual_memory().total / 1024 / 1024,
                "used_mb": psutil.virtual_memory().used / 1024 / 1024,
                "percent": psutil.virtual_memory().percent
            },
            "disk": {
                "read_mb": psutil.disk_io_counters().read_bytes / 1024 / 1024,
                "write_mb": psutil.disk_io_counters().write_bytes / 1024 / 1024
            },
            "network": {
                "sent_mb": psutil.net_io_counters().bytes_sent / 1024 / 1024,
                "recv_mb": psutil.net_io_counters().bytes_recv / 1024 / 1024
            }
        }
    
    def monitor_loop(self):
        """监控循环"""
        while self.running:
            try:
                metrics = self.collect_metrics()
                self.metrics.append(metrics)
                
                # 实时输出
                print(f"[{metrics['timestamp']}] "
                      f"CPU: {metrics['cpu_percent']:.1f}% | "
                      f"内存: {metrics['memory']['percent']:.1f}% "
                      f"({metrics['memory']['used_mb']:.0f}MB)")
                
            except Exception as e:
                print(f"监控出错: {e}")
            
            time.sleep(self.interval)
    
    def start(self):
        """开始监控"""
        print("🚀 开始性能监控...")
        self.running = True
        self.monitor_thread = threading.Thread(target=self.monitor_loop)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
    
    def stop(self):
        """停止监控"""
        print("🛑 停止性能监控...")
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
    
    def get_report(self) -> Dict:
        """生成监控报告"""
        if not self.metrics:
            return {"error": "没有监控数据"}
        
        # 计算平均值
        avg_cpu = sum(m['cpu_percent'] for m in self.metrics) / len(self.metrics)
        avg_memory_percent = sum(m['memory']['percent'] for m in self.metrics) / len(self.metrics)
        max_memory_percent = max(m['memory']['percent'] for m in self.metrics)
        
        return {
            "monitoring_duration": len(self.metrics) * self.interval,
            "samples": len(self.metrics),
            "avg_cpu_percent": avg_cpu,
            "avg_memory_percent": avg_memory_percent,
            "max_memory_percent": max_memory_percent,
            "alerts": self._check_alerts()
        }
    
    def _check_alerts(self) -> List[Dict]:
        """检查告警"""
        alerts = []
        
        for metrics in self.metrics:
            # CPU告警
            if metrics['cpu_percent'] > 80:
                alerts.append({
                    "type": "CPU_HIGH",
                    "value": metrics['cpu_percent'],
                    "threshold": 80,
                    "timestamp": metrics['timestamp']
                })
            
            # 内存告警
            if metrics['memory']['percent'] > 85:
                alerts.append({
                    "type": "MEMORY_HIGH",
                    "value": metrics['memory']['percent'],
                    "threshold": 85,
                    "timestamp": metrics['timestamp']
                })
        
        return alerts
    
    def save_metrics(self, filename: str = "performance_metrics.json"):
        """保存监控数据"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                "metrics": self.metrics,
                "report": self.get_report()
            }, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 监控数据已保存到: {filename}")


def main():
    """主函数"""
    monitor = PerformanceMonitor(interval=5)
    
    try:
        monitor.start()
        
        # 监控30分钟
        print("监控运行中，持续30分钟...")
        time.sleep(1800)
        
    except KeyboardInterrupt:
        print("\n用户中断监控")
    
    finally:
        monitor.stop()
        report = monitor.get_report()
        print("\n" + "=" * 60)
        print("监控报告")
        print("=" * 60)
        print(f"监控时长: {report['monitoring_duration']}秒")
        print(f"采样次数: {report['samples']}")
        print(f"平均CPU: {report['avg_cpu_percent']:.1f}%")
        print(f"平均内存: {report['avg_memory_percent']:.1f}%")
        print(f"最高内存: {report['max_memory_percent']:.1f}%")
        
        if report['alerts']:
            print(f"\n⚠️ 告警次数: {len(report['alerts'])}")
        
        monitor.save_metrics()


if __name__ == "__main__":
    main()
