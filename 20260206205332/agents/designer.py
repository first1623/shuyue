from PIL import Image
import requests
import os
from config import Config
from logger import logger
from ai_client import AIClient

class ImageDesigner:
    """图片智能体：生成符合文案的图片"""

    def __init__(self):
        self.ai_client = AIClient()
        self.image_engine = Config.IMAGE_ENGINE
        self.output_dir = "generated_images"

        # 确保输出目录存在
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_image_prompts(self, theme: str, copywriting: str, strategy: dict) -> list:
        """
        生成图片提示词

        Args:
            theme: 主题
            copywriting: 文案内容
            strategy: 内容策略

        Returns:
            list: 图片提示词列表
        """
        logger.info("生成图片提示词")

        prompt = f"""
为主题"{theme}"的文案生成2-3张配图的AI绘画提示词。

文案内容：
{copywriting[:200]}

内容策略：
- 目标人群：{strategy.get('target_audience')}
- 内容角度：{', '.join(strategy.get('content_angles', []))}

请为小红书风格配图生成提示词，要求：
1. 风格清新简约，高质量
2. 色彩明亮，适合社交媒体传播
3. 第一张：主题主图
4. 第二张：细节或步骤图（如有）
5. 第三张：氛围或效果图（可选）

请以JSON格式返回，格式如下：
{{
    "prompts": [
        "prompt1",
        "prompt2"
    ]
}}
"""

        try:
            use_json_format = self.ai_client.provider in ['openai', 'deepseek']

            kwargs = {
                "messages": [
                    {"role": "system", "content": "你是一个专业的AI绘画提示词创作专家。"},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7
            }

            if use_json_format:
                kwargs["response_format"] = {"type": "json_object"}

            response = self.ai_client.chat_completion(**kwargs)

            result = eval(response.choices[0].message.content)
            prompts = result.get('prompts', [])
            logger.info(f"生成了{len(prompts)}个图片提示词")
            return prompts

        except Exception as e:
            logger.error(f"提示词生成失败: {str(e)}")
            return self._get_default_prompts(theme)

    def _get_default_prompts(self, theme: str) -> list:
        """获取默认提示词"""
        return [
            f"小红书风格配图，{theme}，清新简约，明亮色彩，高质量，4K，社交媒体风格",
            f"生活方式主题图，{theme}，现代简约风格，柔和光线，温馨氛围，ins风"
        ]

    def generate_images(self, prompts: list) -> list:
        """
        根据提示词生成图片

        Args:
            prompts: 图片提示词列表

        Returns:
            list: 生成的图片路径列表
        """
        logger.info(f"开始生成{len(prompts)}张图片")

        image_paths = []

        for idx, prompt in enumerate(prompts):
            try:
                image_path = self._generate_single_image(prompt, idx)
                if image_path:
                    image_paths.append(image_path)

            except Exception as e:
                logger.error(f"生成第{idx+1}张图片失败: {str(e)}")

        logger.info(f"成功生成{len(image_paths)}张图片")
        return image_paths

    def _generate_single_image(self, prompt: str, index: int) -> str:
        """
        生成单张图片

        Args:
            prompt: 提示词
            index: 图片索引

        Returns:
            str: 图片保存路径
        """
        if self.image_engine == "dall-e-3":
            return self._generate_with_dalle(prompt, index)
        else:
            return self._generate_with_stable_diffusion(prompt, index)

    def _generate_with_dalle(self, prompt: str, index: int) -> str:
        """使用DALL-E 3生成图片"""
        try:
            response = self.ai_client.generate_image(
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )

            image_url = response.data[0].url
            image_path = os.path.join(self.output_dir, f"image_{index+1}.png")

            # 下载图片
            response = requests.get(image_url)
            with open(image_path, 'wb') as f:
                f.write(response.content)

            logger.info(f"DALL-E生成图片成功: {image_path}")
            return image_path

        except Exception as e:
            logger.error(f"DALL-E生成失败: {str(e)}")
            return None

    def _generate_with_stable_diffusion(self, prompt: str, index: int) -> str:
        """使用Stable Diffusion生成图片"""
        try:
            url = f"{Config.STABLE_DIFFUSION_API_URL}/sdapi/v1/txt2img"
            payload = {
                "prompt": prompt,
                "negative_prompt": "low quality, blurry, ugly, distorted",
                "steps": 20,
                "width": 768,
                "height": 768,
                "cfg_scale": 7
            }

            response = requests.post(url, json=payload)
            response.raise_for_status()

            # 保存图片
            import base64
            from io import BytesIO

            image_data = response.json()['images'][0]
            image = Image.open(BytesIO(base64.b64decode(image_data)))

            image_path = os.path.join(self.output_dir, f"image_{index+1}.png")
            image.save(image_path)

            logger.info(f"Stable Diffusion生成图片成功: {image_path}")
            return image_path

        except Exception as e:
            logger.error(f"Stable Diffusion生成失败: {str(e)}")
            return None

    def regenerate_image(self, old_path: str, new_prompt: str) -> str:
        """
        重新生成指定图片

        Args:
            old_path: 原图片路径
            new_prompt: 新的提示词

        Returns:
            str: 新图片路径
        """
        logger.info(f"重新生成图片: {old_path}")

        # 提取索引
        index = int(os.path.basename(old_path).split('_')[1].split('.')[0]) - 1

        return self._generate_single_image(new_prompt, index)

    def optimize_image_for_xhs(self, image_path: str) -> str:
        """
        优化图片适合小红书发布

        Args:
            image_path: 原图片路径

        Returns:
            str: 优化后图片路径
        """
        try:
            image = Image.open(image_path)

            # 转换为RGB
            if image.mode != 'RGB':
                image = image.convert('RGB')

            # 压缩图片（小红书建议图片大小不超过10MB）
            optimized_path = image_path.replace('.png', '_optimized.jpg')
            image.save(optimized_path, 'JPEG', quality=85, optimize=True)

            logger.info(f"图片优化成功: {optimized_path}")
            return optimized_path

        except Exception as e:
            logger.error(f"图片优化失败: {str(e)}")
            return image_path
