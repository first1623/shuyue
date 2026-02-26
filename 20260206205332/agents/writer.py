from config import Config
from logger import logger
from ai_client import AIClient

class CopyWriter:
    """文案智能体：根据策略生成小红书风格文案"""

    def __init__(self):
        self.ai_client = AIClient()
        self.model = self.ai_client.model

    def generate_copy(self, theme: str, strategy: dict) -> str:
        """
        根据主题和策略生成小红书文案

        Args:
            theme: 主题
            strategy: 内容策略字典

        Returns:
            str: 生成的文案内容
        """
        logger.info(f"文案智能体开始生成文案，主题: {theme}")

        prompt = f"""
作为一个小红书爆款文案写手，请根据以下信息创作一篇吸引人的笔记文案：

主题：{theme}

内容策略：
- 目标人群：{strategy.get('target_audience', '20-35岁女性')}
- 内容角度：{', '.join(strategy.get('content_angles', ['实用技巧']))}
- 关键词：{', '.join(strategy.get('keywords', []))}
- 文案风格：{strategy.get('tone', '亲切自然，带emoji')}
- Emoji推荐：{' '.join(strategy.get('emojis', ['✨', '💡']))}

文案要求：
1. 标题要吸睛，使用emoji和数字
2. 正文采用"3点法则"，分点阐述核心内容
3. 语言口语化，亲切自然
4. 适当使用emoji增加趣味性
5. 结尾引导互动（点赞、收藏、评论）
6. 包含8-10个相关话题标签

请直接输出文案内容，不要添加其他说明文字。
"""

        try:
            response = self.ai_client.chat_completion(
                messages=[
                    {"role": "system", "content": "你是一个擅长创作小红书爆款文案的专家，深谙用户心理和平台算法。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=1000
            )

            copywriting = response.choices[0].message.content.strip()
            logger.info(f"文案生成成功，长度: {len(copywriting)}")
            return copywriting

        except Exception as e:
            logger.error(f"文案生成失败: {str(e)}")
            return self._get_default_copy(theme, strategy)

    def _get_default_copy(self, theme: str, strategy: dict) -> str:
        """获取默认文案模板"""
        emojis = strategy.get('emojis', ['✨', '💡', '❤️'])
        keywords = strategy.get('keywords', [f'#{theme}', '#生活小技巧', '#好物推荐'])

        copy = f"""
{theme}的3个必备技巧！{emojis[0]}

▪️ 第一点：实用建议
关于{theme}，最重要的是掌握基础方法。从简单开始，循序渐进，你会发现意想不到的效果！

▪️ 第二点：避坑指南
在实践过程中，记得避免常见错误。保持耐心，多观察多总结，这样才能快速进步~

▪️ 第三点：升级方案
想要更进一步？试试这些小技巧，让你的{theme}体验提升一个档次！{emojis[1]}

最后，一定要根据自己情况调整哦~ 有问题欢迎评论区交流！{emojis[2]}

{' '.join(keywords[:8])}
"""
        return copy.strip()

    def rewrite_copy(self, original_copy: str, feedback: str, strategy: dict) -> str:
        """
        根据用户反馈重写文案

        Args:
            original_copy: 原始文案
            feedback: 用户反馈
            strategy: 内容策略

        Returns:
            str: 重写后的文案
        """
        logger.info(f"根据反馈重写文案: {feedback}")

        prompt = f"""
请根据以下反馈重写文案：

原始文案：
{original_copy}

用户反馈：{feedback}

保持小红书风格，优化内容后直接输出文案。
"""

        try:
            response = self.ai_client.chat_completion(
                messages=[
                    {"role": "system", "content": "你是一个小红书文案编辑专家。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=1000
            )

            rewritten_copy = response.choices[0].message.content.strip()
            logger.info(f"文案重写成功")
            return rewritten_copy

        except Exception as e:
            logger.error(f"文案重写失败: {str(e)}")
            return original_copy

    def generate_titles(self, theme: str, count: int = 5) -> list:
        """
        生成多个标题选项

        Args:
            theme: 主题
            count: 标题数量

        Returns:
            list: 标题列表
        """
        prompt = f"""
为主题"{theme}"生成{count}个吸引人的小红书标题。

要求：
1. 使用emoji
2. 包含数字
3. 语言口语化
4. 每个标题不超过20字

请直接输出标题列表，每行一个。
"""

        try:
            response = self.ai_client.chat_completion(
                messages=[
                    {"role": "system", "content": "你是一个小红书标题创作专家。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.9,
                max_tokens=500
            )

            titles = response.choices[0].message.content.strip().split('\n')
            return [title.strip() for title in titles if title.strip()]

        except Exception as e:
            logger.error(f"标题生成失败: {str(e)}")
            return [
                f"{theme}✨5个实用技巧",
                f"搞定{theme}的3个方法💡",
                f"关于{theme}你必须知道的事",
                f"{theme}新手必看指南",
                f"如何快速掌握{theme}？"
            ][:count]
