# 小红书多智能体内容生成与发布系统

基于AI多智能体协作的小红书自动化内容生成与发布系统。

**⭐ 已支持国内AI API（DeepSeek、通义千问、月之暗面、智谱AI），无需翻墙！**

## 功能特点

- **多智能体协作**：策划、文案、设计、审核、发布五个智能体分工协作
- **智能内容生成**：自动生成符合小红书风格的文案和配图
- **内容审核**：智能检测敏感词和内容质量
- **灵活发布**：支持立即发布、定时发布、批量发布
- **人工确认**：生成内容后可预览和修改
- **多AI支持**：支持DeepSeek、通义千问、月之暗面、智谱AI、OpenAI

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置AI API

**推荐使用DeepSeek（免费额度500万Tokens）**

详细配置教程请查看：[API配置指南](API_SETUP_GUIDE.md)

快速配置：

```bash
# 复制配置模板
cp .env.example .env

# 编辑.env，设置AI提供商和API Key
AI_PROVIDER=deepseek
DEEPSEEK_API_KEY=你的API_Key
```

获取DeepSeek API Key：
1. 访问 https://platform.deepseek.com/
2. 注册账号（新用户赠送500万免费Tokens）
3. 进入API Keys页面创建Key
4. 复制到.env文件

## 系统架构

```
用户输入主题
    ↓
【策划智能体】分析主题，生成内容策略
    ↓
【文案智能体】根据策略生成小红书风格文案
    ↓
【图片智能体】生成符合文案的配图
    ↓
【审核智能体】检查内容合规性
    ↓
人工确认/修改
    ↓
【发布智能体】发布到小红书
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

复制配置模板：
```bash
cp .env.example .env
```

编辑 `.env` 文件，选择AI服务商并填入API Key：

```env
# 选择AI提供商（deepseek、qwen、moonshot、zhipu、openai）
AI_PROVIDER=deepseek

# DeepSeek配置（推荐）
DEEPSEEK_API_KEY=sk-xxxxxxxx

# 通义千问配置
# QWEN_API_KEY=sk-xxxxxxxx

# 月之暗面配置
# MOONSHOT_API_KEY=sk-xxxxxxxx

# 智谱AI配置
# ZHIPU_API_KEY=xxxxxxxx

# OpenAI配置（国外）
# OPENAI_API_KEY=sk-xxxxxxxx

# 小红书API（可选，真实发布需要）
XHS_ACCESS_TOKEN=your_token
```

### 4. 运行程序

### 3. 运行程序

```bash
python main.py
```

## 使用说明

### 主菜单

```
1. 快速发布 - 输入主题直接发布
2. 生成预览 - 生成内容后确认
3. 批量发布 - 批量处理多个主题
4. 查看记录 - 查看历史发布记录
5. 系统配置 - 查看和修改配置
6. 退出程序
```

### 工作流程示例

```python
from xiaohongshu_publisher import XiaohongshuPublisher

# 初始化系统
system = XiaohongshuPublisher()

# 输入主题
theme = "夏季护肤小技巧"

# 生成并发布
result = system.full_workflow(theme)

if result['success']:
    print(f"发布成功！笔记ID: {result['note_id']}")
```

## 智能体说明

### 1. 策划智能体 (ContentPlanner)
- 分析主题，确定目标人群
- 选择内容角度和风格
- 生成关键词和话题标签

### 2. 文案智能体 (CopyWriter)
- 根据策略生成小红书风格文案
- 自动添加emoji和话题标签
- 支持根据反馈重新生成

### 3. 图片智能体 (ImageDesigner)
- 生成AI绘画提示词
- 支持DALL-E 3和Stable Diffusion
- 优化图片适配小红书

### 4. 审核智能体 (ContentReviewer)
- 敏感词检测
- 内容质量检查
- AI深度审核
- 自动修复问题

### 5. 发布智能体 (APIPublisher)
- 上传图片到小红书
- 创建并发布笔记
- 支持定时发布
- 记录发布历史

## 项目结构

```
.
├── main.py                 # 主程序入口
├── config.py              # 配置管理
├── logger.py              # 日志系统
├── requirements.txt       # 依赖包
├── .env.example          # 配置模板
├── xiaohongshu_publisher.py # 主系统类
├── agents/               # 智能体模块
│   ├── planner.py        # 策划智能体
│   ├── writer.py         # 文案智能体
│   ├── designer.py       # 图片智能体
│   ├── reviewer.py       # 审核智能体
│   └── publisher.py      # 发布智能体
├── generated_images/     # 生成的图片
├── publish_records/      # 发布记录
└── logs/                 # 日志文件
```

## 注意事项

1. **API配置**：需配置OpenAI API Key才能使用AI功能
2. **小红书API**：真实发布需要申请小红书开放平台权限
3. **图片生成**：DALL-E 3需要付费，Stable Diffusion需本地部署
4. **频率限制**：遵守小红书API调用频率限制
5. **内容合规**：发布前请确保内容符合平台规则

## 扩展功能

### 数据分析智能体

分析发布效果，优化后续内容策略。

### 排期智能体

根据最佳发布时间自动调度发布任务。

### 评论管理

自动回复或收集用户反馈。

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！
