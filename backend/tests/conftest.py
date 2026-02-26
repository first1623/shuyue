#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pytest 配置文件
"""

import sys
import os

# 添加项目根目录到 Python 路径 - 必须最先执行
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

print(f"[conftest] Added to path: {backend_dir}")
