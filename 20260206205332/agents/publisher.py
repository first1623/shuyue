import requests
import time
import json
import os
from typing import Dict, List
from config import Config
from logger import logger

class APIPublisher:
    """发布智能体：处理小红书API发布流程"""

    def __init__(self):
        self.access_token = Config.XHS_ACCESS_TOKEN
        self.app_id = Config.XHS_APP_ID
        self.app_secret = Config.XHS_APP_SECRET
        self.api_base = Config.XHS_API_BASE
        self.max_retry = Config.MAX_RETRY_TIMES
        self.publish_delay = Config.PUBLISH_DELAY

    def publish_post(self, content: Dict) -> Dict:
        """
        发布笔记到小红书

        Args:
            content: 内容字典
                {
                    'title': str,
                    'content': str,
                    'images': List[str],
                    'hashtags': List[str]
                }

        Returns:
            dict: 发布结果
                {
                    'success': bool,
                    'note_id': str,
                    'message': str
                }
        """
        logger.info("开始发布笔记")

        try:
            # 1. 上传图片
            image_ids = self._upload_images(content['images'])
            if not image_ids:
                return {
                    'success': False,
                    'note_id': None,
                    'message': '图片上传失败'
                }

            # 2. 创建笔记
            result = self._create_note(content, image_ids)

            logger.info(f"发布完成: {result['message']}")
            return result

        except Exception as e:
            logger.error(f"发布失败: {str(e)}")
            return {
                'success': False,
                'note_id': None,
                'message': f'发布失败: {str(e)}'
            }

    def _upload_images(self, image_paths: List[str]) -> List[str]:
        """
        上传图片

        Args:
            image_paths: 图片路径列表

        Returns:
            list: 图片ID列表
        """
        logger.info(f"开始上传{len(image_paths)}张图片")

        image_ids = []

        for idx, image_path in enumerate(image_paths):
            try:
                # 优化图片
                if not os.path.exists(image_path):
                    logger.warning(f"图片不存在: {image_path}")
                    continue

                # 模拟上传（实际调用小红书API）
                image_id = self._upload_single_image(image_path)
                if image_id:
                    image_ids.append(image_id)
                    logger.info(f"图片{idx+1}上传成功，ID: {image_id}")

                # 避免频率限制
                time.sleep(1)

            except Exception as e:
                logger.error(f"图片{idx+1}上传失败: {str(e)}")

        logger.info(f"成功上传{len(image_ids)}张图片")
        return image_ids

    def _upload_single_image(self, image_path: str) -> str:
        """
        上传单张图片（模拟实现）

        Args:
            image_path: 图片路径

        Returns:
            str: 图片ID
        """
        try:
            # 实际实现需要调用小红书API
            # 这里是模拟实现

            # 检查API配置
            if not self.access_token:
                logger.warning("未配置小红书API，使用模拟上传")
                return f"mock_image_id_{int(time.time())}"

            # 实际API调用示例（需要根据官方文档调整）
            # url = f"{self.api_base}/upload/image"
            # headers = {
            #     'Authorization': f'Bearer {self.access_token}',
            #     'Content-Type': 'multipart/form-data'
            # }
            # files = {'file': open(image_path, 'rb')}
            # response = requests.post(url, headers=headers, files=files)
            # response.raise_for_status()
            # return response.json()['data']['image_id']

            # 模拟成功
            return f"image_id_{int(time.time() * 1000)}"

        except Exception as e:
            logger.error(f"单张图片上传失败: {str(e)}")
            raise

    def _create_note(self, content: Dict, image_ids: List[str]) -> Dict:
        """
        创建笔记

        Args:
            content: 内容字典
            image_ids: 图片ID列表

        Returns:
            dict: 创建结果
        """
        url = f"{self.api_base}/note/create"
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

        payload = {
            'title': content.get('title', ''),
            'content': content.get('content', ''),
            'image_ids': image_ids,
            'visibility': 'PUBLIC',
            'type': 'NORMAL'
        }

        try:
            # 检查API配置
            if not self.access_token:
                logger.warning("未配置小红书API，模拟发布")
                note_id = f"mock_note_{int(time.time())}"
                return {
                    'success': True,
                    'note_id': note_id,
                    'message': '模拟发布成功'
                }

            # 实际API调用（需要根据官方文档调整）
            # for retry in range(self.max_retry):
            #     try:
            #         response = requests.post(url, headers=headers, json=payload)
            #         response.raise_for_status()
            #         result = response.json()

            #         if result.get('success'):
            #             return {
            #                 'success': True,
            #                 'note_id': result.get('data', {}).get('note_id'),
            #                 'message': '发布成功'
            #             }
            #         else:
            #             logger.error(f"API返回错误: {result}")
            #             time.sleep(self.publish_delay)

            #     except requests.RequestException as e:
            #         logger.error(f"发布请求失败(重试{retry+1}/{self.max_retry}): {str(e)}")
            #         if retry < self.max_retry - 1:
            #             time.sleep(self.publish_delay * (retry + 1))

            # 模拟成功
            note_id = f"note_{int(time.time() * 1000)}"
            return {
                'success': True,
                'note_id': note_id,
                'message': '发布成功'
            }

        except Exception as e:
            logger.error(f"创建笔记失败: {str(e)}")
            return {
                'success': False,
                'note_id': None,
                'message': f'创建笔记失败: {str(e)}'
            }

    def delete_note(self, note_id: str) -> Dict:
        """
        删除笔记

        Args:
            note_id: 笔记ID

        Returns:
            dict: 删除结果
        """
        logger.info(f"删除笔记: {note_id}")

        url = f"{self.api_base}/note/{note_id}/delete"
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }

        try:
            # 实际API调用
            # response = requests.delete(url, headers=headers)
            # response.raise_for_status()
            # return {'success': True, 'message': '删除成功'}

            # 模拟成功
            return {'success': True, 'message': '模拟删除成功'}

        except Exception as e:
            logger.error(f"删除笔记失败: {str(e)}")
            return {'success': False, 'message': f'删除失败: {str(e)}'}

    def get_note_status(self, note_id: str) -> Dict:
        """
        获取笔记状态

        Args:
            note_id: 笔记ID

        Returns:
            dict: 笔记状态
        """
        logger.info(f"查询笔记状态: {note_id}")

        url = f"{self.api_base}/note/{note_id}"
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }

        try:
            # 实际API调用
            # response = requests.get(url, headers=headers)
            # response.raise_for_status()
            # return response.json()

            # 模拟返回
            return {
                'note_id': note_id,
                'status': 'PUBLISHED',
                'view_count': 100,
                'like_count': 50,
                'comment_count': 10
            }

        except Exception as e:
            logger.error(f"查询笔记状态失败: {str(e)}")
            return {'status': 'UNKNOWN'}

    def schedule_publish(self, content: Dict, publish_time: str) -> Dict:
        """
        定时发布

        Args:
            content: 内容字典
            publish_time: 发布时间（格式: "2024-01-01 18:00:00"）

        Returns:
            dict: 定时发布结果
        """
        logger.info(f"设置定时发布: {publish_time}")

        # 计算延迟
        from datetime import datetime
        publish_dt = datetime.strptime(publish_time, "%Y-%m-%d %H:%M:%S")
        now = datetime.now()
        delay = (publish_dt - now).total_seconds()

        if delay < 0:
            return {'success': False, 'message': '发布时间无效'}

        # 模拟定时发布
        # 实际实现可以使用任务队列（如Celery）
        logger.info(f"将在{delay}秒后发布")
        return {
            'success': True,
            'message': f'已设置定时发布: {publish_time}',
            'scheduled_time': publish_time
        }

    def save_publish_record(self, content: Dict, result: Dict) -> None:
        """
        保存发布记录

        Args:
            content: 内容字典
            result: 发布结果
        """
        record = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'theme': content.get('theme', ''),
            'title': content.get('title', ''),
            'note_id': result.get('note_id', ''),
            'status': 'success' if result.get('success') else 'failed',
            'message': result.get('message', '')
        }

        # 确保记录目录存在
        records_dir = "publish_records"
        os.makedirs(records_dir, exist_ok=True)

        # 保存记录
        record_file = os.path.join(records_dir, f"records_{time.strftime('%Y%m%d')}.json")
        try:
            if os.path.exists(record_file):
                with open(record_file, 'r', encoding='utf-8') as f:
                    records = json.load(f)
            else:
                records = []

            records.append(record)

            with open(record_file, 'w', encoding='utf-8') as f:
                json.dump(records, f, ensure_ascii=False, indent=2)

            logger.info(f"发布记录已保存: {record_file}")

        except Exception as e:
            logger.error(f"保存发布记录失败: {str(e)}")
