// pages/bookshelf/bookshelf.js
const app = getApp();

Page({
  data: {
    loading: true,
    recentRead: [], // 最近阅读
    favorites: [], // 收藏列表
    readingHistory: [], // 阅读历史
  },

  onLoad() {
    this.checkLogin();
  },

  onShow() {
    if (app.globalData.userInfo) {
      this.loadUserData();
    }
  },

  // 检查登录状态
  checkLogin() {
    if (!app.globalData.userInfo) {
      this.showLoginTip();
    } else {
      this.loadUserData();
    }
  },

  // 显示登录提示
  showLoginTip() {
    wx.showModal({
      title: '提示',
      content: '请先登录后查看书架',
      confirmText: '去登录',
      success: (res) => {
        if (res.confirm) {
          wx.switchTab({
            url: '/pages/profile/profile'
          });
        }
      }
    });
  },

  // 加载用户数据
  async loadUserData() {
    this.setData({ loading: true });
    
    try {
      const res = await wx.cloud.callFunction({
        name: 'getUserData',
        data: {}
      });

      if (res.result && res.result.data) {
        const userData = res.result.data;
        const favorites = userData.favorites || [];
        const readingHistory = userData.readingHistory || [];
        
        // 获取收藏的PDF详情
        if (favorites.length > 0) {
          const favDetails = await this.getFavoriteDetails(favorites);
          this.setData({ favorites: favDetails });
        }
        
        // 处理最近阅读数据
        if (readingHistory.length > 0) {
          const recentDetails = await this.getReadingHistoryDetails(readingHistory);
          this.setData({ recentRead: recentDetails.slice(0, 5) });
        }
        
        this.setData({ 
          readingHistory: readingHistory.slice(0, 10),
          loading: false 
        });
      } else {
        this.setData({ loading: false });
      }
    } catch (err) {
      console.error('加载用户数据失败', err);
      this.setData({ loading: false });
    }
  },

  // 获取收藏的PDF详情
  async getFavoriteDetails(favoriteIds) {
    try {
      const res = await wx.cloud.callFunction({
        name: 'getPdfDetails',
        data: {
          ids: favoriteIds
        }
      });
      const details = res.result && res.result.data ? res.result.data : [];
      return await this.convertCloudPaths(details);
    } catch (err) {
      console.error('获取收藏详情失败', err);
      return [];
    }
  },

  // 转换云存储路径为临时URL
  async convertCloudPaths(list) {
    if (!list || list.length === 0) return list;
    
    // 收集云存储路径
    const cloudCovers = [];
    const pdfMap = {};
    
    list.forEach((pdf, index) => {
      if (pdf.cover && pdf.cover.startsWith('cloud://')) {
        cloudCovers.push(pdf.cover);
        pdfMap[pdf.cover] = index;
      }
    });
    
    if (cloudCovers.length === 0) return list;
    
    try {
      const res = await wx.cloud.getTempFileURL({ fileList: cloudCovers });
      if (res.fileList) {
        res.fileList.forEach(item => {
          const index = pdfMap[item.fileID];
          if (index !== undefined && item.tempFileURL) {
            list[index].cover = item.tempFileURL;
          }
        });
      }
    } catch (err) {
      console.error('转换云存储路径失败', err);
    }
    
    return list;
  },

  // 获取阅读历史的PDF详情
  async getReadingHistoryDetails(history) {
    const pdfIds = history.map(item => item.pdfId);
    try {
      const res = await wx.cloud.callFunction({
        name: 'getPdfDetails',
        data: {
          ids: pdfIds
        }
      });
      
      if (res.result && res.result.data) {
        // 合并详情和阅读记录
        const detailsMap = {};
        res.result.data.forEach(item => {
          detailsMap[item._id] = item;
        });
        
        return history.map(item => ({
          ...detailsMap[item.pdfId],
          page: item.page,
          updateTime: this.formatTime(item.updateTime)
        })).filter(item => item._id);
      }
      return [];
    } catch (err) {
      console.error('获取阅读历史详情失败', err);
      return [];
    }
  },

  // 格式化时间
  formatTime(timestamp) {
    if (!timestamp) return '';
    const date = new Date(timestamp);
    const now = new Date();
    const diff = now - date;
    
    if (diff < 60000) return '刚刚';
    if (diff < 3600000) return Math.floor(diff / 60000) + '分钟前';
    if (diff < 86400000) return Math.floor(diff / 3600000) + '小时前';
    if (diff < 604800000) return Math.floor(diff / 86400000) + '天前';
    
    return `${date.getMonth() + 1}-${date.getDate()}`;
  },

  // 继续阅读
  continueReading(e) {
    const { id, page } = e.currentTarget.dataset;
    wx.navigateTo({
      url: `/pages/reader/reader?id=${id}&page=${page || 1}`
    });
  },

  // 跳转详情页
  goToDetail(e) {
    const { id } = e.currentTarget.dataset;
    wx.navigateTo({
      url: `/pages/detail/detail?id=${id}`
    });
  },

  // 移除收藏
  async removeFavorite(e) {
    const { id } = e.currentTarget.dataset;
    
    wx.showModal({
      title: '确认取消收藏',
      content: '确定要取消收藏这本书吗？',
      success: async (res) => {
        if (res.confirm) {
          try {
            await wx.cloud.callFunction({
              name: 'updateFavorite',
              data: {
                pdfId: id,
                action: 'remove'
              }
            });
            
            wx.showToast({
              title: '已取消收藏',
              icon: 'success'
            });
            
            // 刷新列表
            this.loadUserData();
          } catch (err) {
            console.error('取消收藏失败', err);
            wx.showToast({
              title: '操作失败',
              icon: 'none'
            });
          }
        }
      }
    });
  },

  // 去首页
  goToIndex() {
    wx.switchTab({
      url: '/pages/index/index'
    });
  },

  // 页面分享
  onShareAppMessage() {
    return {
      title: '我的书架 - 书页阅',
      path: '/pages/bookshelf/bookshelf'
    };
  }
});
