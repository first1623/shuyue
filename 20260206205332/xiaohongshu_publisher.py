from agents.planner import ContentPlanner
from agents.writer import CopyWriter
from agents.designer import ImageDesigner
from agents.reviewer import ContentReviewer
from agents.publisher import APIPublisher
from logger import logger
from typing import Dict, Optional

class XiaohongshuPublisher:
    """小红书内容生成与发布系统"""

    def __init__(self):
        """初始化系统"""
        logger.info("初始化小红书发布系统")

        self.agents = {
            'planner': ContentPlanner(),
            'writer': CopyWriter(),
            'designer': ImageDesigner(),
            'reviewer': ContentReviewer(),
            'publisher': APIPublisher()
        }

        self.current_content = None

    def process_theme(self, theme: str) -> Dict:
        """
        多智能体协同工作流：处理主题生成内容

        Args:
            theme: 用户输入的主题

        Returns:
            dict: 生成的内容包
                {
                    'theme': str,
                    'strategy': dict,
                    'copy': str,
                    'image_prompts': list,
                    'image_paths': list,
                    'review_result': dict
                }
        """
        logger.info(f"开始处理主题: {theme}")
        print(f"\n{'='*50}")
        print(f"正在处理主题: {theme}")
        print(f"{'='*50}\n")

        content_package = {
            'theme': theme,
            'strategy': None,
            'copy': None,
            'image_prompts': None,
            'image_paths': [],
            'review_result': None
        }

        try:
            # 1. 策划阶段
            print("📋 策划智能体正在分析主题...")
            strategy = self.agents['planner'].analyze_theme(theme)
            content_package['strategy'] = strategy
            print(f"✓ 策划完成：目标人群 {strategy.get('target_audience')}\n")

            # 2. 文案生成阶段
            print("✍️  文案智能体正在生成文案...")
            copy = self.agents['writer'].generate_copy(theme, strategy)
            content_package['copy'] = copy
            print(f"✓ 文案生成完成（{len(copy)}字）\n")

            # 3. 图片生成阶段
            print("🎨 图片智能体正在生成配图...")
            image_prompts = self.agents['designer'].generate_image_prompts(
                theme, copy, strategy
            )
            content_package['image_prompts'] = image_prompts

            print(f"✓ 生成{len(image_prompts)}个图片提示词:")
            for idx, prompt in enumerate(image_prompts):
                print(f"  {idx+1}. {prompt[:50]}...")

            print(f"\n正在生成图片...")
            image_paths = self.agents['designer'].generate_images(image_prompts)
            content_package['image_paths'] = image_paths
            print(f"✓ 成功生成{len(image_paths)}张图片\n")

            # 4. 内容审核阶段
            print("🔍 审核智能体正在检查内容...")
            review_result = self.agents['reviewer'].review_content(content_package)
            content_package['review_result'] = review_result

            if review_result['passed']:
                print(f"✓ 审核通过")
            else:
                print(f"✗ 审核未通过:")
                for issue in review_result['issues']:
                    print(f"  - {issue}")

            if review_result['suggestions']:
                print(f"\n💡 优化建议:")
                for suggestion in review_result['suggestions']:
                    print(f"  - {suggestion}")

            print(f"\n{'='*50}")
            print("内容生成完成！")
            print(f"{'='*50}\n")

            self.current_content = content_package
            return content_package

        except Exception as e:
            logger.error(f"内容生成失败: {str(e)}")
            print(f"✗ 内容生成失败: {str(e)}\n")
            raise

    def confirm_content(self, content_package: Dict) -> bool:
        """
        确认内容是否需要修改

        Args:
            content_package: 内容包

        Returns:
            bool: 是否确认发布
        """
        self.display_content_preview(content_package)

        while True:
            choice = input("\n请选择操作:\n"
                          "1. 确认发布\n"
                          "2. 修改文案\n"
                          "3. 重新生成图片\n"
                          "4. 放弃\n"
                          "请输入选项 (1-4): ").strip()

            if choice == '1':
                return True
            elif choice == '2':
                self._edit_copy(content_package)
            elif choice == '3':
                self._regenerate_images(content_package)
            elif choice == '4':
                return False
            else:
                print("无效选项，请重新输入")

    def display_content_preview(self, content_package: Dict):
        """展示内容预览"""
        print("\n" + "="*60)
        print("📝 内容预览".center(60))
        print("="*60)

        print(f"\n主题：{content_package['theme']}")

        print("\n📋 策略信息：")
        strategy = content_package.get('strategy', {})
        print(f"  - 目标人群: {strategy.get('target_audience', 'N/A')}")
        print(f"  - 内容角度: {', '.join(strategy.get('content_angles', []))}")
        print(f"  - 最佳发布时间: {strategy.get('best_time', 'N/A')}")

        print("\n✍️  文案内容：")
        print("-"*60)
        print(content_package['copy'])
        print("-"*60)

        print(f"\n🎨 配图：")
        image_paths = content_package.get('image_paths', [])
        if image_paths:
            for idx, path in enumerate(image_paths):
                print(f"  {idx+1}. {path}")
        else:
            print("  未生成图片")

        print("\n🔍 审核结果：")
        review = content_package.get('review_result', {})
        if review.get('passed'):
            print("  ✓ 审核通过")
        else:
            print("  ✗ 审核未通过")
            for issue in review.get('issues', []):
                print(f"    - {issue}")

        if review.get('suggestions'):
            print("\n💡 优化建议：")
            for suggestion in review.get('suggestions', []):
                print(f"  - {suggestion}")

        print("="*60)

    def _edit_copy(self, content_package: Dict):
        """修改文案"""
        print("\n当前文案：")
        print(content_package['copy'])

        print("\n修改选项:")
        print("1. 手动修改文案")
        print("2. 让AI重新生成")
        print("3. 返回")

        choice = input("请选择 (1-3): ").strip()

        if choice == '1':
            new_copy = input("\n请输入新文案（直接回车保持原样）: ").strip()
            if new_copy:
                content_package['copy'] = new_copy
                print("✓ 文案已更新")

        elif choice == '2':
            feedback = input("请输入修改建议: ").strip()
            if feedback:
                strategy = content_package.get('strategy', {})
                new_copy = self.agents['writer'].rewrite_copy(
                    content_package['copy'],
                    feedback,
                    strategy
                )
                content_package['copy'] = new_copy
                print("✓ 文案已重新生成")

    def _regenerate_images(self, content_package: Dict):
        """重新生成图片"""
        print("\n重新生成图片选项:")
        print("1. 修改所有图片")
        print("2. 修改指定图片")

        choice = input("请选择 (1-2): ").strip()

        if choice == '1':
            # 重新生成所有图片
            prompts = content_package.get('image_prompts', [])
            if prompts:
                print(f"\n当前提示词:")
                for idx, prompt in enumerate(prompts):
                    print(f"{idx+1}. {prompt}")

                print("\n是否修改提示词？(y/n)")
                if input().lower() == 'y':
                    new_prompt = input("输入新提示词（留空保持）: ")
                    if new_prompt:
                        prompts = [new_prompt]

                new_paths = self.agents['designer'].generate_images(prompts)
                content_package['image_paths'] = new_paths
                print("✓ 图片已重新生成")

        elif choice == '2':
            paths = content_package.get('image_paths', [])
            if paths:
                print("\n当前图片:")
                for idx, path in enumerate(paths):
                    print(f"{idx+1}. {path}")

                idx = int(input("\n选择要重新生成的图片编号: ")) - 1
                if 0 <= idx < len(paths):
                    new_prompt = input("输入新提示词: ")
                    if new_prompt:
                        new_path = self.agents['designer'].regenerate_image(
                            paths[idx],
                            new_prompt
                        )
                        content_package['image_paths'][idx] = new_path
                        print("✓ 图片已重新生成")

    def publish(self, content_package: Dict) -> Dict:
        """
        发布内容到小红书

        Args:
            content_package: 内容包

        Returns:
            dict: 发布结果
        """
        print("\n" + "="*60)
        print("🚀 开始发布...".center(60))
        print("="*60 + "\n")

        try:
            # 格式化内容
            formatted_content = self.agents['reviewer'].format_for_publish(
                content_package
            )

            # 发布
            result = self.agents['publisher'].publish_post(formatted_content)

            # 保存记录
            if result.get('success'):
                self.agents['publisher'].save_publish_record(
                    formatted_content,
                    result
                )

            return result

        except Exception as e:
            logger.error(f"发布失败: {str(e)}")
            return {
                'success': False,
                'note_id': None,
                'message': f'发布失败: {str(e)}'
            }

    def full_workflow(self, theme: str) -> Dict:
        """
        完整工作流：生成 → 确认 → 发布

        Args:
            theme: 主题

        Returns:
            dict: 最终结果
        """
        try:
            # 生成内容
            content_package = self.process_theme(theme)

            # 确认内容
            if self.confirm_content(content_package):
                # 发布
                result = self.publish(content_package)

                print(f"\n{'='*60}")
                if result.get('success'):
                    print(f"🎉 发布成功！".center(60))
                    print(f"笔记ID: {result.get('note_id')}".center(60))
                else:
                    print(f"❌ 发布失败: {result.get('message')}".center(60))
                print("="*60 + "\n")

                return result
            else:
                print("\n已取消发布")
                return {'success': False, 'message': '用户取消'}

        except Exception as e:
            logger.error(f"工作流执行失败: {str(e)}")
            print(f"\n✗ 执行失败: {str(e)}")
            return {'success': False, 'message': str(e)}
