# 沐禾智心 - 微信小程序 PDF 电子书阅读器

## 项目介绍

沐禾智心是一款基于微信小程序云开发的PDF电子书阅读器，采用原生开发方式，实现了栏目展示、PDF列表、仿真翻页阅读器等核心功能。

## 技术栈

- **前端**：微信小程序原生开发
- **后端**：微信云开发（云函数 + 云数据库 + 云存储）
- **H5阅读器**：turn.js + jQuery

## 项目结构

```
shuyue-read/
├── app.js                    # 小程序入口
├── app.json                  # 小程序配置
├── app.wxss                  # 全局样式
├── project.config.json       # 项目配置
├── sitemap.json              # 网站地图
├── cloudfunctions/           # 云函数目录
│   ├── getCategories/        # 获取栏目列表
│   ├── getPdfsByCategory/    # 获取栏目PDF列表
│   ├── getPdfDetail/         # 获取PDF详情
│   ├── getUserData/          # 获取用户数据
│   ├── getPdfDetails/        # 批量获取PDF详情
│   ├── checkFavorite/        # 检查收藏状态
│   ├── updateFavorite/       # 更新收藏
│   ├── updateReadingRecord/  # 更新阅读记录
│   ├── getReadingRecord/     # 获取阅读记录
│   ├── getUserStats/         # 获取用户统计
│   ├── login/                # 用户登录
│   ├── updateUserInfo/       # 更新用户信息
│   ├── searchPdfs/           # 搜索PDF
│   └── uploadPDF/            # 上传PDF
├── pages/                    # 页面目录
│   ├── index/                # 首页
│   ├── bookshelf/            # 书架页
│   ├── detail/               # PDF详情页
│   ├── reader/               # 阅读器页面
│   ├── profile/              # 个人中心
│   ├── search/               # 搜索页
│   └── flipbook/             # H5翻页实现
├── assets/                   # 静态资源
│   └── icons/                # 图标
└── database/                 # 数据库设计文档
```

## 功能列表

### 1. 用户模块
- 微信授权登录（获取头像昵称）
- 用户数据云端存储

### 2. 首页
- 顶部栏目滑动导航
- PDF列表展示（卡片形式）
- 下拉刷新、上拉加载更多

### 3. 书架页
- 最近阅读记录
- 我的收藏列表
- 继续阅读功能

### 4. PDF详情页
- 大封面展示
- 收藏/开始阅读功能

### 5. 阅读器
- web-view 加载 H5
- 仿真翻页效果（turn.js）
- 页码同步记录

### 6. 搜索功能
- 标题/作者搜索
- 搜索结果展示

## 快速开始

### 1. 创建云开发环境
1. 登录 [微信公众平台](https://mp.weixin.qq.com/)
2. 进入云开发控制台
3. 创建环境并记录环境ID

### 2. 配置项目
1. 修改 `project.config.json` 中的 `appid`
2. 修改 `app.js` 中的云开发环境ID
3. 修改 `app.json` 中的 tabBar 图标

### 3. 创建数据库集合
在云控制台创建以下集合：
- `categories` - 栏目表
- `pdfs` - PDF资料表
- `users` - 用户表

### 4. 初始化栏目数据
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

### 5. 上传云函数
使用微信开发者工具上传所有云函数

### 6. 添加PDF数据
通过后台管理（uploadPDF云函数）添加PDF，或直接在云控制台添加测试数据。

## 核心实现

### H5 翻页实现要点

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

### 小程序接收消息

```xml
<!-- reader.wxml -->
<web-view src="{{flipbookUrl}}" bindmessage="onMessage"></web-view>
```

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

## 注意事项

1. **web-view 限制**：需要业务域名配置
2. **云存储**：图片需上传至云存储
3. **PDF转换**：建议使用工具先将PDF转为图片，再上传

## 待优化

- [ ] PDF在线转图片服务
- [ ] 阅读进度同步
- [ ] 夜间模式
- [ ] 字体大小调整

## 许可证

MIT License
