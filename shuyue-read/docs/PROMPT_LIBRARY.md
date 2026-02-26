# 沐禾智心 - 微信小程序 PDF 电子书阅读器 提示库

**版本**: v1.0  
**日期**: 2026-02-25  
**项目路径**: `c:\Users\zhaoy\CodeBuddy\shuyue-read`

---

## 一、用户提示（User Prompts）

### 1.1 登录与授权提示

| 位置 | 提示内容 | 类型 |
|------|----------|------|
| `app.js` | "用于完善用户资料" | 授权描述 |
| `pages/profile/profile.js` | "登录成功" | 成功提示 |
| `pages/profile/profile.js` | "登录失败" | 错误提示 |
| `pages/bookshelf/bookshelf.js` | "请先登录后查看书架" | 登录引导 |
| `pages/bookshelf/bookshelf.js` | "去登录" | 按钮文本 |
| `pages/detail/detail.js` | "请先登录" | 登录提示 |
| `pages/detail/detail.js` | "去登录" | 按钮文本 |
| `pages/profile/profile.js` | "请先登录" | 登录提示 |

### 1.2 收藏操作提示

| 位置 | 提示内容 | 类型 |
|------|----------|------|
| `pages/detail/detail.js` | "已收藏" | 成功提示 |
| `pages/detail/detail.js` | "已取消" | 成功提示 |
| `pages/detail/detail.js` | "操作失败" | 错误提示 |
| `pages/bookshelf/bookshelf.js` | "确认取消收藏" | 确认对话框标题 |
| `pages/bookshelf/bookshelf.js` | "确定要取消收藏这本书吗？" | 确认对话框内容 |
| `pages/bookshelf/bookshelf.js` | "已取消收藏" | 成功提示 |
| `pages/detail/detail.wxml` | "已收藏" / "收藏" | 按钮状态文本 |
| `pages/detail/detail.wxml` | "❤️" / "🤍" | 收藏图标 |

### 1.3 阅读相关提示

| 位置 | 提示内容 | 类型 |
|------|----------|------|
| `pages/detail/detail.js` | "开始阅读" | 对话框标题 |
| `pages/detail/detail.js` | "由于小程序web-view限制，仿真翻页功能需要在真机环境体验。\n\n当前将展示简化的阅读界面。" | 功能说明 |
| `pages/detail/detail.js` | "继续" | 按钮文本 |
| `pages/reader/reader.js` | "参数错误" | 错误提示 |
| `pages/reader/reader.js` | "已读完本书" | 完成提示 |
| `pages/reader/reader.js` | "打开阅读器失败" | 错误提示 |
| `pages/flipbook/flipbook.wxml` | "正在加载..." | 加载提示 |
| `pages/flipbook/flipbook.wxml` | "← 点击左右翻页 →" | 操作指引 |
| `pages/flipbook/flipbook.wxml` | "暂无内容" | 空状态提示 |
| `pages/flipbook/flipbook.wxml` | "📚" | 空状态图标 |
| `pages/flipbook/flipbook.wxml` | "{{currentIndex + 1}} / {{images.length}}" | 页码显示 |
| `pages/flipbook/flipbook.wxml` | "← 返回" | 返回按钮 |
| `pages/bookshelf/bookshelf.wxml` | "读到第 {{item.page}} 页" | 阅读进度 |
| `pages/bookshelf/bookshelf.wxml` | "继续阅读" | 按钮文本 |
| `pages/reader/reader.wxml` | "正在加载..." | 加载提示 |
| `pages/reader/reader.wxml` | "加载失败" | 错误提示 |
| `pages/reader/reader.wxml` | "重试" | 按钮文本 |

### 1.4 搜索相关提示

| 位置 | 提示内容 | 类型 |
|------|----------|------|
| `pages/search/search.wxml` | "搜索书名、作者..." | 搜索占位符 |
| `pages/search/search.wxml` | "取消" | 按钮文本 |
| `pages/search/search.wxml` | "搜索中..." | 加载提示 |
| `pages/search/search.wxml` | "未找到相关图书" | 空结果提示 |
| `pages/search/search.wxml` | "换个关键词试试" | 建议文本 |
| `pages/search/search.js` | "搜索失败" | 错误提示 |
| `pages/search/search.js` | 热门关键词：['小说', '文学', '历史', '科技', '经济', '心理', '教育', '艺术'] | 热门搜索标签 |
| `pages/search/search.wxml` | "热门搜索" | 区块标题 |
| `pages/index/index.wxml` | "🔍 搜索书名、作者..." | 搜索栏占位符 |

### 1.5 书架与历史提示

| 位置 | 提示内容 | 类型 |
|------|----------|------|
| `pages/bookshelf/bookshelf.wxml` | "最近阅读" | 区块标题 |
| `pages/bookshelf/bookshelf.wxml` | "我的收藏" | 区块标题 |
| `pages/bookshelf/bookshelf.wxml` | "{{favorites.length}} 本" | 收藏数量 |
| `pages/bookshelf/bookshelf.wxml` | "加载中..." | 加载提示 |
| `pages/bookshelf/bookshelf.wxml` | "暂无收藏" | 空状态 |
| `pages/bookshelf/bookshelf.wxml` | "去首页逛逛" | 引导按钮 |
| `pages/bookshelf/bookshelf.wxml` | "阅读记录" | 区块标题 |
| `pages/bookshelf/bookshelf.wxml` | "上次阅读：{{item.updateTime}}" | 时间显示 |
| `pages/bookshelf/bookshelf.js` | "刚刚" | 时间格式化 |
| `pages/bookshelf/bookshelf.js` | "X分钟前" | 时间格式化 |
| `pages/bookshelf/bookshelf.js` | "X小时前" | 时间格式化 |
| `pages/bookshelf/bookshelf.js` | "X天前" | 时间格式化 |

### 1.6 首页与列表提示

| 位置 | 提示内容 | 类型 |
|------|----------|------|
| `pages/index/index.wxml` | "加载中..." | 加载提示 |
| `pages/index/index.js` | "使用模拟数据预览" | 提示信息 |
| `pages/index/index.wxml` | "上拉加载更多" | 加载提示 |
| `pages/index/index.wxml` | "没有更多了" | 结束提示 |
| `pages/index/index.wxml` | "⚠️" | 错误图标 |
| `pages/index/index.wxml` | "数据库未初始化" | 错误标题 |
| `pages/index/index.wxml` | "暂无图书" | 空状态 |
| `pages/index/index.wxml` | "📚" | 空状态图标 |
| `pages/index/index.wxml` | "真机调试时如看不到内容，请检查网络连接或下拉刷新" | 调试提示 |
| `pages/index/index.wxml` | "使用测试数据" | 调试按钮 |

### 1.7 详情页提示

| 位置 | 提示内容 | 类型 |
|------|----------|------|
| `pages/detail/detail.wxml` | "加载中..." | 加载提示 |
| `pages/detail/detail.wxml` | "作者：{{pdf.author}}" | 作者标签 |
| `pages/detail/detail.wxml` | "{{pdf.pages}} 页" | 页数显示 |
| `pages/detail/detail.wxml` | "阅读 {{pdf.viewCount \|\| 0 }} 次" | 阅读次数 |
| `pages/detail/detail.wxml` | "简介" | 区块标题 |
| `pages/detail/detail.wxml` | "试读" | 区块标题 |
| `pages/detail/detail.js` | "预览链接已复制" | 成功提示 |
| `pages/detail/detail.js` | "请在手机浏览器中粘贴链接查看仿真翻页效果演示。\n\n演示内容包括：\n• 左右滑动翻页\n• 仿真翻页动画\n• 页码显示\n• 响应式适配" | 功能说明 |

### 1.8 个人中心提示

| 位置 | 提示内容 | 类型 |
|------|----------|------|
| `pages/profile/profile.wxml` | "微信授权登录" | 登录按钮 |
| `pages/profile/profile.wxml` | "收藏" | 统计标签 |
| `pages/profile/profile.wxml` | "阅读" | 统计标签 |
| `pages/profile/profile.wxml` | "时长(分钟)" | 统计标签 |
| `pages/profile/profile.wxml` | "我的书架" | 菜单项 |
| `pages/profile/profile.wxml` | "阅读历史" | 菜单项 |
| `pages/profile/profile.wxml` | "我的收藏" | 菜单项 |
| `pages/profile/profile.wxml` | "设置" | 菜单项 |
| `pages/profile/profile.wxml` | "关于我们" | 菜单项 |

### 1.9 分享提示

| 位置 | 提示内容 | 类型 |
|------|----------|------|
| `pages/index/index.js` | "书页阅 - 发现好书" | 分享标题 |
| `pages/bookshelf/bookshelf.js` | "我的书架 - 书页阅" | 分享标题 |
| `pages/detail/detail.js` | "书页阅 - 发现好书" | 分享标题 |
| `pages/profile/profile.js` | "书页阅 - 发现好书" | 分享标题 |

---

## 二、开发者提示（Developer Prompts）

### 2.1 代码注释与说明

#### app.js
```javascript
// 初始化云开发
// 检查登录状态
// 用户登录
// 获取用户信息并登录
```

#### pages/index/index.js
```javascript
// 栏目列表
// 当前选中的栏目索引
// PDF列表
// 当前页码
// 每页数量
// 是否还有更多
// 加载中
// 下拉刷新中
// 数据库错误状态
// 错误信息
// 加载栏目列表
// 方法1: 尝试使用云函数
// 方法2: 如果云函数没数据，使用数据库直连
// 如果有数据，显示数据
// 没有数据，使用模拟数据
// 使用模拟数据（开发测试用）
// 正在加载模拟数据...
// 加载PDF列表
// 批量转换云存储路径
// 收集所有云存储路径
// 批量获取临时URL
// 栏目切换
// 下拉刷新
// 上拉加载更多
// 跳转到搜索页
// 跳转到详情页
// 页面分享
```

#### pages/bookshelf/bookshelf.js
```javascript
// 检查登录状态
// 显示登录提示
// 加载用户数据
// 获取收藏的PDF详情
// 转换云存储路径为临时URL
// 收集云存储路径
// 获取阅读历史的PDF详情
// 格式化时间
// 继续阅读
// 跳转详情页
// 移除收藏
// 去首页
```

#### pages/detail/detail.js
```javascript
// 加载PDF详情
// 方法1: 尝试使用云函数
// 方法2: 如果云函数没数据，使用数据库直连
// 如果还是没有数据，使用模拟数据
// 使用模拟PDF详情数据
// 根据ID生成不同的模拟数据
// 默认使用pdf001的数据，或者根据ID查找
// 检查收藏状态
// 切换收藏
// 开始阅读
// 预览翻页效果
// 复制翻页HTML链接到剪贴板
// 将云存储路径转换为临时文件URL
// 批量转换云存储路径为临时文件URL
// 过滤出云存储路径
```

#### pages/reader/reader.js
```javascript
// 加载PDF详情并打开阅读器
// 方法1: 尝试使用云函数
// 方法2: 如果云函数没数据，使用数据库直连
// 如果还是没有数据，使用模拟数据
// 转换云存储路径
// 原始图片路径
// 临时URL转换结果
// 最终图片URL
// 跳转到flipbook页面，传递图片列表
// WebView加载完成
// WebView加载错误
// 接收H5发来的消息
// 处理页码变化
// 处理阅读完成
// 更新阅读记录
// 重试加载
// 页面卸载时保存进度
// 返回按钮
```

#### pages/flipbook/flipbook.js
```javascript
// 当前页索引
// 下一页索引
// 翻页角度
// 当前页角度
// 是否正在翻页
// 是否显示当前页翻转
// 页面高度
// 解析图片参数
// 获取屏幕高度，用于计算图片显示区域
// 留出工具栏空间
// 计算当前页
// 3秒后隐藏提示
// 下一页
// 开始翻页动画
// 动画：下一页从90度翻到0度（平铺）
// 动画结束，显示实际页面
// 上一页
// 动画：从-90度翻到0度
// 保存阅读进度
```

#### pages/search/search.js
```javascript
// 执行搜索
// 清除搜索
// 热门关键词点击
// 跳转到详情
// 返回
```

#### pages/profile/profile.js
```javascript
// 检查登录状态
// 登录
// 加载用户统计
// 跳转书架
// 跳转历史
```

### 2.2 云函数注释

#### cloudfunctions/login/index.js
```javascript
// 云函数: login - 用户登录
// 查询用户是否已存在
// 用户已存在，返回openid
// 新用户，创建用户记录
```

#### cloudfunctions/updateFavorite/index.js
```javascript
// 云函数: updateFavorite - 更新用户收藏
// action: 'add' 或 'remove'
// 查询用户
// 添加收藏
// 移除收藏
// 更新收藏列表
// 更新PDF的收藏数
```

#### cloudfunctions/updateReadingRecord/index.js
```javascript
// 云函数: updateReadingRecord - 更新阅读记录
// 查询用户
// 查找是否已有该PDF的阅读记录
// 更新已有记录
// 添加新记录
// 只保留最近50条记录
// 更新阅读记录
```

#### cloudfunctions/uploadPDF/index.js
```javascript
// 云函数: uploadPDF - 上传PDF并转换为图片
// 获取PDF文件
// 这里需要使用PDF转图片服务
// 可以使用 pdf-poppler 或其他Node.js库
// 由于云函数环境限制，建议使用云托管服务或第三方服务
// 示例：假设已转换为图片数组
// 实际实现需要接入图片处理服务
// 第一张作为封面
// 存储到数据库

// 注意：PDF转图片功能需要额外配置
// 建议方案：
// 1. 使用云托管部署 LibreOffice 或 PDF.js
// 2. 使用第三方PDF转图片API服务
// 3. 手动在本地转换后上传图片列表
```

#### cloudfunctions/searchPdfs/index.js
```javascript
// 云函数: searchPdfs - 搜索PDF
// 模糊搜索标题和作者
```

#### cloudfunctions/getCategories/index.js
```javascript
// 云函数: getCategories - 获取栏目列表
```

#### cloudfunctions/getPdfDetail/index.js
```javascript
// 云函数: getPdfDetail - 获取PDF详情
// 获取PDF详情
// 增加阅读次数
```

#### cloudfunctions/initDatabase/index.js
```javascript
// 云函数: initDatabase - 初始化数据库集合
// 1. 创建 categories 集合
// 集合不存在，创建它
// 2. 创建 pdfs 集合
// 3. 创建 users 集合
// 4. 初始化栏目数据
// 添加默认栏目
```

#### cloudfunctions/getUserData/index.js
```javascript
// 云函数: getUserData - 获取用户数据
// 查询用户
```

#### cloudfunctions/getUserStats/index.js
```javascript
// 云函数: getUserStats - 获取用户统计
// 查询用户
// 可后续添加阅读时长统计
```

#### cloudfunctions/checkFavorite/index.js
```javascript
// 云函数: checkFavorite - 检查是否收藏
// 查询用户
```

#### cloudfunctions/getReadingRecord/index.js
```javascript
// 云函数: getReadingRecord - 获取阅读记录
// 查询用户
```

#### cloudfunctions/updateUserInfo/index.js
```javascript
// 云函数: updateUserInfo - 更新用户信息
// 查询用户
// 更新用户信息
```

#### cloudfunctions/getPdfsByCategory/index.js
```javascript
// 云函数: getPdfsByCategory - 获取栏目下的PDF列表
// 获取PDF列表（不返回images以节省流量）
// 只返回已上架的
```

#### cloudfunctions/getPdfDetails/index.js
```javascript
// 云函数: getPdfDetails - 批量获取PDF详情
// 批量查询
```

---

## 三、错误提示（Error Prompts）

### 3.1 用户错误提示

| 位置 | 错误提示 | 场景 |
|------|----------|------|
| `pages/search/search.js` | "搜索失败" | 搜索异常 |
| `pages/bookshelf/bookshelf.js` | "操作失败" | 取消收藏失败 |
| `pages/detail/detail.js` | "操作失败" | 收藏操作失败 |
| `pages/reader/reader.js` | "参数错误" | 缺少PDF ID |
| `pages/reader/reader.js` | "打开阅读器失败" | 页面跳转失败 |
| `pages/profile/profile.js` | "登录失败" | 授权失败 |
| `pages/index/index.wxml` | "数据库未初始化" | 数据库连接失败 |
| `pages/reader/reader.wxml` | "加载失败" | WebView加载失败 |

### 3.2 开发者错误日志

| 位置 | 错误日志 | 类型 |
|------|----------|------|
| `app.js` | "云开发初始化完成，环境ID: zhaozoe-4gb1vhek6b687186" | 初始化日志 |
| `pages/index/index.js` | "getCategories返回:", "云函数失败，使用数据库直连", "数据库直连结果:", "数据库查询失败", "获取栏目失败", "没有获取到栏目数据，使用模拟数据" | 调试日志 |
| `pages/detail/detail.js` | "getPdfDetail返回:", "云函数失败，使用数据库直连", "数据库直连结果:", "数据库查询失败", "检查收藏状态失败", "更新收藏失败" | 调试日志 |
| `pages/reader/reader.js` | "getPdfDetail返回:", "云函数失败，使用数据库直连", "数据库直连结果:", "数据库查询失败", "原始图片路径:", "临时URL转换结果:", "最终图片URL:", "转换图片路径失败", "跳转失败", "更新阅读记录失败" | 调试日志 |
| `pages/bookshelf/bookshelf.js` | "加载用户数据失败", "获取收藏详情失败", "转换云存储路径失败", "获取阅读历史详情失败" | 调试日志 |
| `pages/flipbook/flipbook.js` | "解析图片参数失败" | 调试日志 |
| `pages/profile/profile.js` | "加载用户统计失败", "登录失败" | 调试日志 |
| `cloudfunctions/*/index.js` | "登录失败", "更新收藏失败", "更新阅读记录失败", "上传PDF失败", "搜索失败", "获取栏目失败", "获取PDF详情失败", "初始化失败:", "获取用户数据失败", "获取用户统计失败", "检查收藏状态失败", "获取阅读记录失败", "更新用户信息失败", "获取PDF列表失败", "批量获取PDF详情失败" | 云函数错误 |

---

## 四、功能描述（Feature Descriptions）

### 4.1 项目概述

**来自 README.md:**

> 沐禾智心是一款基于微信小程序云开发的PDF电子书阅读器，采用原生开发方式，实现了栏目展示、PDF列表、仿真翻页阅读器等核心功能。

### 4.2 技术栈

- **前端**：微信小程序原生开发
- **后端**：微信云开发（云函数 + 云数据库 + 云存储）
- **H5阅读器**：turn.js + jQuery

### 4.3 功能模块

#### 用户模块
- 微信授权登录（获取头像昵称）
- 用户数据云端存储

#### 首页
- 顶部栏目滑动导航
- PDF列表展示（卡片形式）
- 下拉刷新、上拉加载更多

#### 书架页
- 最近阅读记录
- 我的收藏列表
- 继续阅读功能

#### PDF详情页
- 大封面展示
- 收藏/开始阅读功能

#### 阅读器
- web-view 加载 H5
- 仿真翻页效果（turn.js）
- 页码同步记录

#### 搜索功能
- 标题/作者搜索
- 搜索结果展示

### 4.4 核心实现说明

**H5 翻页实现要点:**
```javascript
// 初始化 turn.js
$('#flipbook').turn({
  width: 屏幕宽度,
  height: 屏幕高度,
  autoCenter: true,
  elevation: 50,
  when: {
    turned: function(event, page, view) {
      // 翻页完成时发送消息给小程序
      wx.miniProgram.postMessage({
        data: { currentPage: page }
      });
    }
  }
});
```

**小程序接收消息:**
```javascript
// reader.js
onMessage(e) {
  const data = e.detail.data[0];
  if (data.currentPage) {
    // 更新阅读记录
    this.updateReadingRecord(data.currentPage);
  }
}
```

### 4.5 注意事项

1. **web-view 限制**：需要业务域名配置
2. **云存储**：图片需上传至云存储
3. **PDF转换**：建议使用工具先将PDF转为图片，再上传

### 4.6 待优化功能

- [ ] PDF在线转图片服务
- [ ] 阅读进度同步
- [ ] 夜间模式
- [ ] 字体大小调整

---

## 五、数据库文档提示（Database Documentation）

### 5.1 数据表结构

#### categories - 栏目表

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| _id | string | 是 | 自动生成，唯一标识 |
| name | string | 是 | 栏目名称，如"小说"、"科技" |
| sort | number | 是 | 排序权重，数字越小越靠前 |
| createTime | date | 是 | 创建时间 |

**示例数据:**
```json
{
  "_id": "xxx123",
  "name": "文学经典",
  "sort": 1,
  "createTime": "2024-01-01T00:00:00.000Z"
}
```

#### pdfs - PDF资料表

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

**示例数据:**
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

#### users - 用户表

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| _id | string | 是 | 自动生成 |
| _openid | string | 是 | 微信openid，用户唯一标识 |
| avatarUrl | string | 否 | 用户头像URL |
| nickName | string | 否 | 用户昵称 |
| favorites | array | 是 | 收藏的PDF ID列表，默认为空数组 |
| readingHistory | array | 是 | 阅读历史记录 |
| createTime | date | 是 | 创建时间 |

**readingHistory 数组元素结构:**
```json
{
  "pdfId": "pdf001",
  "page": 10,
  "updateTime": "2024-01-15T10:30:00.000Z"
}
```

### 5.2 数据库权限配置

**categories（栏目表）**
- 读取：所有用户可读
- 写入：仅管理员（可配置云函数调用）

**pdfs（PDF资料表）**
- 读取：所有用户可读
- 写入：仅管理员（通过云函数 uploadPDF）

**users（用户表）**
- 读取：仅用户本人
- 写入：仅用户本人（通过云函数）

### 5.3 索引建议

1. `categories` 表：`sort` 字段（升序）
2. `pdfs` 表：`categoryId` + `createTime`（复合索引）
3. `pdfs` 表：`title` + `author`（全文搜索）
4. `users` 表：`_openid`（唯一索引，默认）

### 5.4 图片加载优化建议

- **尺寸**：宽度750px（适配手机屏幕）
- **格式**：JPEG
- **质量**：80%
- **命名**：按页码顺序命名（1.jpg, 2.jpg, ...）

### 5.5 数据量考虑

- 建议单本PDF不超过500页
- 大型PDF可考虑分章节存储

---

## 六、快速开始指南

### 6.1 创建云开发环境

1. 登录 [微信公众平台](https://mp.weixin.qq.com/)
2. 进入云开发控制台
3. 创建环境并记录环境ID

### 6.2 配置项目

1. 修改 `project.config.json` 中的 `appid`
2. 修改 `app.js` 中的云开发环境ID
3. 修改 `app.json` 中的 tabBar 图标

### 6.3 创建数据库集合

在云控制台创建以下集合：
- `categories` - 栏目表
- `pdfs` - PDF资料表
- `users` - 用户表

### 6.4 初始化栏目数据

```javascript
// 在云控制台或云函数中添加
db.collection('categories').add({
  data: [
    { name: '文学经典', sort: 1 },
    { name: '小说传记', sort: 2 },
    { name: '科学技术', sort: 3 },
    // ...
  ]
});
```

### 6.5 上传云函数

使用微信开发者工具上传所有云函数

### 6.6 添加PDF数据

通过后台管理（uploadPDF云函数）添加PDF，或直接在云控制台添加测试数据。

---

## 七、文件路径汇总

### 7.1 JavaScript 文件

| 文件路径 | 说明 |
|----------|------|
| `c:/Users/zhaoy/CodeBuddy/shuyue-read/app.js` | 小程序入口 |
| `c:/Users/zhaoy/CodeBuddy/shuyue-read/pages/index/index.js` | 首页逻辑 |
| `c:/Users/zhaoy/CodeBuddy/shuyue-read/pages/bookshelf/bookshelf.js` | 书架页逻辑 |
| `c:/Users/zhaoy/CodeBuddy/shuyue-read/pages/detail/detail.js` | 详情页逻辑 |
| `c:/Users/zhaoy/CodeBuddy/shuyue-read/pages/reader/reader.js` | 阅读器逻辑 |
| `c:/Users/zhaoy/CodeBuddy/shuyue-read/pages/flipbook/flipbook.js` | 翻页实现逻辑 |
| `c:/Users/zhaoy/CodeBuddy/shuyue-read/pages/search/search.js` | 搜索页逻辑 |
| `c:/Users/zhaoy/CodeBuddy/shuyue-read/pages/profile/profile.js` | 个人中心逻辑 |
| `c:/Users/zhaoy/CodeBuddy/shuyue-read/cloudfunctions/login/index.js` | 用户登录云函数 |
| `c:/Users/zhaoy/CodeBuddy/shuyue-read/cloudfunctions/updateFavorite/index.js` | 更新收藏云函数 |
| `c:/Users/zhaoy/CodeBuddy/shuyue-read/cloudfunctions/updateReadingRecord/index.js` | 更新阅读记录云函数 |
| `c:/Users/zhaoy/CodeBuddy/shuyue-read/cloudfunctions/uploadPDF/index.js` | 上传PDF云函数 |
| `c:/Users/zhaoy/CodeBuddy/shuyue-read/cloudfunctions/searchPdfs/index.js` | 搜索PDF云函数 |
| `c:/Users/zhaoy/CodeBuddy/shuyue-read/cloudfunctions/getCategories/index.js` | 获取栏目云函数 |
| `c:/Users/zhaoy/CodeBuddy/shuyue-read/cloudfunctions/getPdfDetail/index.js` | 获取PDF详情云函数 |
| `c:/Users/zhaoy/CodeBuddy/shuyue-read/cloudfunctions/initDatabase/index.js` | 初始化数据库云函数 |
| `c:/Users/zhaoy/CodeBuddy/shuyue-read/cloudfunctions/getUserData/index.js` | 获取用户数据云函数 |
| `c:/Users/zhaoy/CodeBuddy/shuyue-read/cloudfunctions/getUserStats/index.js` | 获取用户统计云函数 |
| `c:/Users/zhaoy/CodeBuddy/shuyue-read/cloudfunctions/checkFavorite/index.js` | 检查收藏状态云函数 |
| `c:/Users/zhaoy/CodeBuddy/shuyue-read/cloudfunctions/getReadingRecord/index.js` | 获取阅读记录云函数 |
| `c:/Users/zhaoy/CodeBuddy/shuyue-read/cloudfunctions/updateUserInfo/index.js` | 更新用户信息云函数 |
| `c:/Users/zhaoy/CodeBuddy/shuyue-read/cloudfunctions/getPdfsByCategory/index.js` | 获取栏目PDF列表云函数 |
| `c:/Users/zhaoy/CodeBuddy/shuyue-read/cloudfunctions/getPdfDetails/index.js` | 批量获取PDF详情云函数 |

### 7.2 WXML 文件

| 文件路径 | 说明 |
|----------|------|
| `c:/Users/zhaoy/CodeBuddy/shuyue-read/pages/index/index.wxml` | 首页模板 |
| `c:/Users/zhaoy/CodeBuddy/shuyue-read/pages/bookshelf/bookshelf.wxml` | 书架页模板 |
| `c:/Users/zhaoy/CodeBuddy/shuyue-read/pages/detail/detail.wxml` | 详情页模板 |
| `c:/Users/zhaoy/CodeBuddy/shuyue-read/pages/reader/reader.wxml` | 阅读器模板 |
| `c:/Users/zhaoy/CodeBuddy/shuyue-read/pages/flipbook/flipbook.wxml` | 翻页模板 |
| `c:/Users/zhaoy/CodeBuddy/shuyue-read/pages/search/search.wxml` | 搜索页模板 |
| `c:/Users/zhaoy/CodeBuddy/shuyue-read/pages/profile/profile.wxml` | 个人中心模板 |

### 7.3 文档文件

| 文件路径 | 说明 |
|----------|------|
| `c:/Users/zhaoy/CodeBuddy/shuyue-read/README.md` | 项目说明文档 |
| `c:/Users/zhaoy/CodeBuddy/shuyue-read/database/README.md` | 数据库设计文档 |

---

*本提示库由 Agent 自动生成，包含沐禾智心微信小程序项目的所有用户提示、开发者注释、错误信息和功能说明。*
