#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一键调用示例脚本
运行所有 personal Skill 并验证输出（修正路径版）
"""

import os
import subprocess
import sys
from pathlib import Path

# 固定 Skill 根目录（用户目录下的 .codebuddy）
CODEBUDDY_ROOT = Path.home() / ".codebuddy" / "skills"

# Skill 脚本映射：Skill 名 → (脚本绝对路径, 参数)
SKILLS = {
    "auto-doc-generator": (
        CODEBUDDY_ROOT / "auto-doc-generator" / "scripts" / "auto_doc_generator.py",
        Path("c:/Users/zhaoy/CodeBuddy/20260206205332")  # 传给脚本的项目路径
    ),
    "project-analyzer": (
        CODEBUDDY_ROOT / "project-analyzer" / "scripts" / "project_analyzer.py",
        Path("c:/Users/zhaoy/CodeBuddy/20260206205332")
    ),
    "prompt-collector": (
        CODEBUDDY_ROOT / "prompt-collector" / "scripts" / "prompt_collector.py",
        Path("c:/Users/zhaoy/CodeBuddy/20260206205332")
    ),
    "doc-theory-analyzer": (
        CODEBUDDY_ROOT / "doc-theory-analyzer" / "scripts" / "doc_theory_analyzer.py",
        Path("c:/Users/zhaoy/CodeBuddy/20260206205332")
    )
}

def run_skill(name, script_path, arg_path):
    script_full = Path(script_path)
    if not script_full.exists():
        print(f"[FAIL] [{name}] 脚本不存在: {script_full}")
        return False
    cmd = [sys.executable, str(script_full), str(arg_path)]
    print(f"[RUN] 正在运行 [{name}] ...")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            print(f"[OK] [{name}] 执行成功")
            if result.stdout:
                print(result.stdout.strip())
            return True
        else:
            print(f"[FAIL] [{name}] 执行失败")
            if result.stderr:
                print(result.stderr.strip())
            return False
    except subprocess.TimeoutExpired:
        print(f"[TIMEOUT] [{name}] 执行超时")
        return False
    except Exception as e:
        print(f"[EXCEPTION] [{name}] 异常: {e}")
        return False

def main():
    print("=== 一键调用所有 Personal Skill 演示（修正路径） ===\n")
    results = {}
    for skill, (spath, arg) in SKILLS.items():
        ok = run_skill(skill, spath, arg)
        results[skill] = ok
        print()
    # 汇总
    print("=== 执行结果汇总 ===")
    for skill, ok in results.items():
        status = "[OK] 成功" if ok else "[FAIL] 失败"
        print(f"{skill}: {status}")
    # 列出生成的文档
    proj_dir = Path("c:/Users/zhaoy/CodeBuddy/20260206205332")
    print("\n=== 生成文档清单（应在项目根目录）===")
    for fname in [
        "auto_generated_documentation.md",
        "project_requirements_generated.md",
        "prompt_library_generated.md",
        "theory_enhanced_documentation.md"
    ]:
        fpath = proj_dir / fname
        print(f"{fname} : {'[OK] 存在' if fpath.exists() else '[FAIL] 缺失'}")
    print("\n演示结束。")

if __name__ == "__main__":
    main()
