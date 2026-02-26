// pages/profile/profile.js
const app = getApp();

Page({
  data: {
    userInfo: null,
    stats: {
      favoriteCount: 0,
      readCount: 0,
      readingTime: 0
    }
  },

  onLoad() {
    // 检查登录状态
    this.checkLoginStatus();
  },

  onShow() {
    if (app.globalData.userInfo) {
      this.setData({ userInfo: app.globalData.userInfo });
      this.loadUserStats();
    }
  },

  // 检查登录状态
  checkLoginStatus() {
    const userInfo = wx.getStorageSync('userInfo');
    if (userInfo) {
      this.setData({ userInfo: userInfo });
      app.globalData.userInfo = userInfo;
      this.loadUserStats();
    }
  },

  // 登录
  async login() {
    try {
      // 获取用户信息
      const userInfo = await app.getUserProfile();
      
      this.setData({ userInfo: userInfo });
      
      wx.showToast({
        title: '登录成功',
        icon: 'success'
      });
      
      // 加载用户统计
      this.loadUserStats();
    } catch (err) {
      console.error('登录失败', err);
      if (err.errMsg.indexOf('getUserProfile:fail') === -1) {
        wx.showToast({
          title: '登录失败',
          icon: 'none'
        });
      }
    }
  },

  // 加载用户统计
  async loadUserStats() {
    try {
      const res = await wx.cloud.callFunction({
        name: 'getUserStats',
        data: {}
      });

      if (res.result && res.result.data) {
        this.setData({ stats: res.result.data });
      }
    } catch (err) {
      console.error('加载用户统计失败', err);
    }
  },

  // 跳转书架
  goToBookshelf() {
    if (!app.globalData.userInfo) {
      wx.showToast({
        title: '请先登录',
        icon: 'none'
      });
      return;
    }
    wx.switchTab({
      url: '/pages/bookshelf/bookshelf'
    });
  },

  // 跳转历史
  goToHistory() {
    if (!app.globalData.userInfo) {
      wx.showToast({
        title: '请先登录',
        icon: 'none'
      });
      return;
    }
    wx.navigateTo({
      url: '/pages/history/history'
    });
  },

  // 页面分享
  onShareAppMessage() {
    return {
      title: '书页阅 - 发现好书',
      path: '/pages/index/index'
    };
  }
});
