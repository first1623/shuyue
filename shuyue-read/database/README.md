# 书页阅 - 数据库设计

## 概述

本文档详细描述了"书页阅"微信小程序PDF阅读器的云开发数据库设计。

## 数据表结构

### 1. `categories` - 栏目表

用于存储PDF的分类栏目信息。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| _id | string | 是 | 自动生成，唯一标识 |
| name | string | 是 | 栏目名称，如"小说"、"科技" |
| sort | number | 是 | 排序权重，数字越小越靠前 |
| createTime | date | 是 | 创建时间 |

**示例数据：**
```json
{
  "_id": "xxx123",
  "name": "文学经典",
  "sort": 1,
  "createTime": "2024-01-01T00:00:00.000Z"
}
```

### 2. `pdfs` - PDF资料表

存储PDF电子书的基本信息和图片列表。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| _id | string | 是 | 自动生成，唯一标识 |
| title | string | 是 | PDF标题 |
| author | string | 是 | 作者/来源 |
| cover | string | 是 | 封面图URL（云存储） |
| description | string | 否 | 简介/摘要 |
| pages | number | 是 | 总页数 |
| images | array | 是 | 每一页的图片URL数组（按顺序存储） |
| categoryId | string | 是 | 所属栏目ID |
| viewCount | number | 是 | 阅读次数，默认为0 |
| likeCount | number | 是 | 收藏/点赞数，默认为0 |
| status | boolean | 是 | 上架状态，true为已上架 |
| createTime | date | 是 | 创建时间 |

**示例数据：**
```json
{
  "_id": "pdf001",
  "title": "红楼梦",
  "author": "曹雪芹",
  "cover": "cloud://xxx/cover/1.jpg",
  "description": "中国古典四大名著之一",
  "pages": 120,
  "images": [
    "cloud://xxx/pages/1.jpg",
    "cloud://xxx/pages/2.jpg",
    "cloud://xxx/pages/3.jpg"
  ],
  "categoryId": "cat001",
  "viewCount": 100,
  "likeCount": 50,
  "status": true,
  "createTime": "2024-01-01T00:00:00.000Z"
}
```

### 3. `users` - 用户表

存储用户信息和阅读数据。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| _id | string | 是 | 自动生成 |
| _openid | string | 是 | 微信openid，用户唯一标识 |
| avatarUrl | string | 否 | 用户头像URL |
| nickName | string | 否 | 用户昵称 |
| favorites | array | 是 | 收藏的PDF ID列表，默认为空数组 |
| readingHistory | array | 是 | 阅读历史记录 |
| subscribedThemes | array | 是 | 订阅的主题ID列表，默认为空数组 |
| updateTime | date | 是 | 更新时间 |
| createTime | date | 是 | 创建时间 |

**readingHistory 数组元素结构：**
```json
{
  "pdfId": "pdf001",
  "page": 10,
  "updateTime": "2024-01-15T10:30:00.000Z"
}
```

**subscribedThemes 数组：**
用户订阅的主题ID列表，如 `["carbon", "power", "digital-gov"]`

**示例数据：**
```json
{
  "_id": "user001",
  "_openid": "oXXXX...",
  "avatarUrl": "cloud://xxx/avatar.jpg",
  "nickName": "书虫",
  "favorites": ["pdf001", "pdf002"],
  "readingHistory": [
    {
      "pdfId": "pdf001",
      "page": 25,
      "updateTime": "2024-01-15T10:30:00.000Z"
    }
  ],
  "subscribedThemes": ["carbon", "power"],
  "updateTime": "2024-01-15T10:30:00.000Z",
  "createTime": "2024-01-01T00:00:00.000Z"
}
```

### 4. `subscription_logs` - 主题订阅日志表

记录用户的主题订阅行为，用于数据分析和运营。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| _id | string | 是 | 自动生成 |
| userId | string | 是 | 用户ID（users表_id） |
| openId | string | 是 | 微信openid |
| themeId | string | 是 | 订阅的主题ID |
| subscribeTime | date | 是 | 订阅时间 |
| createTime | date | 是 | 记录创建时间 |

**示例数据：**
```json
{
  "_id": "sub001",
  "userId": "user001",
  "openId": "oXXXX...",
  "themeId": "carbon",
  "subscribeTime": "2024-01-15T10:30:00.000Z",
  "createTime": "2024-01-15T10:30:00.000Z"
}
```

### 5. `themes` - 主题配置表（核心）

存储主题的基本配置信息，与栏目数据关联。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| _id | string | 是 | 自动生成 |
| themeId | string | 是 | 主题唯一标识（如 carbon, power） |
| name | string | 是 | 主题名称 |
| shortName | string | 是 | 简称 |
| color | string | 是 | 主题色（如 #10B981） |
| darkenColor | string | 是 | 深色变体（如 #059669） |
| lightColor | string | 是 | 浅色背景色 |
| icon | string | 是 | 图标URL或emoji |
| bgImage | string | 是 | 主题背景图URL |
| tags | array | 是 | 主题标签 |
| description | string | 是 | 主题描述 |
| subtitle | string | 是 | 副标题描述 |
| categoryIds | array | 是 | 关联的栏目ID列表 |
| sort | number | 是 | 排序权重 |
| status | boolean | 是 | 是否启用 |
| createTime | date | 是 | 创建时间 |
| updateTime | date | 是 | 更新时间 |

**示例数据：**
```json
{
  "_id": "theme001",
  "themeId": "carbon",
  "name": "碳中和",
  "shortName": "碳中和",
  "color": "#10B981",
  "darkenColor": "#059669",
  "lightColor": "rgba(16, 185, 129, 0.15)",
  "icon": "🌿",
  "bgImage": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=800",
  "tags": ["绿色发展", "环保领域"],
  "description": "双碳目标政策解读与企业碳中和实施路径，涵盖碳盘查、碳交易等核心内容。",
  "subtitle": "聚焦双碳目标、政策解读与行业案例",
  "categoryIds": ["cat_env", "cat_energy", "cat_policy"],
  "sort": 1,
  "status": true,
  "createTime": "2024-01-01T00:00:00.000Z",
  "updateTime": "2024-01-01T00:00:00.000Z"
}
```

### 6. `experts` - 专家表

存储智库专家信息，与主题关联。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| _id | string | 是 | 自动生成 |
| expertId | string | 是 | 专家唯一标识 |
| name | string | 是 | 专家姓名 |
| title | string | 是 | 职称/头衔 |
| avatar | string | 是 | 头像URL |
| themeIds | array | 是 | 关联的主题ID列表 |
| bio | string | 否 | 个人简介 |
| organization | string | 否 | 所属机构 |
| specialty | array | 否 | 专业领域 |
| status | boolean | 是 | 是否启用 |
| createTime | date | 是 | 创建时间 |

**示例数据：**
```json
{
  "_id": "exp001",
  "expertId": "expert_001",
  "name": "吴擎中",
  "title": "碳中和首席专家",
  "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=1",
  "themeIds": ["carbon", "energy-transition"],
  "bio": "20年环保领域研究经验，主导多项国家级碳中和项目",
  "organization": "国家环境科学研究院",
  "specialty": ["碳盘查", "碳交易", "政策研究"],
  "status": true,
  "createTime": "2024-01-01T00:00:00.000Z"
}
```

### 7. `reports` - 智库报告表

存储主题相关的智库报告，关联到pdfs表或独立存储。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| _id | string | 是 | 自动生成 |
| reportId | string | 是 | 报告唯一标识 |
| title | string | 是 | 报告标题 |
| author | string | 是 | 作者/机构 |
| icon | string | 是 | 图标emoji或URL |
| themeIds | array | 是 | 关联的主题ID列表 |
| categoryIds | array | 是 | 关联的栏目ID列表 |
| pdfId | string | 否 | 关联的PDF ID（如果有完整PDF） |
| pages | number | 是 | 页数 |
| type | string | 是 | 报告类型（研究报告/政策指南/白皮书等） |
| description | string | 否 | 报告简介 |
| publishDate | string | 是 | 发布日期（如 2024-01） |
| cover | string | 否 | 封面图URL |
| viewCount | number | 是 | 阅读次数 |
| downloadCount | number | 是 | 下载次数 |
| status | boolean | 是 | 是否上架 |
| createTime | date | 是 | 创建时间 |

**示例数据：**
```json
{
  "_id": "rep001",
  "reportId": "report_001",
  "title": "2024年中国碳中和实施路径研究报告",
  "author": "碳中和研究院",
  "icon": "📑",
  "themeIds": ["carbon"],
  "categoryIds": ["cat_env", "cat_policy"],
  "pdfId": "pdf_carbon_001",
  "pages": 128,
  "type": "研究报告",
  "description": "全面分析中国碳中和目标的实施路径与关键举措",
  "publishDate": "2024-01",
  "cover": "cloud://xxx/covers/carbon_report.jpg",
  "viewCount": 1250,
  "downloadCount": 368,
  "status": true,
  "createTime": "2024-01-15T00:00:00.000Z"
}
```

### 8. `metrics` - 数据指标表

存储主题相关的数据指标和图表数据。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| _id | string | 是 | 自动生成 |
| metricId | string | 是 | 指标唯一标识 |
| themeId | string | 是 | 所属主题ID |
| name | string | 是 | 指标名称 |
| value | string | 是 | 当前值（带单位） |
| unit | string | 否 | 单位 |
| trend | number | 是 | 变化趋势百分比 |
| bgColor | string | 是 | 卡片背景色 |
| sort | number | 是 | 排序权重 |
| chartData | array | 否 | 图表数据数组 |
| timeRange | string | 是 | 时间范围（近7天/近30天等） |
| status | boolean | 是 | 是否启用 |
| updateTime | date | 是 | 更新时间 |
| createTime | date | 是 | 创建时间 |

**chartData 数组元素结构：**
```json
{
  "label": "1月",
  "value": 65,
  "date": "2024-01"
}
```

**示例数据：**
```json
{
  "_id": "met001",
  "metricId": "metric_carbon_001",
  "themeId": "carbon",
  "name": "碳排放量同比下降",
  "value": "12%",
  "trend": 12,
  "bgColor": "#10B981",
  "sort": 1,
  "chartData": [
    { "label": "1月", "value": 65, "date": "2024-01" },
    { "label": "2月", "value": 72, "date": "2024-02" },
    { "label": "3月", "value": 68, "date": "2024-03" },
    { "label": "4月", "value": 85, "date": "2024-04" },
    { "label": "5月", "value": 78, "date": "2024-05" },
    { "label": "6月", "value": 92, "date": "2024-06" }
  ],
  "timeRange": "近30天",
  "status": true,
  "updateTime": "2024-06-15T00:00:00.000Z",
  "createTime": "2024-01-01T00:00:00.000Z"
}
```

## 数据库权限配置

### categories（栏目表）
- 读取：所有用户可读
- 写入：仅管理员（可配置云函数调用）

### pdfs（PDF资料表）
- 读取：所有用户可读
- 写入：仅管理员（通过云函数 uploadPDF）

### users（用户表）
- 读取：仅用户本人
- 写入：仅用户本人（通过云函数）

**云数据库安全规则示例：**
```json
{
  "categories": {
    "read": true,
    "write": "auth.uid != null"
  },
  "pdfs": {
    "read": true,
    "write": "auth.uid != null"
  },
  "users": {
    "read": "doc._openid == auth.openid",
    "write": "doc._openid == auth.openid"
  }
}
```

## 新增云函数说明

### 1. `initDatabase` - 数据库初始化
初始化所有主题相关的数据表和基础数据。

**调用方式：**
```javascript
wx.cloud.callFunction({
  name: 'initDatabase',
  data: { type: 'all' } // 'all' | 'themes' | 'experts' | 'reports' | 'metrics'
})
```

**初始化内容：**
- 6个主题（碳中和、十三五规划、煤炭、电力、数字政务、能源转型）
- 6位专家
- 4份智库报告
- 数据指标

### 2. `getThemesList` - 获取主题列表
获取所有启用的主题列表，包含用户订阅状态。

**调用方式：**
```javascript
wx.cloud.callFunction({
  name: 'getThemesList',
  data: { page: 1, pageSize: 20 }
})
```

**返回数据：**
```json
{
  "success": true,
  "data": {
    "themes": [...],
    "total": 6,
    "hasMore": false
  }
}
```

### 3. `getThemeDetail` - 获取主题详情
获取主题的完整信息，包括专家、报告、指标、关联PDF等。

**调用方式：**
```javascript
wx.cloud.callFunction({
  name: 'getThemeDetail',
  data: { 
    themeId: 'carbon',
    timeRange: '近30天'
  }
})
```

**返回数据：**
```json
{
  "success": true,
  "data": {
    "theme": {...},
    "categories": [...],
    "experts": [...],
    "reports": [...],
    "metrics": [...],
    "pdfs": [...]
  }
}
```

### 4. `subscribeTheme` - 主题订阅
用户订阅/取消订阅主题。

### 5. `getUserSubscriptions` - 获取用户订阅列表
获取当前用户订阅的所有主题。

## 索引建议

建议为以下字段创建索引以提升查询性能：

### 必须创建的索引：

1. **themes表**
   - `themeId` (唯一)
   - `status` + `sort` (复合索引)

2. **experts表**
   - `expertId` (唯一)
   - `themeIds` (数组索引)
   - `status`

3. **reports表**
   - `reportId` (唯一)
   - `themeIds` (数组索引)
   - `status` + `publishDate` (复合索引)

4. **metrics表**
   - `metricId` (唯一)
   - `themeId` + `timeRange` (复合索引)
   - `status`

5. **原有表索引**
   - `categories` 表：`sort` 字段（升序）
   - `pdfs` 表：`categoryId` + `createTime`（复合索引）
   - `users` 表：`_openid`（唯一索引，默认）

## 注意事项

1. **images 数组**：由于小程序web-view加载H5的限制，图片建议存放在云存储中，并使用云存储的临时链接或永久链接。

2. **图片加载优化**：PDF转成的图片建议：
   - 尺寸：宽度750px（适配手机屏幕）
   - 格式：JPEG
   - 质量：80%
   - 命名：按页码顺序命名（1.jpg, 2.jpg, ...）

3. **数据量考虑**：
   - 建议单本PDF不超过500页
   - 大型PDF可考虑分章节存储

## 初始化数据

### 栏目数据初始化
```javascript
// 在云控制台或云函数中添加初始栏目
db.collection('categories').add({
  data: [
    { name: '文学经典', sort: 1 },
    { name: '小说传记', sort: 2 },
    { name: '科学技术', sort: 3 },
    { name: '历史地理', sort: 4 },
    { name: '经济管理', sort: 5 },
    { name: '人文社科', sort: 6 }
  ]
});
```
