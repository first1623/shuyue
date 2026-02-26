Page({
  data: {
    // 状态栏高度
    statusBarHeight: 44,
    // 当前选中卡片索引
    currentIndex: 0,
    // 选中的主题ID（漂浮区域）
    selectedThemeId: null,
    // 主题总数
    themeCount: 6,
    // 剩余未查看数量
    remainingCount: 0,
    // 主题数据 - 使用emoji作为临时图标，生产环境建议替换为专用图标
    themes: [
      {
        id: 'carbon',
        name: '碳中和',
        shortName: '碳中和',
        iconType: 'emoji',
        icon: '🌿',
        color: '#10B981',
        lightColor: 'rgba(16, 185, 129, 0.15)',
        tags: ['绿色发展', '环保领域'],
        description: '双碳目标政策解读与企业碳中和实施路径，涵盖碳盘查、碳交易等核心内容。',
        position: 'position-0',
        delay: 0,
        isSubscribed: false
      },
      {
        id: '13th-five',
        name: '十三五规划',
        shortName: '十三五',
        iconType: 'emoji',
        icon: '📊',
        color: '#DC2626',
        lightColor: 'rgba(220, 38, 38, 0.15)',
        tags: ['国家规划', '宏观政策'],
        description: '十三五规划数字化项目落地案例与政策解读，助力政企高效执行。',
        position: 'position-1',
        delay: 0.2,
        isSubscribed: false
      },
      {
        id: 'coal',
        name: '煤炭产业',
        shortName: '煤炭',
        iconType: 'emoji',
        icon: '⛏️',
        color: '#4B5563',
        lightColor: 'rgba(75, 85, 99, 0.15)',
        tags: ['传统能源', '产业转型'],
        description: '煤炭行业智能化转型与清洁利用技术，推动产业升级与绿色发展。',
        position: 'position-2',
        delay: 0.4,
        isSubscribed: false
      },
      {
        id: 'power',
        name: '电力能源',
        shortName: '电力',
        iconType: 'emoji',
        icon: '⚡',
        color: '#F59E0B',
        lightColor: 'rgba(245, 158, 11, 0.15)',
        tags: ['电力行业', '新能源'],
        description: '智能电网建设与新能源并网技术，聚焦电力行业数字化转型实践。',
        position: 'position-3',
        delay: 0.6,
        isSubscribed: false
      },
      {
        id: 'digital-gov',
        name: '数字化政务',
        shortName: '数字政务',
        iconType: 'emoji',
        icon: '🏛️',
        color: '#3B82F6',
        lightColor: 'rgba(59, 130, 246, 0.15)',
        tags: ['政府数字化', '智慧城市'],
        description: '政务服务数字化转型最佳实践，一网通办、数据共享等创新应用。',
        position: 'position-4',
        delay: 0.8,
        isSubscribed: false
      },
      {
        id: 'energy-transition',
        name: '能源转型',
        shortName: '能源转型',
        iconType: 'emoji',
        icon: '🔄',
        color: '#8B5CF6',
        lightColor: 'rgba(139, 92, 246, 0.15)',
        tags: ['能源革命', '可再生'],
        description: '传统能源向可再生能源转型战略，储能技术与多能互补解决方案。',
        position: 'position-5',
        delay: 1.0,
        isSubscribed: false
      }
    ]
  },

  onLoad() {
    // 获取系统信息
    const systemInfo = wx.getSystemInfoSync();
    this.setData({
      statusBarHeight: systemInfo.statusBarHeight,
      themeCount: this.data.themes.length
    });
    
    this.updateRemainingCount();
    
    // 加载已订阅状态
    this.loadSubscriptionStatus();
  },

  onShow() {
    // 页面显示时更新订阅状态
    this.loadSubscriptionStatus();
  },

  // 加载订阅状态
  loadSubscriptionStatus() {
    const subscribedIds = wx.getStorageSync('subscribedThemes') || [];
    const themes = this.data.themes.map(theme => ({
      ...theme,
      isSubscribed: subscribedIds.includes(theme.id)
    }));
    this.setData({ themes });
  },

  // 更新剩余数量提示
  updateRemainingCount() {
    const remaining = this.data.themes.length - this.data.currentIndex - 1;
    this.setData({
      remainingCount: Math.max(0, remaining)
    });
  },

  // 漂浮主题点击
  onThemeSelect(e) {
    const themeId = e.currentTarget.dataset.id;
    const themeIndex = this.data.themes.findIndex(t => t.id === themeId);
    
    this.setData({
      selectedThemeId: themeId,
      currentIndex: themeIndex
    });
    
    this.updateRemainingCount();
  },

  // Swiper切换
  onSwiperChange(e) {
    const currentIndex = e.detail.current;
    const currentTheme = this.data.themes[currentIndex];
    
    this.setData({
      currentIndex: currentIndex,
      selectedThemeId: currentTheme.id
    });
    
    this.updateRemainingCount();
  },

  // 订阅按钮点击
  onSubscribe(e) {
    const themeId = e.currentTarget.dataset.id;
    const theme = this.data.themes.find(t => t.id === themeId);
    
    if (theme.isSubscribed) {
      wx.showToast({
        title: '已订阅该主题',
        icon: 'none'
      });
      return;
    }
    
    // 获取已订阅列表
    let subscribedIds = wx.getStorageSync('subscribedThemes') || [];
    
    if (!subscribedIds.includes(themeId)) {
      subscribedIds.push(themeId);
      wx.setStorageSync('subscribedThemes', subscribedIds);
      
      // 更新本地数据
      const themes = this.data.themes.map(t => 
        t.id === themeId ? { ...t, isSubscribed: true } : t
      );
      this.setData({ themes });
      
      wx.showToast({
        title: '订阅成功',
        icon: 'success'
      });
      
      // 同步到云数据库（可选）
      this.syncSubscriptionToCloud(themeId);
    }
  },

  // 同步订阅到云端
  async syncSubscriptionToCloud(themeId) {
    try {
      await wx.cloud.callFunction({
        name: 'subscribeTheme',
        data: {
          themeId: themeId,
          subscribeTime: new Date().toISOString()
        }
      });
    } catch (err) {
      console.log('云端同步失败，已本地保存', err);
    }
  },

  // 关闭按钮
  onClose() {
    wx.showModal({
      title: '提示',
      content: '确定要离开主题订阅页面吗？',
      success: (res) => {
        if (res.confirm) {
          // 返回首页或上一页
          wx.switchTab({
            url: '/pages/index/index'
          });
        }
      }
    });
  },

  // 跳转到主题详情
  goToThemeDetail(themeId) {
    const theme = this.data.themes.find(t => t.id === themeId);
    if (theme) {
      wx.navigateTo({
        url: `/pages/themeDetail/themeDetail?id=${themeId}&name=${encodeURIComponent(theme.name)}`
      });
    }
  },

  // 点击卡片查看更多
  onCardTap(e) {
    const themeId = e.currentTarget.dataset.id;
    this.goToThemeDetail(themeId);
  },

  // 分享功能
  onShareAppMessage() {
    return {
      title: '沐禾智心 - 订阅行业主题，获取专属内容',
      path: '/pages/themes/themes',
      imageUrl: '/assets/images/share-themes.png'
    };
  }
});