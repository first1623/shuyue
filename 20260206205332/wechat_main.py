#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号多智能体内容生成与发布系统
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

from agents.planner import ContentPlanner
from agents.designer import ImageDesigner
from agents.reviewer import ContentReviewer
from agents.wechat_writer import WeChatArticleWriter
from agents.wechat_publisher import WeChatPublisher
from logger import logger
from config import Config
from typing import Dict

class WeChatContentSystem:
    """微信公众号内容生成与发布系统"""

    def __init__(self):
        """初始化系统"""
        logger.info("初始化微信公众号发布系统")

        self.agents = {
            'planner': ContentPlanner(),
            'writer': WeChatArticleWriter(),
            'designer': ImageDesigner(),
            'reviewer': ContentReviewer(),
            'publisher': WeChatPublisher()
        }

        self.current_content = None

    def process_theme(self, theme: str) -> Dict:
        """
        多智能体协同工作流：处理主题生成公众号文章

        Args:
            theme: 用户输入的主题

        Returns:
            dict: 生成的内容包
        """
        logger.info(f"开始处理主题: {theme}")
        print(f"\n{'='*50}")
        print(f"正在处理主题: {theme}")
        print(f"{'='*50}\n")

        content_package = {
            'theme': theme,
            'strategy': None,
            'article': None,
            'image_prompts': None,
            'image_paths': [],
            'review_result': None
        }

        try:
            # 1. 策划阶段
            print("【策划】分析主题...")
            strategy = self.agents['planner'].analyze_theme(theme)
            content_package['strategy'] = strategy
            print(f"完成：目标人群 {strategy.get('target_audience')}\n")

            # 2. 文章生成阶段
            print("【写作】生成公众号文章...")
            article = self.agents['writer'].generate_article(theme, strategy)
            content_package['article'] = article
            print(f"完成：标题《{article['title']}》\n")
            print(f"内容预览：{article['digest']}\n")

            # 3. 图片生成阶段（可选）
            print("【配图】生成配图（可选）...")
            print("提示：已跳过图片生成\n")
            # Web 模式下跳过图片生成
            content_package['image_prompts'] = []
            content_package['image_paths'] = []

            # 4. 内容审核阶段
            print("【审核】检查文章内容...")
            review_result = self.agents['reviewer'].review_content(content_package)
            content_package['review_result'] = review_result

            if review_result['passed']:
                print("审核通过\n")
            else:
                print("审核未通过:")
                for issue in review_result['issues']:
                    print(f"  - {issue}")
                print()

            return content_package

        except Exception as e:
            logger.error(f"处理主题失败: {str(e)}")
            raise

    def publish(self, content_package: Dict) -> Dict:
        """
        发布文章到微信公众号

        Args:
            content_package: 内容包

        Returns:
            dict: 发布结果
        """
        logger.info("开始发布公众号文章")

        try:
            article = content_package['article']

            # 准备发布内容
            publish_content = {
                'theme': content_package['theme'],
                'title': article['title'],
                'content': article['content'],
                'digest': article['digest'],
                'author': article['author'],
                'show_cover_pic': 0,  # 默认不显示封面，除非有上传
                'need_open_comment': 1,
                'only_fans_can_comment': 0
            }

            # 如果有封面图，上传并设置
            if content_package.get('image_paths'):
                image_path = content_package['image_paths'][0]
                print(f"\n正在上传封面图: {image_path}")
                # 上传图片到微信服务器
                media_id = self.agents['publisher']._upload_image(image_path)
                if media_id:
                    publish_content['thumb_media_id'] = media_id
                    publish_content['show_cover_pic'] = 1
                    print("封面图上传成功")
                else:
                    print("封面图上传失败，将不显示封面")

            # 发布文章
            result = self.agents['publisher'].publish_article(publish_content)

            # 保存发布记录
            if result.get('success'):
                self.agents['publisher'].save_publish_record(
                    publish_content,
                    result
                )

            return result

        except Exception as e:
            logger.error(f"发布失败: {str(e)}")
            return {
                'success': False,
                'media_id': None,
                'article_id': None,
                'message': f'发布失败: {str(e)}'
            }

    def display_content_preview(self, content_package: Dict):
        """显示内容预览"""
        article = content_package['article']

        print("\n" + "="*50)
        print("文章预览")
        print("="*50)
        print(f"\n标题：{article['title']}")
        print(f"作者：{article['author']}")
        print(f"摘要：{article['digest']}")
        print(f"\n关键词：{', '.join(article['keywords'])}")
        print("\n" + "-"*50)
        print("正文内容（HTML）：")
        print("-"*50)
        print(article['content'])
        print("="*50)

    def full_workflow(self, theme: str) -> Dict:
        """完整工作流：生成并发布"""
        try:
            # 生成内容
            content_package = self.process_theme(theme)

            # 发布
            print("\n【发布】上传文章到公众号...")
            result = self.publish(content_package)

            # 显示结果
            print("\n" + "="*50)
            print("发布结果")
            print("="*50)
            if result.get('success'):
                print(f"成功：{result['message']}")
                print(f"文章ID：{result.get('media_id', 'N/A')}")
            else:
                print(f"失败：{result['message']}")
            print("="*50)

            return result

        except Exception as e:
            logger.error(f"完整工作流失败: {str(e)}")
            return {
                'success': False,
                'message': f'流程失败: {str(e)}'
            }


def print_banner():
    """打印欢迎横幅"""
    banner = """
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║        微信公众号多智能体内容生成与发布系统                ║
║                                                            ║
║           Multi-Agent WeChat Publisher                     ║
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
  2. 生成预览 - 生成文章后确认
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
        # 检查AI配置
        api_key = Config.get_current_api_key()
        if not api_key:
            print("[WARN] 未配置API Key")
            print("  请在.env文件中设置对应的API_KEY")
            return False

        print(f"[OK] {Config.AI_PROVIDER.upper()} API Key: {api_key[:10]}...")

        # 检查微信公众号配置
        if Config.WECHAT_APP_ID:
            print(f"[OK] 微信公众号APP_ID: {Config.WECHAT_APP_ID}")
        else:
            print("[WARN] 微信公众号未配置")
            print("  请在.env文件中设置 WECHAT_APP_ID 和 WECHAT_APP_SECRET")

        return True

    except ValueError as e:
        print(f"[ERROR] 配置错误: {e}")
        return False


def quick_publish(system):
    """快速发布模式"""
    print("\n" + "─"*50)
    print("快速发布模式")
    print("─"*50)

    theme = input("\n请输入文章主题: ").strip()
    if not theme:
        print("主题不能为空")
        return

    result = system.full_workflow(theme)
    return result


def preview_publish(system):
    """预览发布模式"""
    print("\n" + "─"*50)
    print("预览发布模式")
    print("─"*50)

    theme = input("\n请输入文章主题: ").strip()
    if not theme:
        print("主题不能为空")
        return

    # 生成内容
    try:
        content_package = system.process_theme(theme)

        # 展示预览
        system.display_content_preview(content_package)

        # 询问是否发布
        choice = input("\n是否立即发布到公众号？(y/n): ").strip().lower()
        if choice == 'y':
            print("\n正在上传文章...")
            result = system.publish(content_package)
            print(f"\n发布结果: {result.get('message', 'Unknown')}")
        else:
            print("已取消发布")

    except Exception as e:
        print(f"错误: {str(e)}")


def batch_publish(system):
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

    confirm = input("\n确认开始批量处理？(y/n): ").strip().lower()
    if confirm != 'y':
        print("已取消")
        return

    results = []
    for idx, theme in enumerate(themes, 1):
        print(f"\n{'='*60}")
        print(f"处理 {idx}/{len(themes)}: {theme}")
        print('='*60)

        result = system.full_workflow(theme)
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
    import glob

    print("\n" + "─"*50)
    print("发布记录")
    print("─"*50)

    records_dir = "wechat_publish_records"
    if not os.path.exists(records_dir):
        print("暂无发布记录")
        return

    # 查找最新的记录文件
    record_files = sorted(
        glob.glob(os.path.join(records_dir, "*.json")),
        reverse=True
    )

    if not record_files:
        print("暂无发布记录")
        return

    # 读取所有记录
    all_records = []
    for file in record_files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
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
        print(f"   标题: {record.get('title', 'N/A')}")
        print(f"   文章ID: {record.get('media_id', 'N/A')}")
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

    print(f"\n微信公众号APP_ID: {Config.WECHAT_APP_ID or '未配置'}")
    print(f"微信公众号APP_SECRET: {'已配置' if Config.WECHAT_APP_SECRET else '未配置'}")

    print(f"\n图片生成引擎: {Config.IMAGE_ENGINE}")

    print("\n─"*50)


def main():
    """主函数"""
    print_banner()

    # 检查配置
    if not check_config():
        print("\n请先配置.env文件后再运行程序")
        return

    # 初始化系统
    try:
        system = WeChatContentSystem()
    except Exception as e:
        print(f"\n系统初始化失败: {str(e)}")
        logger.error(f"系统初始化失败: {str(e)}")
        return

    # 主循环
    while True:
        print_menu()
        choice = input("请选择操作 (1-6): ").strip()

        if choice == '1':
            quick_publish(system)

        elif choice == '2':
            preview_publish(system)

        elif choice == '3':
            batch_publish(system)

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
