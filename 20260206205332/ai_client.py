from openai import OpenAI
from config import Config
from logger import logger

class AIClient:
    """统一AI客户端，支持多个AI服务提供商"""

    def __init__(self, provider: str = None):
        """
        初始化AI客户端

        Args:
            provider: AI服务提供商 (openai, deepseek, qwen, moonshot, zhipu)
                     默认从配置读取
        """
        self.provider = provider or Config.AI_PROVIDER
        self.client = self._init_client()
        self.model = self._get_model()

    def _init_client(self):
        """根据提供商初始化客户端"""
        if self.provider == 'openai':
            return OpenAI(
                api_key=Config.OPENAI_API_KEY,
                base_url=Config.OPENAI_BASE_URL
            )

        elif self.provider == 'deepseek':
            return OpenAI(
                api_key=Config.DEEPSEEK_API_KEY,
                base_url=Config.DEEPSEEK_BASE_URL
            )

        elif self.provider == 'qwen':
            return OpenAI(
                api_key=Config.QWEN_API_KEY,
                base_url=Config.QWEN_BASE_URL
            )

        elif self.provider == 'moonshot':
            return OpenAI(
                api_key=Config.MOONSHOT_API_KEY,
                base_url=Config.MOONSHOT_BASE_URL
            )

        elif self.provider == 'zhipu':
            return OpenAI(
                api_key=Config.ZHIPU_API_KEY,
                base_url=Config.ZHIPU_BASE_URL
            )

        else:
            raise ValueError(f"不支持的AI提供商: {self.provider}")

    def _get_model(self):
        """获取模型名称"""
        if self.provider == 'openai':
            return Config.OPENAI_MODEL
        elif self.provider == 'deepseek':
            return Config.DEEPSEEK_MODEL
        elif self.provider == 'qwen':
            return Config.QWEN_MODEL
        elif self.provider == 'moonshot':
            return Config.MOONSHOT_MODEL
        elif self.provider == 'zhipu':
            return Config.ZHIPU_MODEL
        else:
            return "default"

    def chat_completion(self, messages, **kwargs):
        """
        聊天完成

        Args:
            messages: 消息列表
            **kwargs: 其他参数

        Returns:
            response: 响应对象
        """
        try:
            response = self.client.chat.completions.create(
                messages=messages,
                model=self.model,
                **kwargs
            )
            return response

        except Exception as e:
            logger.error(f"API调用失败: {str(e)}")
            raise

    def generate_image(self, prompt, **kwargs):
        """
        生成图片（仅OpenAI支持）

        Args:
            prompt: 图片提示词
            **kwargs: 其他参数

        Returns:
            response: 响应对象
        """
        try:
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                **kwargs
            )
            return response

        except Exception as e:
            logger.error(f"图片生成失败: {str(e)}")
            raise

    def test_connection(self):
        """测试连接是否正常"""
        try:
            messages = [
                {"role": "user", "content": "你好，请回复'连接成功'"}
            ]
            response = self.chat_completion(messages, max_tokens=10)
            logger.info(f"{self.provider} API连接测试成功")
            return True

        except Exception as e:
            logger.error(f"{self.provider} API连接测试失败: {str(e)}")
            return False
