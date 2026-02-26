#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
节点详情视图 - 占位符模块
正在开发中
"""

from fastapi import APIRouter

router = APIRouter()

@router.get("/placeholder")
async def placeholder():
    return {"message": "节点详情模块正在开发中", "status": "coming_soon"}