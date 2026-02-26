# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv

load_dotenv()

print("="*60)
print("配置检查")
print("="*60)
print()
print("WECHAT_APP_ID:", os.getenv('WECHAT_APP_ID'))
print("WECHAT_APP_SECRET:", os.getenv('WECHAT_APP_SECRET')[:10] + "..." if os.getenv('WECHAT_APP_SECRET') else "None")
print()
print("="*60)
