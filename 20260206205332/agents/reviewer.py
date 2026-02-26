import re
from config import Config
from logger import logger
from ai_client import AIClient

class ContentReviewer:
    """审核智能体：检查内容合规性，格式化发布内容"""

    def __init__(self):
        self.ai_client = AIClient()
        self.model = self.ai_client.model
        self.sensitive_words = Config.SENSITIVE_WORDS

    def review_content(self, content: dict) -> dict:
        """
        审核内容，返回审核结果

        Args:
            content: 内容字典（包含theme, copy, image_paths等）

        Returns:
            dict: 审核结果
                {
                    'passed': bool,
                    'issues': list,
                    'warnings': list,
                    'suggestions': list
                }
        """
        logger.info("开始内容审核")

        result = {
            'passed': True,
            'issues': [],
            'warnings': [],
            'suggestions': []
        }

        # 1. 敏感词检测
        sensitive_issues = self._check_sensitive_words(content.get('copy', ''))
        result['issues'].extend(sensitive_issues)

        # 2. 内容质量检测
        quality_issues = self._check_content_quality(content.get('copy', ''))
        result['issues'].extend(quality_issues)

        # 3. 图片合规检查
        image_warnings = self._check_images(content.get('image_paths', []))
        result['warnings'].extend(image_warnings)

        # 4. 使用AI进行深度审核
        ai_review = self._ai_review(content)
        result['issues'].extend(ai_review['issues'])
        result['warnings'].extend(ai_review['warnings'])
        result['suggestions'].extend(ai_review['suggestions'])

        # 判断是否通过
        result['passed'] = len(result['issues']) == 0

        logger.info(f"审核完成，结果: {'通过' if result['passed'] else '不通过'}")
        return result

    def _check_sensitive_words(self, text: str) -> list:
        """检测敏感词"""
        issues = []

        for word in self.sensitive_words:
            if word in text:
                issues.append(f"发现敏感词: {word}")
                logger.warning(f"发现敏感词: {word}")

        return issues

    def _check_content_quality(self, copy: str) -> list:
        """检查内容质量"""
        issues = []

        # 检查文案长度
        if len(copy) < 100:
            issues.append("文案过短，建议至少100字")
        elif len(copy) > 1000:
            issues.append("文案过长，建议控制在1000字以内")

        # 检查话题标签数量
        hashtag_count = len(re.findall(r'#\w+', copy))
        if hashtag_count < 3:
            issues.append("话题标签过少，建议至少3个")
        elif hashtag_count > 10:
            issues.append("话题标签过多，建议不超过10个")

        # 检查emoji使用
        emoji_count = len(re.findall(r'[^\w\s]', copy))
        if emoji_count < 2:
            issues.append("emoji使用过少，建议增加")

        return issues

    def _check_images(self, image_paths: list) -> list:
        """检查图片"""
        warnings = []

        if not image_paths:
            warnings.append("未添加图片")
        elif len(image_paths) > 9:
            warnings.append("图片数量超过9张，小红书最多支持9张")

        return warnings

    def _ai_review(self, content: dict) -> dict:
        """使用AI进行深度审核"""
        result = {
            'issues': [],
            'warnings': [],
            'suggestions': []
        }

        prompt = f"""
请审核以下小红书内容：

主题：{content.get('theme', '')}

文案：
{content.get('copy', '')}

请从以下维度审核：
1. 内容是否违规（色情、暴力、虚假宣传等）
2. 是否包含敏感信息
3. 内容质量建议
4. 格式建议

请以JSON格式返回，格式如下：
{{
    "issues": ["问题1", "问题2"],
    "warnings": ["警告1", "警告2"],
    "suggestions": ["建议1", "建议2"]
}}

如果内容没有问题，issues和warnings数组为空即可。
"""

        try:
            use_json_format = self.ai_client.provider in ['openai', 'deepseek']

            kwargs = {
                "messages": [
                    {"role": "system", "content": "你是一个专业的内容审核专家，熟悉平台规则和内容规范。"},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.3
            }

            if use_json_format:
                kwargs["response_format"] = {"type": "json_object"}

            response = self.ai_client.chat_completion(**kwargs)

            ai_result = eval(response.choices[0].message.content)
            result['issues'].extend(ai_result.get('issues', []))
            result['warnings'].extend(ai_result.get('warnings', []))
            result['suggestions'].extend(ai_result.get('suggestions', []))

            logger.info("AI审核完成")

        except Exception as e:
            logger.error(f"AI审核失败: {str(e)}")

        return result

    def format_for_publish(self, content: dict) -> dict:
        """
        格式化内容以便发布

        Args:
            content: 原始内容字典

        Returns:
            dict: 格式化后的内容
        """
        logger.info("格式化发布内容")

        formatted = {
            'title': self._extract_title(content.get('copy', '')),
            'content': content.get('copy', ''),
            'images': content.get('image_paths', []),
            'hashtags': self._extract_hashtags(content.get('copy', '')),
            'summary': self._generate_summary(content.get('copy', ''))
        }

        return formatted

    def _extract_title(self, copy: str) -> str:
        """提取标题（第一行）"""
        lines = copy.strip().split('\n')
        return lines[0] if lines else copy[:50]

    def _extract_hashtags(self, copy: str) -> list:
        """提取话题标签"""
        hashtags = re.findall(r'#\w+', copy)
        return list(set(hashtags))

    def _generate_summary(self, copy: str) -> str:
        """生成摘要"""
        # 移除话题标签和emoji
        clean_text = re.sub(r'#\w+', '', copy)
        clean_text = re.sub(r'[^\w\s\u4e00-\u9fff]', '', clean_text)

        # 取前100字作为摘要
        return clean_text[:100].strip()

    def fix_issues(self, content: dict, issues: list) -> dict:
        """
        自动修复部分问题

        Args:
            content: 原始内容
            issues: 问题列表

        Returns:
            dict: 修复后的内容
        """
        logger.info(f"尝试修复{len(issues)}个问题")

        fixed_content = content.copy()

        for issue in issues:
            if "话题标签过少" in issue:
                fixed_content['copy'] = self._add_hashtags(fixed_content['copy'])
            elif "emoji使用过少" in issue:
                fixed_content['copy'] = self._add_emojis(fixed_content['copy'])

        return fixed_content

    def _add_hashtags(self, copy: str) -> str:
        """添加话题标签"""
        additional_tags = " #生活记录 #分享 #日常"
        return copy + additional_tags

    def _add_emojis(self, copy: str) -> str:
        """添加emoji"""
        emojis = " ✨💡"
        return copy + emojis
