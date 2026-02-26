# 学习平台知识图谱系统 - 项目演示

## 🎉 项目概述

本项目已成功搭建基础架构，实现了从文件夹扫描到知识树构建的完整流程。

## 📁 项目结构

```
backend/
├── app/
│   ├── models/           # 数据模型层
│   │   ├── base.py              # 基础模型
│   │   ├── data_overview.py     # 文件和文件夹信息 ⭐
│   │   ├── data_relationship.py # 关系数据 ⭐
│   │   └── user_models.py       # 用户相关模型 ⭐
│   ├── views/            # API视图层
│   │   └── knowledge_tree.py    # 知识树API ⭐
│   ├── schemas/          # 数据验证层
│   │   └── knowledge_tree.py    # Pydantic模型 ⭐
│   ├── tasks/            # 异步任务层
│   │   ├── celery_worker.py     # Celery配置 ⭐
│   │   └── document_tasks.py    # 文档处理任务 ⭐
│   ├── utils/            # 工具层
│   │   └── document_parser.py   # 文档解析器 ⭐
│   ├── crawler/          # 爬虫层
│   │   └── file_scanner.py      # 文件扫描器 ⭐
│   └── core/             # 核心配置
│       ├── config.py            # 配置文件 ⭐
│       └── database.py          # 数据库连接 ⭐
├── alembic/              # 数据库迁移 ⭐
├── tests/                # 测试文件
├── scripts/              # 脚本文件
├── data/                 # 数据存储
├── requirements.txt      # Python依赖 ⭐
├── .env.example          # 环境变量示例 ⭐
├── start_server.py       # 启动脚本 ⭐
└── README.md             # 项目说明 ⭐
```

## 🌟 核心功能演示

### 1. 文件系统扫描

**功能说明：**
- 递归扫描指定路径下的所有文件夹和文件
- 自动识别文件类型（PDF、DOCX、TXT、MD等）
- 构建树形知识结构
- 提取书名和元数据信息

**API接口：**
```http
POST /api/v1/knowledge-tree/scan
GET  /api/v1/knowledge-tree/tree
GET  /api/v1/knowledge-tree/statistics
```

**示例代码：**
```python
from app.crawler.file_scanner import FileScanner

scanner = FileScanner()
result = scanner.scan_filesystem()
print(f"扫描完成，发现 {result['total_nodes']} 个节点")
```

### 2. 文档智能解析

**支持格式：**
- ✅ PDF（文本、表格提取）
- ✅ DOCX（段落、表格、样式）
- ✅ TXT（编码检测、段落分割）
- ✅ Markdown（结构化解析）

**解析内容：**
- 📝 全文内容提取
- 🏷️ 关键词自动提取
- 📚 理论引用识别
- 🔬 实验流程分析
- 📊 统计方法识别
- 💡 研究结论提取

**API接口：**
```http
POST /api/v1/knowledge-tree/process-documents
GET  /api/v1/node-detail/{node_id}
```

### 3. 异步任务处理

**Celery任务队列：**
- 📂 `scan_filesystem_task` - 文件系统扫描
- 📄 `process_document` - 单文档处理
- 📚 `batch_process_documents` - 批量文档处理

**启动方式：**
```bash
# 启动Worker
celery -A app.tasks.celery_worker worker --loglevel=info

# 或通过启动脚本
python start_server.py
```

### 4. 数据库设计亮点

**PostgreSQL关系型数据：**
- 完整的文件夹层级关系
- 文档详细信息和解析结果
- 用户收藏、笔记、搜索历史
- 灵活的关系类型和权重系统

**Neo4j图数据库：**
- 高效的关系查询
- 知识图谱可视化支持
- 复杂关系网络分析

## 🚀 快速开始

### 环境要求
- Python 3.8+
- PostgreSQL 12+
- Neo4j 4.x+
- Redis 6+

### 安装步骤

1. **克隆项目**
```bash
git clone <repository>
cd CodeBuddy/backend
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置环境**
```bash
cp .env.example .env
# 编辑 .env 文件，填入实际配置
```

4. **初始化数据库**
```bash
# 创建PostgreSQL数据库
createdb knowledge_graph

# 运行迁移
alembic upgrade head
```

5. **启动服务**
```bash
python start_server.py
```

### API测试

访问 http://localhost:8000/api/docs 查看完整的API文档。

**示例请求：**
```bash
# 触发文件扫描
curl -X POST http://localhost:8000/api/v1/knowledge-tree/scan

# 获取知识树
curl http://localhost:8000/api/v1/knowledge-tree/tree

# 获取统计信息
curl http://localhost:8000/api/v1/knowledge-tree/statistics
```

## 🎯 核心特性

### 智能化程度高
- 自动识别文档结构和内容
- AI驱动的语义分析和信息提取
- 智能关键词和主题识别

### 扩展性强
- 模块化设计，易于扩展新功能
- 支持多种文档格式
- 灵活的插件化架构

### 性能优化
- 异步任务处理，不阻塞主线程
- 智能缓存策略
- 分页和懒加载支持

### 用户体验
- RESTful API设计
- 完整的错误处理
- 详细的日志记录

## 📈 后续开发计划

### 即将实现的功能
1. **关系抽取与图谱构建** - 自动发现文档间的关联关系
2. **全文搜索引擎** - 基于Elasticsearch的高效搜索
3. **图谱可视化界面** - 交互式关系图谱展示
4. **用户管理系统** - 完整的用户认证和授权
5. **前端React应用** - 现代化的Web界面

### 技术升级方向
- 集成真实的DeepSeek API
- 实现增量扫描和更新
- 添加机器学习推荐算法
- 支持更多文档格式
- 分布式处理能力

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork项目
2. 创建特性分支
3. 提交代码
4. 推送分支
5. 创建Pull Request

## 📄 许可证

MIT License - 详见LICENSE文件

---

**项目状态：** 🟢 基础架构完成，核心功能可用  
**下一步：** 关系抽取与图谱可视化  
**预计完成时间：** 2-3周