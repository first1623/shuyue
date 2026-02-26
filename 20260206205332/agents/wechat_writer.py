from config import Config
from logger import logger
from ai_client import AIClient

class WeChatArticleWriter:
    """微信公众号文章写作智能体"""

    def __init__(self):
        self.ai_client = AIClient()
        self.model = self.ai_client.model

    def generate_article(self, theme: str, strategy: dict) -> dict:
        """
        生成微信公众号文章

        Args:
            theme: 主题
            strategy: 内容策略字典

        Returns:
            dict: 文章内容
                {
                    'title': str,
                    'content': str,  # HTML格式
                    'digest': str,   # 摘要
                    'author': str,
                    'keywords': list
                }
        """
        logger.info(f"开始生成公众号文章，主题: {theme}")

        # 生成标题
        title = self._generate_title(theme, strategy)

        # 生成正文
        content = self._generate_content(theme, strategy, title)

        # 生成摘要
        digest = self._generate_digest(content)

        # 提取关键词
        keywords = strategy.get('keywords', [])

        return {
            'title': title,
            'content': content,
            'digest': digest,
            'author': strategy.get('author', '小助手'),
            'keywords': keywords
        }

    def _generate_title(self, theme: str, strategy: dict) -> str:
        """生成文章标题"""
        target_audience = strategy.get('target_audience', '所有读者')
        content_type = strategy.get('content_type', '干货分享')

        prompt = f"""
作为微信公众号标题专家，请为以下内容生成5个吸引人的标题：

主题：{theme}
目标读者：{target_audience}
内容类型：{content_type}

标题要求：
1. 字数控制在15-25字之间
2. 使用疑问句或感叹句增加吸引力
3. 包含数字或关键词
4. 突出价值点和痛点
5. 符合公众号调性，不夸大不标题党

请直接输出5个标题，每行一个，不要添加其他内容。
"""

        try:
            import concurrent.futures
            
            def call_ai():
                return self.ai_client.chat_completion(
                    messages=[{'role': 'user', 'content': prompt}],
                    max_tokens=500
                )
            
            # 设置30秒超时
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(call_ai)
                response = future.result(timeout=30)
            
            # 提取响应文本
            content = response.choices[0].message.content
            titles = content.strip().split('\n')
            # 返回第一个标题
            return titles[0].strip() if titles else theme
        except concurrent.futures.TimeoutError:
            logger.error("生成标题超时")
            return f"关于{theme}的深度解析"
        except Exception as e:
            logger.error(f"生成标题失败: {str(e)}")
            return f"关于{theme}的深度解析"

    def _generate_content(self, theme: str, strategy: dict, title: str) -> str:
        """生成文章正文（HTML格式）"""
        target_audience = strategy.get('target_audience', '所有读者')
        content_angles = ', '.join(strategy.get('content_angles', ['深度分析']))
        keywords = ', '.join(strategy.get('keywords', []))
        tone = strategy.get('tone', '专业、亲切、有深度')

        prompt = f"""
作为微信公众号文章写作专家，请创作一篇高质量文章：

主题：{theme}
标题：{title}
目标读者：{target_audience}
内容角度：{content_angles}
关键词：{keywords}
写作风格：{tone}

文章结构要求：
1. 开头：用故事或问题引入，吸引读者
2. 正文：分2-3个小节，每节一个小标题
3. 内容：有干货、有案例、有观点
4. 结尾：总结升华，引导关注
5. 字数：500-800字（简洁精炼）

格式要求：
- 输出HTML格式
- 使用<h2>标签做小标题
- 使用<p>标签做段落
- 适当使用<strong>强调重点
- 段落之间用<br>分隔

请直接输出HTML格式的内容，不要添加其他说明。
"""

        try:
            import concurrent.futures
            
            def call_ai():
                return self.ai_client.chat_completion(
                    messages=[{'role': 'user', 'content': prompt}],
                    max_tokens=2000
                )
            
            # 设置60秒超时
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(call_ai)
                response = future.result(timeout=60)
            
            # 提取响应文本
            content = response.choices[0].message.content
            return content.strip()
        except concurrent.futures.TimeoutError:
            logger.error("生成正文超时")
            return self._get_fallback_content(title, theme)
        except Exception as e:
            logger.error(f"生成正文失败: {str(e)}")
            return self._get_fallback_content(title, theme)

    def _get_fallback_content(self, title: str, theme: str) -> str:
        """获取备用内容"""
        return f"""<h2>{title}</h2>
<p>亲爱的读者，今天我们来聊聊<strong>{theme}</strong>这个话题。</p>
<br>
<h2>为什么会出现这个问题</h2>
<p>在生活中，我们经常会遇到各种各样的挑战。了解问题的根源，是解决问题的第一步。</p>
<br>
<h2>实用的解决方法</h2>
<p>1. <strong>保持冷静</strong>：遇到问题时，先深呼吸，让自己平静下来。</p>
<p>2. <strong>分析原因</strong>：找出问题的根本原因，而不是只看表面。</p>
<p>3. <strong>寻求帮助</strong>：必要时可以向专业人士或身边的朋友寻求建议。</p>
<br>
<h2>写在最后</h2>
<p>希望这篇文章对你有所帮助。如果你觉得有价值，欢迎分享给更多需要的人。</p>
<p>关注我们，获取更多实用内容！</p>"""

    def _generate_digest(self, content: str) -> str:
        """生成文章摘要"""
        # 提取纯文本
        import re
        text = re.sub(r'<[^>]+>', '', content)
        text = text.strip()

        # 清理空白字符
        text = re.sub(r'\s+', ' ', text)

        # 取前120字作为摘要
        if len(text) > 120:
            digest = text[:117] + '...'
        else:
            digest = text

        # 摘要不能为空
        if not digest:
            digest = "这是一篇精彩的文章，欢迎阅读！"

        return digest
