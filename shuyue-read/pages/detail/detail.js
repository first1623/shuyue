// pages/detail/detail.js
const app = getApp();

Page({
  data: {
    loading: true,
    pdf: null,
    isFavorite: false,
    previewImages: [],
    pdfId: '',
  },

  onLoad(options) {
    if (options.id) {
      this.setData({ pdfId: options.id });
      this.loadPdfDetail(options.id);
    }
  },

  onShow() {
    // 刷新收藏状态
    if (this.data.pdfId) {
      this.checkFavoriteStatus();
    }
  },

  // 加载PDF详情
  async loadPdfDetail(pdfId) {
    this.setData({ loading: true });
    
    let pdf = null;
    
    // 方法1: 尝试使用云函数
    try {
      const res = await wx.cloud.callFunction({
        name: 'getPdfDetail',
        data: { pdfId }
      });
      console.log('getPdfDetail返回:', res.result);
      
      if (res.result && res.result.data) {
        pdf = res.result.data;
      }
    } catch (cfErr) {
      console.log('云函数失败，使用数据库直连', cfErr);
    }
    
    // 方法2: 如果云函数没数据，使用数据库直连
    if (!pdf) {
      try {
        const dbRes = await wx.cloud.database().collection('pdfs')
          .doc(pdfId)
          .get();
        console.log('数据库直连结果:', dbRes.data);
        pdf = dbRes.data;
      } catch (dbErr) {
        console.error('数据库查询失败', dbErr);
      }
    }
    
    // 如果还是没有数据，使用模拟数据
    if (!pdf) {
      this.useMockPdfDetail(pdfId);
      return;
    }
    
    // 转换云存储路径为临时URL
    if (pdf.cover && pdf.cover.startsWith('cloud://')) {
      pdf.cover = await this.getTempFileURL(pdf.cover);
    }
    
    // 转换预览图片
    let previewImages = [];
    if (pdf.images && pdf.images.length > 0) {
      const tempUrls = await this.getTempFileURLs(pdf.images.slice(0, 5));
      previewImages = tempUrls;
    }
    
    this.setData({
      pdf,
      previewImages,
      loading: false
    });
    
    // 更新标题
    wx.setNavigationBarTitle({
      title: pdf.title
    });
    
    // 检查收藏状态
    this.checkFavoriteStatus();
  },

  // 使用模拟PDF详情数据
  useMockPdfDetail(pdfId) {
    // 根据ID生成不同的模拟数据
    const mockPdfs = {
      'pdf001': {
        _id: 'pdf001',
        title: '红楼梦',
        author: '曹雪芹',
        cover: 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=300&h=400&fit=crop',
        description: '《红楼梦》，中国古代章回体长篇小说，中国古典四大名著之一。小说以贾、史、王、薛四大家族的兴衰为背景，以富贵公子贾宝玉为视角，以贾宝玉与林黛玉、薛宝钗的爱情婚姻悲剧为主线，描绘了一批举止见识出于须眉之上的闺阁佳人的人生百态。',
        pages: 10,
        images: [
          'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=750&h=1000&fit=crop',
          'https://images.unsplash.com/photo-1512820790803-83ca734da794?w=750&h=1000&fit=crop',
          'https://images.unsplash.com/photo-1495446815901-a7297e633e8d?w=750&h=1000&fit=crop',
          'https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=750&h=1000&fit=crop',
          'https://images.unsplash.com/photo-1516979187457-637abb4f9353?w=750&h=1000&fit=crop',
          'https://images.unsplash.com/photo-1543002588-bfa74002ed7e?w=750&h=1000&fit=crop',
          'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=750&h=1000&fit=crop',
          'https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=750&h=1000&fit=crop',
          'https://images.unsplash.com/photo-1519682337058-a94d519337bc?w=750&h=1000&fit=crop',
          'https://images.unsplash.com/photo-1524578271613-d550eacf6090?w=750&h=1000&fit=crop'
        ]
      }
    };

    // 默认使用pdf001的数据，或者根据ID查找
    let pdf = mockPdfs[pdfId];
    if (!pdf) {
      pdf = mockPdfs['pdf001'];
      pdf._id = pdfId;
    }

    const previewImages = pdf.images.slice(0, 5);

    this.setData({
      pdf,
      previewImages,
      loading: false
    });

    wx.setNavigationBarTitle({
      title: pdf.title
    });
  },

  // 检查收藏状态
  async checkFavoriteStatus() {
    try {
      const res = await wx.cloud.callFunction({
        name: 'checkFavorite',
        data: { pdfId: this.data.pdfId }
      });

      if (res.result) {
        this.setData({ isFavorite: res.result.isFavorite });
      }
    } catch (err) {
      console.error('检查收藏状态失败', err);
    }
  },

  // 切换收藏
  async toggleFavorite() {
    const userInfo = app.globalData.userInfo;
    if (!userInfo) {
      wx.showModal({
        title: '提示',
        content: '请先登录',
        confirmText: '去登录',
        success: (res) => {
          if (res.confirm) {
            wx.switchTab({
              url: '/pages/profile/profile'
            });
          }
        }
      });
      return;
    }

    const action = this.data.isFavorite ? 'remove' : 'add';
    
    try {
      await wx.cloud.callFunction({
        name: 'updateFavorite',
        data: {
          pdfId: this.data.pdfId,
          action: action
        }
      });

      this.setData({ isFavorite: !this.data.isFavorite });
      
      wx.showToast({
        title: this.data.isFavorite ? '已收藏' : '已取消',
        icon: 'success'
      });
    } catch (err) {
      console.error('更新收藏失败', err);
      wx.showToast({
        title: '操作失败',
        icon: 'none'
      });
    }
  },

  // 开始阅读
  startReading() {
    const { pdfId } = this.data;
    
    wx.showModal({
      title: '开始阅读',
      content: '由于小程序web-view限制，仿真翻页功能需要在真机环境体验。\n\n当前将展示简化的阅读界面。',
      confirmText: '继续',
      success: (res) => {
        if (res.confirm) {
          wx.navigateTo({
            url: `/pages/reader/reader?id=${pdfId}&page=1`
          });
        }
      }
    });
  },

  // 预览翻页效果
  previewFlipbook() {
    // 复制翻页HTML链接到剪贴板
    const demoUrl = 'https://htmlpreview.github.io/?https://raw.githubusercontent.com/turnjs/turnjs/main/demos/magazine/index.html';
    
    wx.setClipboardData({
      data: demoUrl,
      success: () => {
        wx.showModal({
          title: '预览链接已复制',
          content: '请在手机浏览器中粘贴链接查看仿真翻页效果演示。\n\n演示内容包括：\n• 左右滑动翻页\n• 仿真翻页动画\n• 页码显示\n• 响应式适配',
          showCancel: false
        });
      }
    });
  },

  // 页面分享
  onShareAppMessage() {
    const { pdf } = this.data;
    return {
      title: pdf ? pdf.title : '书页阅 - 发现好书',
      path: `/pages/detail/detail?id=${this.data.pdfId}`,
      imageUrl: pdf ? pdf.cover : ''
    };
  },

  // 将云存储路径转换为临时文件URL
  getTempFileURL(filePath) {
    return new Promise((resolve) => {
      if (!filePath || !filePath.startsWith('cloud://')) {
        resolve(filePath);
        return;
      }
      wx.cloud.getTempFileURL({
        fileList: [filePath],
        success: (res) => {
          if (res.fileList && res.fileList[0]) {
            resolve(res.fileList[0].tempFileURL);
          } else {
            resolve(filePath);
          }
        },
        fail: () => {
          resolve(filePath);
        }
      });
    });
  },

  // 批量转换云存储路径为临时文件URL
  getTempFileURLs(filePaths) {
    return new Promise(async (resolve) => {
      if (!filePaths || filePaths.length === 0) {
        resolve([]);
        return;
      }
      
      // 过滤出云存储路径
      const cloudPaths = filePaths.filter(p => p && p.startsWith('cloud://'));
      const httpPaths = filePaths.filter(p => p && !p.startsWith('cloud://'));
      
      if (cloudPaths.length === 0) {
        resolve(filePaths);
        return;
      }
      
      wx.cloud.getTempFileURL({
        fileList: cloudPaths,
        success: (res) => {
          const tempUrls = res.fileList.map(item => item.tempFileURL);
          resolve([...httpPaths, ...tempUrls]);
        },
        fail: () => {
          resolve(filePaths);
        }
      });
    });
  }
});
