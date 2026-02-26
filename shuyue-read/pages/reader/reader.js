// pages/reader/reader.js
const app = getApp();

Page({
  data: {
    pdfId: '',
    currentPage: 1,
    flipbookUrl: '',
    loading: true,
    error: false,
  },

  onLoad(options) {
    const { id, page } = options;
    
    if (!id) {
      wx.showToast({
        title: '参数错误',
        icon: 'none'
      });
      setTimeout(() => {
        wx.navigateBack();
      }, 1500);
      return;
    }

    this.setData({
      pdfId: id,
      currentPage: parseInt(page) || 1
    });

    // 加载PDF详情，获取图片列表
    this.loadPdfAndOpenReader(id, parseInt(page) || 1);
  },

  // 加载PDF详情并打开阅读器
  async loadPdfAndOpenReader(pdfId, currentPage) {
    this.setData({ loading: true });
    
    let pdfData = null;
    
    // 方法1: 尝试使用云函数
    try {
      const res = await wx.cloud.callFunction({
        name: 'getPdfDetail',
        data: { pdfId }
      });
      console.log('getPdfDetail返回:', res.result);
      
      if (res.result && res.result.data) {
        pdfData = res.result.data;
      }
    } catch (cfErr) {
      console.log('云函数失败，使用数据库直连', cfErr);
    }
    
    // 方法2: 如果云函数没数据，使用数据库直连
    if (!pdfData) {
      try {
        const dbRes = await wx.cloud.database().collection('pdfs')
          .doc(pdfId)
          .get();
        console.log('数据库直连结果:', dbRes.data);
        pdfData = dbRes.data;
      } catch (dbErr) {
        console.error('数据库查询失败', dbErr);
      }
    }
    
    // 如果还是没有数据，使用模拟数据
    if (!pdfData) {
      pdfData = {
        _id: pdfId,
        title: '测试图书',
        images: [
          'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=750&h=1000&fit=crop',
          'https://images.unsplash.com/photo-1512820790803-83ca734da794?w=750&h=1000&fit=crop',
          'https://images.unsplash.com/photo-1495446815901-a7297e633e8d?w=750&h=1000&fit=crop'
        ]
      };
    }

    // 转换云存储路径
    let imageUrls = pdfData.images || [];
    console.log('原始图片路径:', imageUrls);
    
    if (imageUrls.length > 0 && imageUrls[0].startsWith('cloud://')) {
      try {
        const tempRes = await wx.cloud.getTempFileURL({ fileList: imageUrls });
        console.log('临时URL转换结果:', tempRes);
        if (tempRes.fileList) {
          imageUrls = tempRes.fileList.map(item => item.tempFileURL);
        }
      } catch (err) {
        console.error('转换图片路径失败', err);
      }
    }
    
    console.log('最终图片URL:', imageUrls);

    // 跳转到flipbook页面，传递图片列表
    const imagesParam = encodeURIComponent(JSON.stringify(imageUrls));
    wx.navigateTo({
      url: `/pages/flipbook/flipbook?id=${pdfId}&page=${currentPage}&images=${imagesParam}`,
      fail: (err) => {
        console.error('跳转失败', err);
        this.setData({ loading: false });
        wx.showToast({
          title: '打开阅读器失败',
          icon: 'none'
        });
      }
    });
  },

  // WebView加载完成
  onWebViewLoad() {
    console.log('WebView加载完成');
    this.setData({ loading: false, error: false });
  },

  // WebView加载错误
  onWebViewError(err) {
    console.error('WebView加载错误', err);
    this.setData({ loading: false, error: true });
  },

  // 接收H5发来的消息
  onMessage(e) {
    const message = e.detail.data;
    
    if (message && message.length > 0) {
      const data = message[message.length - 1];
      
      // 处理页码变化
      if (data.currentPage) {
        const page = data.currentPage;
        if (page !== this.data.currentPage) {
          this.setData({ currentPage: page });
          // 更新阅读记录
          this.updateReadingRecord(page);
        }
      }
      
      // 处理阅读完成
      if (data.finished) {
        wx.showToast({
          title: '已读完本书',
          icon: 'success'
        });
      }
    }
  },

  // 更新阅读记录
  async updateReadingRecord(page) {
    try {
      await wx.cloud.callFunction({
        name: 'updateReadingRecord',
        data: {
          pdfId: this.data.pdfId,
          page: page
        }
      });
      console.log('阅读记录已更新:', page);
    } catch (err) {
      console.error('更新阅读记录失败', err);
    }
  },

  // 重试加载
  retryLoad() {
    this.setData({ 
      loading: true, 
      error: false,
      flipbookUrl: `/pages/flipbook/flipbook?id=${this.data.pdfId}&page=${this.data.currentPage}`
    });
  },

  // 页面卸载时保存进度
  onUnload() {
    this.updateReadingRecord(this.data.currentPage);
  },

  // 返回按钮
  onBack() {
    this.updateReadingRecord(this.data.currentPage);
    wx.navigateBack();
  }
});
