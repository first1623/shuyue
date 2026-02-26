from config import Config
from logger import logger
from ai_client import AIClient

class ContentPlanner:
    """策划智能体：分析主题，生成内容策略"""

    def __init__(self):
        self.ai_client = AIClient()
        self.model = self.ai_client.model

    def analyze_theme(self, theme: str) -> dict:
        """
        分析主题，生成内容策略

        Args:
            theme: 用户输入的主题

        Returns:
            dict: 内容策略字典
        """
        logger.info(f"策划智能体开始分析主题: {theme}")

        prompt = f"""
作为一个小红书内容策划专家，请分析以下主题并制定内容策略：

主题：{theme}

请从以下维度分析：
1. 目标人群：明确受众画像（年龄、性别、兴趣等）
2. 内容角度：选择3-4个最适合的内容切入角度（如实用技巧、情感共鸣、好物分享等）
3. 关键词：生成8-10个相关话题标签，包括主标签和长尾标签
4. 文案风格：确定语调风格（亲切自然、专业严谨、活泼可爱等）
5. emoji使用：推荐适合的emoji表情
6. 最佳发布时间：建议发布时间段

请以JSON格式返回，格式如下：
{{
    "target_audience": "25-35岁女性",
    "content_angles": ["实用技巧", "情感共鸣", "好物分享"],
    "keywords": ["#生活方式", "#好物推荐", "#生活小技巧"],
    "tone": "亲切自然，带emoji",
    "emojis": ["✨", "💡", "❤️"],
    "best_time": "18:00-22:00",
    "content_type": "干货分享"
}}
"""

        try:
            import concurrent.futures
            
            # 某些API不支持json_object格式，使用普通格式
            use_json_format = self.ai_client.provider in ['openai', 'deepseek']

            kwargs = {
                "messages": [
                    {"role": "system", "content": "你是一个专业的小红书内容策划专家，擅长分析热点和制定爆款内容策略。"},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 1000
            }

            if use_json_format:
                kwargs["response_format"] = {"type": "json_object"}

            def call_ai():
                return self.ai_client.chat_completion(**kwargs)
            
            # 设置30秒超时
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(call_ai)
                response = future.result(timeout=30)

            strategy = eval(response.choices[0].message.content)
            logger.info(f"内容策略生成成功: {strategy}")
            return strategy

        except Exception as e:
            logger.error(f"内容策略生成失败: {str(e)}")
            # 返回默认策略
            return self._get_default_strategy(theme)

    def _get_default_strategy(self, theme: str) -> dict:
        """获取默认内容策略"""
        return {
            "target_audience": "20-35岁女性",
            "content_angles": ["实用技巧", "好物分享", "生活美学"],
            "keywords": [f"#{theme}", "#生活小技巧", "#好物推荐", "#生活方式"],
            "tone": "亲切自然，带emoji",
            "emojis": ["✨", "💡", "❤️"],
            "best_time": "18:00-22:00",
            "content_type": "干货分享"
        }

    def refine_strategy(self, theme: str, user_feedback: str) -> dict:
        """
        根据用户反馈优化内容策略

        Args:
            theme: 原始主题
            user_feedback: 用户反馈意见

        Returns:
            dict: 优化后的内容策略
        """
        logger.info(f"根据用户反馈优化策略: {user_feedback}")

        prompt = f"""
基于以下内容策略和用户反馈，优化内容策略：

原始主题：{theme}
用户反馈：{user_feedback}

请调整策略并返回优化后的JSON格式内容。
"""

        try:
            use_json_format = self.ai_client.provider in ['openai', 'deepseek']

            kwargs = {
                "messages": [
                    {"role": "system", "content": "你是一个专业的小红书内容策划专家。"},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7
            }

            if use_json_format:
                kwargs["response_format"] = {"type": "json_object"}

            response = self.ai_client.chat_completion(**kwargs)

            refined_strategy = eval(response.choices[0].message.content)
            logger.info(f"策略优化成功")
            return refined_strategy

        except Exception as e:
            logger.error(f"策略优化失败: {str(e)}")
            return self._get_default_strategy(theme)
