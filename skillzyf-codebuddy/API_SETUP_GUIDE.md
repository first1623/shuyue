# AI API 配置指南

本文档详细说明如何配置国内可用的AI API，替代OpenAI API。

## 📋 目录

1. [推荐方案：DeepSeek](#1-deepseek-推荐)
2. [备选方案：通义千问](#2-通义千问)
3. [备选方案：月之暗面](#3-月之暗面)
4. [备选方案：智谱AI](#4-智谱ai)
5. [图片生成方案](#5-图片生成方案)
6. [快速开始](#6-快速开始)

---

## 1. DeepSeek（推荐）

### 为什么推荐？

✅ **免费额度高**：新用户赠送500万Tokens（约相当于2000元OpenAI额度）
✅ **性价比高**：国内价格最低之一
✅ **性能优秀**：支持长上下文（128K）
✅ **免翻墙**：国内访问稳定
✅ **速度快**：响应时间短

### 具体操作步骤

#### 第1步：注册账号

1. 访问 DeepSeek 官网：https://www.deepseek.com/
2. 点击右上角"注册"
3. 使用手机号或邮箱注册
4. 完成验证

#### 第2步：获取API Key

1. 登录后点击"开发者"或"API平台"
2. 进入：https://platform.deepseek.com/
3. 点击"API Keys"菜单
4. 点击"创建新的API Key"
5. 输入名称（如：小红书系统）
6. 复制生成的API Key（格式：sk-xxxxxxxx）

#### 第3步：配置系统

1. 复制项目中的 `.env.example` 文件为 `.env`
2. 编辑 `.env` 文件，填入配置：

```env
# 选择DeepSeek作为AI提供商
AI_PROVIDER=deepseek

# 填入你的API Key
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxx

# 其他配置保持默认
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-chat
```

#### 第4步：测试连接

运行测试脚本：

```bash
python -c "from ai_client import AIClient; client = AIClient('deepseek'); print(client.test_connection())"
```

如果返回 `True`，说明配置成功！

### 费用说明

- 新用户免费额度：500万Tokens
- 超出后价格：
  - DeepSeek-Chat: ¥1 / 100万Tokens
  - DeepSeek-Coder: ¥1 / 100万Tokens

---

## 2. 通义千问

### 特点

✅ 阿里云出品，稳定性强
✅ 新用户赠送免费额度
✅ 支持多模态
✅ 中文优化

### 操作步骤

#### 第1步：注册阿里云账号

1. 访问：https://dashscope.aliyun.com/
2. 点击"登录/注册"
3. 使用支付宝或手机号注册

#### 第2步：开通服务

1. 登录后进入控制台
2. 开通"通义千问"服务
3. 进入API-KEY管理

#### 第3步：创建API Key

1. 点击"创建新的API-KEY"
2. 复制生成的Key

#### 第4步：配置

```env
AI_PROVIDER=qwen
QWEN_API_KEY=sk-xxxxxxxxxxxxxxxx
```

### 费用说明

- 新用户免费试用
- qwen-turbo: ¥0.0008 / 千tokens
- qwen-plus: ¥0.004 / 千tokens

---

## 3. 月之暗面

### 特点

✅ 专注于长上下文
✅ 支持超长文本
✅ 新用户免费额度
✅ 性价比高

### 操作步骤

#### 第1步：注册

1. 访问：https://platform.moonshot.cn/
2. 点击"注册"
3. 完成注册流程

#### 第2步：获取API Key

1. 登录后进入API管理页面
2. 创建新的API Key
3. 复制Key

#### 第3步：配置

```env
AI_PROVIDER=moonshot
MOONSHOT_API_KEY=sk-xxxxxxxxxxxxxxxx
```

### 费用说明

- 新用户免费额度
- moonshot-v1-8k: ¥12 / 1M tokens
- moonshot-v1-32k: ¥24 / 1M tokens
- moonshot-v1-128k: ¥60 / 1M tokens

---

## 4. 智谱AI（GLM-4）

### 特点

✅ 清华系AI公司
✅ 国产大模型领先者
✅ 新用户免费额度
✅ 中文理解能力强

### 操作步骤

#### 第1步：注册

1. 访问：https://open.bigmodel.cn/
2. 点击"注册"
3. 完成注册

#### 第2步：获取API Key

1. 登录后进入API Key管理
2. 创建新的Key
3. 复制Key

#### 第3步：配置

```env
AI_PROVIDER=zhipu
ZHIPU_API_KEY=xxxxxxxxxxxxxxxx
```

### 费用说明

- 新用户免费额度
- GLM-4: ¥0.1 / 千tokens
- GLM-3-Turbo: ¥0.005 / 千tokens

---

## 5. 图片生成方案

### 方案1：Stable Diffusion（推荐，免费）

#### 安装步骤

##### Windows：

1. 下载安装器：https://github.com/AUTOMATIC1111/stable-diffusion-webui
2. 或使用便携版下载链接

##### Mac：

```bash
brew install pyqt
git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git
cd stable-diffusion-webui
./webui.sh
```

##### 配置：

启动后在浏览器访问：http://localhost:7860

无需额外配置，系统默认使用此端口。

### 方案2：DALL-E 3（付费）

需要配置OpenAI API Key，仅在国外可用。

---

## 6. 快速开始

### 最简单的配置方案（推荐）

1. **注册DeepSeek**（5分钟）
   - 访问：https://platform.deepseek.com/
   - 注册并获取API Key

2. **配置.env文件**（2分钟）

```bash
# 复制配置模板
cp .env.example .env

# 编辑.env，修改以下内容
AI_PROVIDER=deepseek
DEEPSEEK_API_KEY=你的API_Key
```

3. **测试运行**（1分钟）

```bash
# 安装依赖
pip install -r requirements.txt

# 运行程序
python main.py
```

### 验证配置

运行以下命令测试配置：

```bash
python -c "
from config import Config
from ai_client import AIClient

# 验证配置
Config.validate()

# 测试连接
client = AIClient()
result = client.test_connection()
print('连接状态:', '成功' if result else '失败')
"
```

---

## 对比表

| 服务商 | 新用户免费 | 价格 | 速度 | 中文支持 | 推荐度 |
|--------|-----------|------|------|---------|--------|
| DeepSeek | 500万Tokens | ¥1/100万 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 通义千问 | 有 | ¥0.8/千 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 月之暗面 | 有 | ¥12/100万 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 智谱AI | 有 | ¥10/万 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| OpenAI | $5 | $15/百万 | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ |

---

## 常见问题

### Q1: API Key 哪里找？

A: 登录对应平台的控制台，在"API Key"或"API管理"页面创建和查看。

### Q2: 如何切换AI服务商？

A: 修改 `.env` 文件中的 `AI_PROVIDER` 参数即可，无需修改代码。

```env
AI_PROVIDER=deepseek  # 可改为 qwen, moonshot, zhipu, openai
```

### Q3: 免费额度用完了怎么办？

A:
1. 继续使用付费服务（价格很低）
2. 注册另一个服务商的免费额度
3. 购买更多额度

### Q4: 图片生成必须配置吗？

A: 不是必须。如果配置了DALL-E 3或Stable Diffusion会生成图片，否则只生成文案。

### Q5: 支持同时配置多个服务商吗？

A: 当前版本不支持同时使用，每次运行选择一个服务商。可在 `.env` 中配置多个，通过 `AI_PROVIDER` 切换。

---

## 技术支持

如遇到问题：

1. 查看日志文件：`logs/日期.log`
2. 确认API Key格式正确
3. 检查网络连接
4. 测试API连接：运行测试脚本

---

## 更新日志

- 2026-02-06: 添加DeepSeek、通义千问、月之暗面、智谱AI支持
- 支持通过配置文件快速切换AI服务商
