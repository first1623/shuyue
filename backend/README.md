# 学习平台知识图谱与文档解析系统

基于文件夹结构自动构建知识图谱，支持文档智能解析、关系提取和可视化展示的学习平台。

## 技术栈

### 后端
- **框架**: Python FastAPI
- **数据库**: PostgreSQL + Neo4j (图谱存储)
- **缓存**: Redis
- **异步任务**: Celery
- **AI集成**: DeepSeek API
- **文档解析**: PyPDF2, python-docx, markdown

### 前端
- **框架**: React + TypeScript
- **UI库**: Ant Design / Element Plus
- **状态管理**: Redux Toolkit / Pinia
- **图谱可视化**: ECharts / G6 / Cytoscape.js

## 项目结构

```
backend/
├── app/                          # 应用核心代码
│   ├── models/                   # 数据模型
│   │   ├── base.py              # 基础模型
│   │   ├── data_overview.py     # 文件和文件夹信息
│   │   ├── data_relationship.py # 关系数据
│   │   └── user_models.py       # 用户相关模型
│   ├── views/                    # API视图
│   ├── serializers/             # 序列化器
│   ├── schemas/                 # Pydantic模型
│   ├── tasks/                   # Celery异步任务
│   ├── utils/                   # 工具函数
│   ├── crawler/                 # 文件系统爬虫
│   └── core/                    # 核心配置
├── alembic/                     # 数据库迁移
├── tests/                       # 测试文件
├── scripts/                     # 脚本文件
├── data/                        # 数据存储
├── requirements.txt             # Python依赖
├── .env.example                # 环境变量示例
└── README.md                   # 项目说明
```

## 快速开始

### 1. 环境准备

确保已安装：
- Python 3.8+
- PostgreSQL 12+
- Neo4j 4.x+
- Redis 6+

### 2. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 3. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，填入实际的配置信息
```

### 4. 数据库初始化

```bash
# 创建PostgreSQL数据库
createdb knowledge_graph

# 运行数据库迁移
alembic upgrade head
```

### 5. 启动服务

```bash
# 启动FastAPI应用
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# 启动Celery Worker (新终端)
celey worker --loglevel=info

# 启动Celery Beat (定时任务，新终端)
celey beat --loglevel=info
```

## API文档

启动服务后访问：
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

## 核心功能

### 1. 文件系统扫描与知识树构建
- 递归扫描指定路径下的所有文件夹和文件
- 维护文件夹层级关系，构建树形结构
- 存储至PostgreSQL `data_overview` 表

### 2. 文档解析与信息入库
- 支持PDF、DOCX、TXT、Markdown格式
- 异步任务队列处理
- 调用DeepSeek API智能解析
- 结果存入 `data_book_detail` 表

### 3. 关系抽取与图谱构建
- 分析文件间关联关系
- 支持包含、引用、相似主题等关系类型
- 同步存储至PostgreSQL和Neo4j

### 4. API接口
- 知识树结构数据获取
- 节点详情查询
- 关系图谱数据
- 全文搜索与筛选
- 用户收藏和笔记功能

## 开发指南

### 代码规范
- 遵循PEP8规范
- 使用Black格式化代码
- 编写单元测试

### 数据库操作
- 使用SQLAlchemy ORM
- 通过Alembic管理迁移
- 注意事务处理

### 异步任务
- 使用Celery处理耗时任务
- 合理设置任务超时和重试
- 监控任务执行状态

## 部署

参考 `scripts/deploy.sh` 进行生产环境部署。

## 贡献

1. Fork项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 许可证

MIT License