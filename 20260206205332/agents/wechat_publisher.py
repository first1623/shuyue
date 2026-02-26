import requests
import time
import json
import os
from typing import Dict, List
from config import Config
from logger import logger
import hashlib

class WeChatPublisher:
    """微信公众号发布智能体"""

    def __init__(self):
        """初始化微信公众号发布器"""
        self.app_id = Config.WECHAT_APP_ID
        self.app_secret = Config.WECHAT_APP_SECRET
        self.api_base = "https://api.weixin.qq.com/cgi-bin"
        self.max_retry = Config.MAX_RETRY_TIMES
        self.publish_delay = Config.PUBLISH_DELAY
        self.access_token = None

    def get_access_token(self) -> str:
        """
        获取微信公众号访问令牌

        Returns:
            str: access_token
        """
        url = f"{self.api_base}/token"
        params = {
            'grant_type': 'client_credential',
            'appid': self.app_id,
            'secret': self.app_secret
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            result = response.json()

            if result.get('access_token'):
                self.access_token = result['access_token']
                logger.info(f"获取access_token成功: {self.access_token[:10]}...")
                return self.access_token
            else:
                logger.error(f"获取access_token失败: {result}")
                raise Exception(result.get('errmsg', '获取token失败'))

        except Exception as e:
            logger.error(f"获取access_token异常: {str(e)}")
            raise

    def publish_article(self, content: Dict) -> Dict:
        """
        发布文章到微信公众号

        Args:
            content: 内容字典
                {
                    'title': str,              # 文章标题
                    'content': str,            # 正文内容（HTML格式）
                    'digest': str,             # 摘要
                    'thumb_media_id': str,     # 封面图片media_id
                    'author': str,             # 作者
                    'show_cover_pic': int,     # 是否显示封面（0否，1是）
                    'need_open_comment': int,  # 是否打开评论（0否，1是）
                    'only_fans_can_comment': int # 是否只有粉丝可以评论（0否，1是）
                }

        Returns:
            dict: 发布结果
                {
                    'success': bool,
                    'article_id': str,
                    'media_id': str,
                    'message': str
                }
        """
        logger.info("开始发布公众号文章")

        try:
            # 获取access_token
            if not self.access_token:
                self.get_access_token()

            # 上传图片（如果有封面图）
            thumb_media_id = content.get('thumb_media_id')
            if not thumb_media_id and content.get('thumb_image'):
                thumb_media_id = self._upload_image(content['thumb_image'])

            # 构建请求数据
            article_data = {
                'title': content.get('title', ''),
                'author': content.get('author', ''),
                'digest': content.get('digest', content.get('content', '')[:100]),
                'content': content.get('content', ''),
                'content_source_url': content.get('source_url', ''),
                'show_cover_pic': content.get('show_cover_pic', 0),
                'need_open_comment': content.get('need_open_comment', 1),
                'only_fans_can_comment': content.get('only_fans_can_comment', 0)
            }

            # 只有在有 thumb_media_id 时才添加此字段
            if thumb_media_id:
                article_data['thumb_media_id'] = thumb_media_id

            articles = [article_data]

            # 调用发布API
            result = self._create_draft(articles)

            if result.get('success'):
                logger.info(f"发布成功: {result['message']}")
                return result
            else:
                logger.error(f"发布失败: {result['message']}")
                return result

        except Exception as e:
            logger.error(f"发布文章失败: {str(e)}")
            return {
                'success': False,
                'article_id': None,
                'media_id': None,
                'message': f'发布失败: {str(e)}'
            }

    def _upload_image(self, image_path: str) -> str:
        """
        上传图片到微信服务器

        Args:
            image_path: 图片路径

        Returns:
            str: media_id
        """
        logger.info(f"上传图片: {image_path}")

        if not self.access_token:
            self.get_access_token()

        url = f"{self.api_base}/material/add_material?type=thumb&access_token={self.access_token}"

        try:
            if not os.path.exists(image_path):
                logger.warning(f"图片不存在: {image_path}")
                return None

            with open(image_path, 'rb') as f:
                files = {'media': f}
                response = requests.post(url, files=files, timeout=30)
                result = response.json()

                if result.get('media_id'):
                    logger.info(f"图片上传成功: {result['media_id']}")
                    return result['media_id']
                else:
                    logger.error(f"图片上传失败: {result}")
                    return None

        except Exception as e:
            logger.error(f"上传图片异常: {str(e)}")
            return None

    def _create_draft(self, articles: List[Dict]) -> Dict:
        """
        创建草稿

        Args:
            articles: 文章列表

        Returns:
            dict: 创建结果
        """
        url = f"{self.api_base}/draft/add?access_token={self.access_token}"

        # 清理article数据，移除None值
        cleaned_articles = []
        for article in articles:
            cleaned_article = {k: v for k, v in article.items() if v is not None and v != ''}
            cleaned_articles.append(cleaned_article)

        payload = {'articles': cleaned_articles}

        # 记录发送的数据
        import json
        logger.info(f"发送给微信API的数据: {json.dumps(payload, ensure_ascii=False)}")
        print(f"\n{'='*60}")
        print(f"[DEBUG] 发送的数据:")
        print(f"{'='*60}")
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        print(f"{'='*60}\n")
        import sys
        sys.stdout.flush()  # 强制刷新输出缓冲区

        try:
            # 检查API配置
            if not self.app_id or not self.app_secret:
                logger.warning("未配置微信公众号API，模拟发布")
                media_id = f"mock_media_{int(time.time())}"
                return {
                    'success': True,
                    'media_id': media_id,
                    'message': '模拟发布成功（草稿模式）'
                }

            # 实际API调用
            for retry in range(self.max_retry):
                try:
                    response = requests.post(url, json=payload, timeout=30)
                    result = response.json()

                    logger.info(f"微信API返回: {json.dumps(result, ensure_ascii=False)}")
                    print(f"[DEBUG] API返回: {json.dumps(result, ensure_ascii=False)}")

                    if result.get('errcode') == 0:
                        return {
                            'success': True,
                            'media_id': result.get('media_id'),
                            'article_id': result.get('media_id'),
                            'message': '草稿创建成功'
                        }
                    else:
                        logger.error(f"API返回错误: {result}")
                        if retry < self.max_retry - 1:
                            time.sleep(self.publish_delay)
                        else:
                            return {
                                'success': False,
                                'media_id': None,
                                'article_id': None,
                                'message': result.get('errmsg', '创建草稿失败')
                            }

                except requests.RequestException as e:
                    logger.error(f"发布请求失败(重试{retry+1}/{self.max_retry}): {str(e)}")
                    if retry < self.max_retry - 1:
                        time.sleep(self.publish_delay * (retry + 1))

        except Exception as e:
            logger.error(f"创建草稿失败: {str(e)}")
            return {
                'success': False,
                'media_id': None,
                'article_id': None,
                'message': f'创建草稿失败: {str(e)}'
            }

    def publish_draft(self, media_id: str) -> Dict:
        """
        发布草稿

        Args:
            media_id: 草稿的media_id

        Returns:
            dict: 发布结果
        """
        logger.info(f"发布草稿: {media_id}")

        url = f"{self.api_base}/freepublish/submit?access_token={self.access_token}"

        payload = {'media_id': media_id}

        try:
            for retry in range(self.max_retry):
                try:
                    response = requests.post(url, json=payload, timeout=30)
                    result = response.json()

                    if result.get('errcode') == 0:
                        publish_id = result.get('publish_id')
                        return {
                            'success': True,
                            'publish_id': publish_id,
                            'message': '文章发布成功'
                        }
                    else:
                        logger.error(f"API返回错误: {result}")
                        if retry < self.max_retry - 1:
                            time.sleep(self.publish_delay)
                        else:
                            return {
                                'success': False,
                                'publish_id': None,
                                'message': result.get('errmsg', '发布失败')
                            }

                except requests.RequestException as e:
                    logger.error(f"发布请求失败(重试{retry+1}/{self.max_retry}): {str(e)}")
                    if retry < self.max_retry - 1:
                        time.sleep(self.publish_delay * (retry + 1))

        except Exception as e:
            logger.error(f"发布草稿失败: {str(e)}")
            return {
                'success': False,
                'publish_id': None,
                'message': f'发布失败: {str(e)}'
            }

    def get_article_list(self, offset: int = 0, count: int = 20) -> Dict:
        """
        获取公众号文章列表

        Args:
            offset: 偏移量
            count: 数量

        Returns:
            dict: 文章列表
        """
        logger.info(f"获取文章列表: offset={offset}, count={count}")

        url = f"{self.api_base}/draft/batchget?access_token={self.access_token}"

        payload = {
            'offset': offset,
            'count': count,
            'no_content': 0  # 是否不返回内容正文（0返回，1不返回）
        }

        try:
            response = requests.post(url, json=payload, timeout=30)
            result = response.json()

            if result.get('errcode') == 0:
                total = result.get('total_count', 0)
                items = result.get('item', [])
                logger.info(f"获取成功: 共{total}篇文章，返回{len(items)}篇")
                return {
                    'success': True,
                    'total': total,
                    'items': items
                }
            else:
                logger.error(f"获取失败: {result}")
                return {
                    'success': False,
                    'total': 0,
                    'items': [],
                    'message': result.get('errmsg', '获取列表失败')
                }

        except Exception as e:
            logger.error(f"获取文章列表异常: {str(e)}")
            return {
                'success': False,
                'total': 0,
                'items': [],
                'message': f'获取列表失败: {str(e)}'
            }

    def delete_article(self, media_id: str) -> Dict:
        """
        删除文章

        Args:
            media_id: 文章的media_id

        Returns:
            dict: 删除结果
        """
        logger.info(f"删除文章: {media_id}")

        url = f"{self.api_base}/draft/delete?access_token={self.access_token}"

        payload = {'media_id': media_id}

        try:
            response = requests.post(url, json=payload, timeout=30)
            result = response.json()

            if result.get('errcode') == 0:
                logger.info("删除成功")
                return {
                    'success': True,
                    'message': '删除成功'
                }
            else:
                logger.error(f"删除失败: {result}")
                return {
                    'success': False,
                    'message': result.get('errmsg', '删除失败')
                }

        except Exception as e:
            logger.error(f"删除文章异常: {str(e)}")
            return {
                'success': False,
                'message': f'删除失败: {str(e)}'
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
            'media_id': result.get('media_id', ''),
            'article_id': result.get('article_id', ''),
            'status': 'success' if result.get('success') else 'failed',
            'message': result.get('message', '')
        }

        # 确保记录目录存在
        records_dir = "wechat_publish_records"
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
