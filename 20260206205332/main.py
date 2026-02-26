#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书多智能体内容生成与发布系统
主程序入口
"""

import sys
import os
import io

# 修复 Windows 控制台编码问题
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from xiaohongshu_publisher import XiaohongshuPublisher
from logger import logger
from config import Config

def print_banner():
    """打印欢迎横幅"""
    banner = """
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║          小红书多智能体内容生成与发布系统                  ║
║                                                            ║
║              Multi-Agent Xiaohongshu Publisher             ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
"""
    print(banner)


def print_menu():
    """打印主菜单"""
    menu = """
═════════════════════════════════════════════════════════════
                        主菜单
═════════════════════════════════════════════════════════════

  1. 快速发布 - 输入主题直接发布
  2. 生成预览 - 生成内容后确认
  3. 批量发布 - 批量处理多个主题
  4. 查看记录 - 查看历史发布记录
  5. 系统配置 - 查看和修改配置
  6. 退出程序

═════════════════════════════════════════════════════════════
"""
    print(menu)


def check_config():
    """检查配置"""
    print("\n检查系统配置...")

    try:
        Config.validate()
        print("[OK] 基础配置验证通过")

        # 检查API配置
        api_key = Config.get_current_api_key()
        if not api_key:
            print("[WARN] 未配置API Key")
            print("  请在.env文件中设置对应的API_KEY")
            return False

        print(f"[OK] {Config.AI_PROVIDER.upper()} API Key: {api_key[:10]}...")

        if Config.XHS_ACCESS_TOKEN:
            print("[OK] 小红书API: 已配置")
        else:
            print("[WARN] 小红书API: 未配置（将使用模拟模式）")

        return True

    except ValueError as e:
        print(f"[ERROR] 配置错误: {e}")
        return False


def quick_publish(publisher):
    """快速发布模式"""
    print("\n" + "─"*50)
    print("快速发布模式")
    print("─"*50)

    theme = input("\n请输入发布主题: ").strip()
    if not theme:
        print("主题不能为空")
        return

    result = publisher.full_workflow(theme)
    return result


def preview_publish(publisher):
    """预览发布模式"""
    print("\n" + "─"*50)
    print("预览发布模式")
    print("─"*50)

    theme = input("\n请输入发布主题: ").strip()
    if not theme:
        print("主题不能为空")
        return

    # 生成内容
    try:
        content_package = publisher.process_theme(theme)

        # 展示预览
        publisher.display_content_preview(content_package)

        # 询问是否发布
        choice = input("\n是否立即发布? (y/n): ").strip().lower()
        if choice == 'y':
            result = publisher.publish(content_package)
            print(f"\n发布结果: {result.get('message', 'Unknown')}")
        else:
            print("已取消发布")

    except Exception as e:
        print(f"错误: {str(e)}")


def batch_publish(publisher):
    """批量发布模式"""
    print("\n" + "─"*50)
    print("批量发布模式")
    print("─"*50)

    themes_input = input("\n请输入主题（多个主题用逗号分隔）:\n").strip()

    if not themes_input:
        print("主题不能为空")
        return

    themes = [t.strip() for t in themes_input.split(',') if t.strip()]

    print(f"\n将处理 {len(themes)} 个主题:")
    for idx, theme in enumerate(themes, 1):
        print(f"  {idx}. {theme}")

    confirm = input("\n确认开始批量处理? (y/n): ").strip().lower()
    if confirm != 'y':
        print("已取消")
        return

    results = []
    for idx, theme in enumerate(themes, 1):
        print(f"\n{'='*60}")
        print(f"处理 {idx}/{len(themes)}: {theme}")
        print('='*60)

        result = publisher.full_workflow(theme)
        results.append({
            'theme': theme,
            'success': result.get('success', False),
            'message': result.get('message', '')
        })

    # 汇总结果
    print("\n" + "="*60)
    print("批量处理汇总".center(60))
    print("="*60)

    success_count = sum(1 for r in results if r['success'])
    print(f"\n总计: {len(results)} 个")
    print(f"成功: {success_count} 个")
    print(f"失败: {len(results) - success_count} 个")

    if results:
        print("\n详细结果:")
        for result in results:
            status = "[OK]" if result['success'] else "[FAIL]"
            print(f"  {status} {result['theme']}: {result['message']}")


def view_records():
    """查看发布记录"""
    import json
    from datetime import datetime

    print("\n" + "─"*50)
    print("发布记录")
    print("─"*50)

    records_dir = "publish_records"
    if not os.path.exists(records_dir):
        print("暂无发布记录")
        return

    # 查找最新的记录文件
    record_files = sorted(
        [f for f in os.listdir(records_dir) if f.endswith('.json')],
        reverse=True
    )

    if not record_files:
        print("暂无发布记录")
        return

    # 读取所有记录
    all_records = []
    for file in record_files:
        file_path = os.path.join(records_dir, file)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                records = json.load(f)
                all_records.extend(records)
        except Exception as e:
            logger.error(f"读取记录文件失败 {file}: {str(e)}")

    if not all_records:
        print("暂无发布记录")
        return

    # 显示记录
    print(f"\n共找到 {len(all_records)} 条记录\n")
    print("─"*50)

    for idx, record in enumerate(all_records[-10:], 1):  # 只显示最近10条
        status = "[OK] 成功" if record.get('status') == 'success' else "[FAIL] 失败"
        print(f"\n{idx}. {record.get('timestamp', 'N/A')}")
        print(f"   主题: {record.get('theme', 'N/A')}")
        print(f"   笔记ID: {record.get('note_id', 'N/A')}")
        print(f"   状态: {status}")
        print(f"   消息: {record.get('message', '')}")


def show_config():
    """显示系统配置"""
    print("\n" + "─"*50)
    print("系统配置")
    print("─"*50)

    print(f"\nAI Provider: {Config.AI_PROVIDER}")
    api_key = Config.get_current_api_key()
    print(f"API Key: {api_key[:10] if api_key else '未配置'}...")
    print(f"Model: {Config.get_current_model()}")

    print(f"\n小红书Access Token: {'已配置' if Config.XHS_ACCESS_TOKEN else '未配置'}")
    print(f"小红书App ID: {Config.XHS_APP_ID or '未配置'}")

    print(f"\n图片生成引擎: {Config.IMAGE_ENGINE}")
    if Config.IMAGE_ENGINE == 'stable-diffusion':
        print(f"Stable Diffusion API: {Config.STABLE_DIFFUSION_API_URL}")

    print(f"\n最大重试次数: {Config.MAX_RETRY_TIMES}")
    print(f"发布延迟(秒): {Config.PUBLISH_DELAY}")

    print("\n─"*50)


def main():
    """主函数"""
    print_banner()

    # 检查配置
    if not check_config():
        print("\n请先配置.env文件后再运行程序")
        print("\n参考步骤:")
        print("1. 复制 .env.example 为 .env")
        print("2. 编辑 .env 填入必要的配置项")
        print("3. 重新运行程序")
        return

    # 初始化系统
    try:
        publisher = XiaohongshuPublisher()
    except Exception as e:
        print(f"\n✗ 系统初始化失败: {str(e)}")
        logger.error(f"系统初始化失败: {str(e)}")
        return

    # 主循环
    while True:
        print_menu()
        choice = input("请选择操作 (1-6): ").strip()

        if choice == '1':
            quick_publish(publisher)

        elif choice == '2':
            preview_publish(publisher)

        elif choice == '3':
            batch_publish(publisher)

        elif choice == '4':
            view_records()

        elif choice == '5':
            show_config()

        elif choice == '6':
            print("\n感谢使用，再见！")
            break

        else:
            print("\n无效选项，请重新输入")

        # 暂停
        if choice != '6':
            input("\n按回车键继续...")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序已中断")
    except Exception as e:
        logger.error(f"程序异常: {str(e)}")
        print(f"\n程序异常: {str(e)}")
