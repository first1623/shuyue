# Skill 注册清单（用户 Skill）

> 本文档汇总所有 **personal（个人 Skill）**，可在任意项目中调用。

| Skill 名称 | 功能概要 | 触发条件 | 主要输出 | 存储位置 |
|------------|----------|----------|----------|----------|
| **auto-doc-generator** | 自动分析代码结构，生成带完整性标记的项目文档（🔴🟡🟢） | 需要结构化文档生成、功能规格、架构说明、完整性报告 | `auto_generated_documentation.md` | `.codebuddy/skills/auto-doc-generator/` |
| **project-analyzer** | 扫描项目目录，自动推导一至三级功能点及调用方式、数据来源 | 快速了解项目功能结构、生成功能需求清单 | `project_requirements_generated.md` | `.codebuddy/skills/project-analyzer/` |
| **prompt-collector** | 收集并分类项目中的提示词/模板，生成可检索的提示词库 | 收集复用提示词、按目的分类管理 | `prompt_library_generated.md` | `.codebuddy/skills/prompt-collector/` |
| **doc-theory-analyzer** | 文档智能监控与理论解析：提取学术/技术/管理理论，构建知识库并分析关联 | 分析文档中的理论、方法论、模型公式，构建可检索知识库 | `theory_enhanced_documentation.md` + 增强版 `大飞ai.xlsx` | `.codebuddy/skills/doc-theory-analyzer/` |

## 调用方式

- 在对话中使用 `@skill-name` 或 `invoke_integration` 调用
- 示例：`@auto-doc-generator` 可对当前项目生成完整文档
- 所有 Skill 均为 **personal** 类型，跨项目可用

## 使用示例

### 一键调用示例脚本
- 文件位置：`run_all_skills_demo.py`（项目根目录）
- 功能：依次运行所有 personal Skill 并验证输出
- 运行方法（在项目根目录执行）：
  ```bash
  py run_all_skills_demo.py
  ```
- 输出：每个 Skill 的执行状态及生成文档清单，便于快速验证

## 维护说明

- 新增 Skill 时在此清单追加记录
- 更新 SKILL_DOC_INDEX.md 方便索引查找
