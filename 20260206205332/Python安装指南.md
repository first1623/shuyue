# 🔧 Python 安装和配置指南

## 问题诊断

当前系统未安装Python或未配置环境变量，因此无法识别 `python`、`python3` 和 `py` 命令。

---

## 解决方案

### 方案1：安装Python（推荐）

#### 步骤1：下载Python

1. 访问Python官网：https://www.python.org/downloads/
2. 下载最新稳定版（推荐 Python 3.10+ 或 3.11+）
3. 选择 Windows installer (64-bit)

#### 步骤2：安装Python

**重要：** 安装时必须勾选以下选项：

```
✅ Add Python to PATH
✅ Install for all users
```

具体步骤：
1. 运行下载的安装程序
2. **第一屏**：勾选 "Add Python to PATH"
3. 点击 "Install Now" 或 "Customize installation"
4. 等待安装完成
5. 点击 "Close"

#### 步骤3：验证安装

打开新的PowerShell窗口，输入：
```powershell
python --version
```

应该显示类似：
```
Python 3.11.0
```

#### 步骤4：安装依赖

```powershell
cd C:\Users\zhaoy\CodeBuddy\20260206205332
pip install -r requirements.txt
```

#### 步骤5：启动系统

```powershell
python launcher.py
```

---

### 方案2：使用Microsoft Store安装（更简单）

#### 步骤1：打开Microsoft Store

- 按 `Win + S`，搜索 "Microsoft Store"

#### 步骤2：搜索Python

- 在Microsoft Store中搜索 "Python"

#### 步骤3：安装

- 点击"Python 3.11"（或最新版本）
- 点击"获取"或"安装"

#### 步骤4：验证

关闭并重新打开PowerShell，输入：
```powershell
python --version
```

#### 步骤5：安装依赖并启动

```powershell
cd C:\Users\zhaoy\CodeBuddy\20260206205332
pip install -r requirements.txt
python launcher.py
```

---

### 方案3：使用Anaconda（适合数据科学用户）

#### 步骤1：下载Anaconda

1. 访问：https://www.anaconda.com/download
2. 下载 Windows 版本

#### 步骤2：安装Anaconda

1. 运行安装程序
2. 按照向导完成安装

#### 步骤3：使用Anaconda Prompt

- 点击开始菜单
- 搜索 "Anaconda Prompt"
- 打开后执行：

```bash
cd C:\Users\zhaoy\CodeBuddy\20260206205332
pip install -r requirements.txt
python launcher.py
```

---

### 方案4：使用在线Python环境（临时方案）

如果暂时无法安装Python，可以使用在线环境：

#### Replit（推荐）
1. 访问：https://replit.com/
2. 创建新项目
3. 上传本项目文件
4. 在线运行

#### Google Colab
1. 访问：https://colab.research.google.com/
2. 创建新笔记本
3. 上传代码运行

---

## 📋 快速安装检查清单

### 安装前检查

- [ ] Windows 10 或 11 系统
- [ ] 管理员权限
- [ ] 网络连接

### 安装后检查

- [ ] Python 已安装
- [ ] 能运行 `python --version`
- [ ] 能运行 `pip --version`
- [ ] 已安装项目依赖
- [ ] 能运行项目

---

## 🔍 验证安装是否成功

安装完成后，在**新的**PowerShell窗口中执行：

```powershell
# 1. 检查Python版本
python --version

# 2. 检查pip
pip --version

# 3. 进入项目目录
cd C:\Users\zhaoy\CodeBuddy\20260206205332

# 4. 安装依赖
pip install -r requirements.txt

# 5. 测试项目
python test_connection.py

# 6. 启动系统
python launcher.py
```

---

## ⚠️ 常见问题

### Q1: 安装后仍提示"找不到命令"

**A:**
1. 确保安装时勾选了"Add Python to PATH"
2. 关闭并重新打开PowerShell
3. 重启电脑

### Q2: 环境变量未生效

**A: 手动添加环境变量**

1. 右键"此电脑" > 属性
2. 高级系统设置 > 环境变量
3. 在"用户变量"或"系统变量"中找到"Path"
4. 添加Python安装路径，例如：
   ```
   C:\Users\YourName\AppData\Local\Programs\Python\Python311
   C:\Users\YourName\AppData\Local\Programs\Python\Python311\Scripts
   ```
5. 点击确定
6. 重启PowerShell

### Q3: pip安装失败

**A:**
```powershell
# 升级pip
python -m pip install --upgrade pip

# 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q4: Python版本太旧

**A:**
项目需要 Python 3.7+
如果版本 < 3.7，请安装新版本

---

## 🎯 推荐方案

**最简单的方式：**

1. 使用Microsoft Store安装Python
2. 安装时确保添加到PATH
3. 重新打开PowerShell
4. 运行 `python launcher.py`

**最快的方式（如果已有Python）：**

1. 找到Python安装路径
2. 使用完整路径运行：
   ```
   "C:\你的Python路径\python.exe" launcher.py
   ```

---

## 📞 需要帮助？

1. 确认Python版本：需要 3.7+
2. 确认已添加到PATH
3. 尝试使用Anaconda
4. 使用在线Python环境

---

## ✅ 安装成功后

您的配置已经完成，只需：

```powershell
cd C:\Users\zhaoy\CodeBuddy\20260206205332
python launcher.py
```

即可开始使用小红书发布系统！🎉
