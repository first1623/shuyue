# -*- coding: utf-8 -*-
import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import json
from agents.wechat_publisher import WeChatPublisher

def test_publish():
    print("="*60)
    print("测试发布文章")
    print("="*60)
    print()

    publisher = WeChatPublisher()

    # 准备测试数据
    content = {
        'title': '测试文章标题',
        'content': '<p>这是一篇测试文章的内容。</p>',
        'digest': '这是一篇测试文章',
        'author': '测试作者',
        'show_cover_pic': 0,  # 不显示封面
        'need_open_comment': 1,
        'only_fans_can_comment': 0
    }

    print("准备发布的内容:")
    print(json.dumps(content, ensure_ascii=False, indent=2))
    print()

    # 构建请求数据
    article_data = {
        'title': content.get('title', ''),
        'author': content.get('author', ''),
        'digest': content.get('digest', ''),
        'content': content.get('content', ''),
        'show_cover_pic': content.get('show_cover_pic', 0),
        'need_open_comment': content.get('need_open_comment', 1),
        'only_fans_can_comment': content.get('only_fans_can_comment', 0)
    }

    print("发送给微信API的数据:")
    print(json.dumps({'articles': [article_data]}, ensure_ascii=False, indent=2))
    print()

    try:
        result = publisher._create_draft([article_data])

        if result.get('success'):
            print("发布成功!")
            print(f"Media ID: {result.get('media_id')}")
        else:
            print("发布失败!")
            print(f"错误信息: {result.get('message')}")
    except Exception as e:
        print(f"异常: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_publish()
    input("\n按回车键退出...")
