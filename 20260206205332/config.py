import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """配置管理类"""

    # 小红书API配置
    XHS_ACCESS_TOKEN = os.getenv('XHS_ACCESS_TOKEN')
    XHS_APP_ID = os.getenv('XHS_APP_ID')
    XHS_APP_SECRET = os.getenv('XHS_APP_SECRET')
    XHS_API_BASE = "https://open.xiaohongshu.com/api"

    # 微信公众号API配置
    WECHAT_APP_ID = os.getenv('WECHAT_APP_ID')
    WECHAT_APP_SECRET = os.getenv('WECHAT_APP_SECRET')
    WECHAT_TOKEN = os.getenv('WECHAT_TOKEN')  # 消息验证用Token
    WECHAT_ENCODING_AES_KEY = os.getenv('WECHAT_ENCODING_AES_KEY')  # 消息加密Key（可选）

    # AI API 配置（支持多个国内API）
    AI_PROVIDER = os.getenv('AI_PROVIDER', 'openai')  # openai, deepseek, qwen, moonshot, zhipu

    # OpenAI配置
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_BASE_URL = os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4')

    # DeepSeek配置（推荐，免费额度高）
    DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
    DEEPSEEK_BASE_URL = os.getenv('DEEPSEEK_BASE_URL', 'https://api.deepseek.com')
    DEEPSEEK_MODEL = os.getenv('DEEPSEEK_MODEL', 'deepseek-chat')

    # 通义千问配置
    QWEN_API_KEY = os.getenv('QWEN_API_KEY')
    QWEN_BASE_URL = os.getenv('QWEN_BASE_URL', 'https://dashscope.aliyuncs.com/compatible-mode/v1')
    QWEN_MODEL = os.getenv('QWEN_MODEL', 'qwen-turbo')

    # 月之暗面配置
    MOONSHOT_API_KEY = os.getenv('MOONSHOT_API_KEY')
    MOONSHOT_BASE_URL = os.getenv('MOONSHOT_BASE_URL', 'https://api.moonshot.cn/v1')
    MOONSHOT_MODEL = os.getenv('MOONSHOT_MODEL', 'moonshot-v1-8k')

    # 智谱AI配置
    ZHIPU_API_KEY = os.getenv('ZHIPU_API_KEY')
    ZHIPU_BASE_URL = os.getenv('ZHIPU_BASE_URL', 'https://open.bigmodel.cn/api/paas/v4')
    ZHIPU_MODEL = os.getenv('ZHIPU_MODEL', 'GLM-4')

    # 图片生成引擎
    IMAGE_ENGINE = os.getenv('IMAGE_ENGINE', 'dall-e-3')

    # Stable Diffusion配置
    STABLE_DIFFUSION_API_URL = os.getenv('STABLE_DIFFUSION_API_URL', 'http://localhost:7860')

    # 其他配置
    MAX_RETRY_TIMES = int(os.getenv('MAX_RETRY_TIMES', 3))
    PUBLISH_DELAY = int(os.getenv('PUBLISH_DELAY', 5))

    # 敏感词列表
    SENSITIVE_WORDS = [
        "违法", "暴力", "色情", "赌博", "毒品",
        # 可根据需要扩展
    ]

    @classmethod
    def validate(cls):
        """验证必需的配置项"""
        provider = cls.AI_PROVIDER

        # 根据提供商检查对应的API Key
        if provider == 'deepseek':
            required_key = 'DEEPSEEK_API_KEY'
        elif provider == 'qwen':
            required_key = 'QWEN_API_KEY'
        elif provider == 'moonshot':
            required_key = 'MOONSHOT_API_KEY'
        elif provider == 'zhipu':
            required_key = 'ZHIPU_API_KEY'
        elif provider == 'openai':
            required_key = 'OPENAI_API_KEY'
        else:
            raise ValueError(f"不支持的AI提供商: {provider}")

        if not getattr(cls, required_key):
            raise ValueError(f"缺少必需的配置项: {required_key} (当前提供商: {provider})")

        return True

    @classmethod
    def get_current_api_key(cls):
        """获取当前AI提供商的API Key"""
        provider = cls.AI_PROVIDER
        if provider == 'deepseek':
            return cls.DEEPSEEK_API_KEY
        elif provider == 'qwen':
            return cls.QWEN_API_KEY
        elif provider == 'moonshot':
            return cls.MOONSHOT_API_KEY
        elif provider == 'zhipu':
            return cls.ZHIPU_API_KEY
        elif provider == 'openai':
            return cls.OPENAI_API_KEY
        else:
            return None

    @classmethod
    def get_current_base_url(cls):
        """获取当前AI提供商的Base URL"""
        provider = cls.AI_PROVIDER
        if provider == 'deepseek':
            return cls.DEEPSEEK_BASE_URL
        elif provider == 'qwen':
            return cls.QWEN_BASE_URL
        elif provider == 'moonshot':
            return cls.MOONSHOT_BASE_URL
        elif provider == 'zhipu':
            return cls.ZHIPU_BASE_URL
        elif provider == 'openai':
            return cls.OPENAI_BASE_URL
        else:
            return None

    @classmethod
    def get_current_model(cls):
        """获取当前AI提供商的模型名称"""
        provider = cls.AI_PROVIDER
        if provider == 'deepseek':
            return cls.DEEPSEEK_MODEL
        elif provider == 'qwen':
            return cls.QWEN_MODEL
        elif provider == 'moonshot':
            return cls.MOONSHOT_MODEL
        elif provider == 'zhipu':
            return cls.ZHIPU_MODEL
        elif provider == 'openai':
            return cls.OPENAI_MODEL
        else:
            return None
