#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图谱可视化视图 - 占位符模块
正在开发中
"""

from fastapi import APIRouter

router = APIRouter()

@router.get("/placeholder")
async def placeholder():
    return {"message": "图谱可视化模块正在开发中", "status": "coming_soon"}