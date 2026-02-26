# 超简单测试脚本 - 测试Python是否能找到文件
import os
print("当前工作目录:", os.getcwd())
print("Python版本:", os.sys.version)

# 检查文件是否存在
file_path = "simple_start.py"
if os.path.exists(file_path):
    print(f"✅ 找到文件: {file_path}")
    print("正在运行...")
    
    # 直接执行文件
    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()
    exec(code)
else:
    print(f"❌ 找不到文件: {file_path}")
    print("当前目录下的文件:")
    for file in os.listdir("."):
        if file.endswith('.py'):
            print(f"  - {file}")