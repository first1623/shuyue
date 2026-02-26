# 快速开始指南

## Windows 用户

### 方法1：使用启动脚本（推荐）

双击运行 `start.bat`，脚本会自动：
1. 检查并安装依赖
2. 测试API连接
3. 启动主程序

### 方法2：手动运行

```bash
# 1. 检查并安装依赖
python check_and_install.py

# 2. 测试API连接
python test_connection.py

# 3. 启动主程序
python main.py
```

## Linux / Mac 用户

```bash
# 1. 检查并安装依赖
python3 check_and_install.py

# 2. 测试API连接
python3 test_connection.py

# 3. 启动主程序
python3 main.py
```

## 使用说明

启动后选择功能：
1. 快速发布 - 输入主题直接发布
2. 生成预览 - 生成内容后确认
3. 批量发布 - 批量处理多个主题
4. 查看记录 - 查看历史发布记录
5. 系统配置 - 查看和修改配置

## 常见问题

### Q: 提示"找不到python命令"
A: Windows用户尝试使用 `python3` 或 `py` 命令

### Q: 依赖安装失败
A: 使用 `pip install -r requirements.txt` 手动安装

### Q: API连接失败
A: 检查 `.env` 文件中的API Key是否正确

## 配置文件

- `.env` - API配置
- `requirements.txt` - Python依赖包
