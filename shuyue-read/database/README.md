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
| createTime | date | 是 | 创建时间 |

**readingHistory 数组元素结构：**
```json
{
  "pdfId": "pdf001",
  "page": 10,
  "updateTime": "2024-01-15T10:30:00.000Z"
}
```

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

## 索引建议

建议为以下字段创建索引以提升查询性能：

1. `categories` 表：`sort` 字段（升序）
2. `pdfs` 表：`categoryId` + `createTime`（复合索引）
3. `pdfs` 表：`title` + `author`（全文搜索）
4. `users` 表：`_openid`（唯一索引，默认）

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
