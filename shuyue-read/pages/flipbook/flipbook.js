// pages/flipbook/flipbook.js
Page({
  data: {
    loading: true,
    images: [],
    currentIndex: 0,       // 当前页索引
    nextIndex: 0,          // 下一页索引
    flipAngle: 90,         // 翻页角度
    currentAngle: 0,       // 当前页角度
    isFlipping: false,     // 是否正在翻页
    showCurrentFlip: false,// 是否显示当前页翻转
    pageHeight: 800,       // 页面高度
    showHint: true
  },

  onLoad(options) {
    const { id, page, images: imagesParam } = options;
    
    let images = [];
    
    // 解析图片参数
    if (imagesParam) {
      try {
        images = JSON.parse(decodeURIComponent(imagesParam));
      } catch (err) {
        console.error('解析图片参数失败', err);
      }
    }
    
    console.log('图片列表:', images);
    
    // 获取屏幕高度，用于计算图片显示区域
    const systemInfo = wx.getSystemInfoSync();
    const pageHeight = systemInfo.windowHeight - 200; // 留出工具栏空间
    
    // 计算当前页
    let currentIndex = (parseInt(page) || 1) - 1;
    if (currentIndex >= images.length) currentIndex = images.length - 1;
    if (currentIndex < 0) currentIndex = 0;
    
    this.setData({
      images: images,
      currentIndex: currentIndex,
      pageHeight: pageHeight,
      loading: false
    });

    // 3秒后隐藏提示
    setTimeout(() => {
      this.setData({ showHint: false });
    }, 3000);
  },

  // 下一页
  nextPage() {
    if (this.data.isFlipping || this.data.currentIndex >= this.data.images.length - 1) {
      return;
    }
    
    const currentIndex = this.data.currentIndex;
    const nextIndex = currentIndex + 1;
    
    // 开始翻页动画
    this.setData({
      isFlipping: true,
      nextIndex: nextIndex,
      flipAngle: 90,      // 下一页从90度开始（垂直）
      showCurrentFlip: false
    });
    
    // 动画：下一页从90度翻到0度（平铺）
    let angle = 90;
    const animate = () => {
      angle -= 5;
      if (angle > 0) {
        this.setData({ flipAngle: angle });
        setTimeout(animate, 16);
      } else {
        // 动画结束，显示实际页面
        this.setData({
          currentIndex: nextIndex,
          isFlipping: false,
          flipAngle: 90
        });
      }
    };
    setTimeout(animate, 50);
  },

  // 上一页
  prevPage() {
    if (this.data.isFlipping || this.data.currentIndex <= 0) {
      return;
    }
    
    const currentIndex = this.data.currentIndex;
    const prevIndex = currentIndex - 1;
    
    // 开始翻页动画
    this.setData({
      isFlipping: true,
      nextIndex: prevIndex,
      flipAngle: -90,     // 下一页（实际是上一页）从-90度开始
      showCurrentFlip: false
    });
    
    // 动画：从-90度翻到0度
    let angle = -90;
    const animate = () => {
      angle += 5;
      if (angle < 0) {
        this.setData({ flipAngle: angle });
        setTimeout(animate, 16);
      } else {
        // 动画结束
        this.setData({
          currentIndex: prevIndex,
          isFlipping: false,
          flipAngle: 90
        });
      }
    };
    setTimeout(animate, 50);
  },

  // 返回
  goBack() {
    wx.navigateBack();
  },

  onUnload() {
    // 保存阅读进度
    const pages = getCurrentPages();
    const readerPage = pages[pages.length - 2];
    if (readerPage && readerPage.updateReadingRecord) {
      readerPage.updateReadingRecord(this.data.currentIndex + 1);
    }
  }
});
