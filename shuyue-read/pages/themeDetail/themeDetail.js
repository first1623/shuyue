Page({
  data: {
    // 系统信息
    statusBarHeight: 44,
    
    // 主题信息
    themeId: '',
    themeName: '',
    themeIcon: '🌿',
    themeColor: '#10B981',
    darkenColor: '#059669',
    themeBgImage: '',
    themeSubtitle: '',
    isSubscribed: false,
    
    // 时间筛选
    timeFilter: '近30天',
    timeFilters: ['近7天', '近30天', '近90天', '近一年', '全部'],
    showFilterPopup: false,
    
    // 专家团队
    experts: [],
    
    // 智库报告
    reports: [],
    
    // 关键指标
    keyMetrics: [],
    
    // 图表数据
    chartTitle: '趋势分析',
    chartData: [],
    
    // 加载状态
    loading: true
  },

  onLoad(options) {
    // 获取系统信息
    const systemInfo = wx.getSystemInfoSync();
    this.setData({ statusBarHeight: systemInfo.statusBarHeight });
    
    // 获取主题ID
    const themeId = options.id || 'carbon';
    this.setData({ themeId });
    
    // 从数据库加载主题数据
    this.loadThemeDataFromDB(themeId);
  },

  onShow() {
    // 页面显示时刷新数据
    if (this.data.themeId) {
      this.loadThemeDataFromDB(this.data.themeId);
    }
  },

  // 从数据库加载主题数据
  async loadThemeDataFromDB(themeId) {
    this.setData({ loading: true });
    
    wx.showLoading({ title: '加载中...' });
    
    try {
      const res = await wx.cloud.callFunction({
        name: 'getThemeDetail',
        data: {
          themeId: themeId,
          timeRange: this.data.timeFilter
        }
      });

      if (res.result.success) {
        const data = res.result.data;
        
        this.setData({
          themeId: data.theme.id,
          themeName: data.theme.name,
          themeIcon: data.theme.icon,
          themeColor: data.theme.color,
          darkenColor: data.theme.darkenColor,
          themeBgImage: data.theme.bgImage,
          themeSubtitle: data.theme.subtitle,
          isSubscribed: data.theme.isSubscribed,
          experts: data.experts,
          reports: data.reports,
          keyMetrics: data.metrics.slice(0, 3),
          chartData: data.metrics[0]?.chartData || [],
          loading: false
        });
      } else {
        // 如果云函数失败，使用本地备用数据
        console.log('云函数获取失败，使用本地数据:', res.result.message);
        this.loadThemeDataLocal(themeId);
      }
    } catch (err) {
      console.error('获取主题数据失败:', err);
      // 使用本地备用数据
      this.loadThemeDataLocal(themeId);
    } finally {
      wx.hideLoading();
    }
  },

  // 本地备用数据（云函数失败时使用）
  loadThemeDataLocal(themeId) {
    const themeConfigs = {
      'carbon': {
        name: '碳中和',
        icon: '🌿',
        color: '#10B981',
        darkenColor: '#059669',
        bgImage: 'https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=800',
        subtitle: '聚焦双碳目标、政策解读与行业案例'
      },
      '13th-five': {
        name: '十三五规划',
        icon: '📊',
        color: '#DC2626',
        darkenColor: '#B91C1C',
        bgImage: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800',
        subtitle: '国家规划数字化落地案例与政策解读'
      }
    };
    
    const config = themeConfigs[themeId] || themeConfigs['carbon'];
    const subscribedIds = wx.getStorageSync('subscribedThemes') || [];
    
    this.setData({
      themeName: config.name,
      themeIcon: config.icon,
      themeColor: config.color,
      darkenColor: config.darkenColor,
      themeBgImage: config.bgImage,
      themeSubtitle: config.subtitle,
      isSubscribed: subscribedIds.includes(themeId),
      experts: [
        { id: 'e1', name: '吴擎中', title: '碳中和首席专家', avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=1' },
        { id: 'e2', name: '赵峰峰', title: '环境政策研究员', avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=2' }
      ],
      reports: [
        { id: 'r1', icon: '📑', title: '2024年中国碳中和实施路径研究报告', author: '碳中和研究院', publishDate: '2024-01', pages: 128, type: '研究报告' }
      ],
      keyMetrics: [
        { id: 'm1', name: '碳排放量下降', value: '12%', trend: 12, bgColor: '#10B981' }
      ],
      chartData: [
        { label: '1月', value: 65 },
        { label: '2月', value: 72 },
        { label: '3月', value: 68 }
      ],
      loading: false
    });
  },

  // 订阅/取消订阅
  onSubscribe() {
    const { themeId, isSubscribed, themeName } = this.data;
    
    if (isSubscribed) {
      wx.showModal({
        title: '取消订阅',
        content: `确定取消订阅「${themeName}」主题吗？`,
        success: (res) => {
          if (res.confirm) {
            this.toggleSubscription(false);
          }
        }
      });
    } else {
      this.toggleSubscription(true);
    }
  },

  // 切换订阅状态
  toggleSubscription(subscribe) {
    const { themeId, themeName } = this.data;
    let subscribedIds = wx.getStorageSync('subscribedThemes') || [];
    
    if (subscribe) {
      if (!subscribedIds.includes(themeId)) {
        subscribedIds.push(themeId);
      }
      wx.showToast({ title: '订阅成功', icon: 'success' });
    } else {
      subscribedIds = subscribedIds.filter(id => id !== themeId);
      wx.showToast({ title: '已取消订阅', icon: 'none' });
    }
    
    wx.setStorageSync('subscribedThemes', subscribedIds);
    this.setData({ isSubscribed: subscribe });
    
    // 同步到云端
    this.syncToCloud(subscribe);
  },

  // 同步到云端
  async syncToCloud(subscribe) {
    try {
      await wx.cloud.callFunction({
        name: 'subscribeTheme',
        data: {
          themeId: this.data.themeId,
          action: subscribe ? 'subscribe' : 'unsubscribe'
        }
      });
    } catch (err) {
      console.log('云端同步失败', err);
    }
  },

  // 点击专家
  onExpertTap(e) {
    const expertId = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: `/pages/expertDetail/expertDetail?id=${expertId}`
    });
  },

  // 点击报告
  onReportTap(e) {
    const reportId = e.currentTarget.dataset.id;
    // 跳转到现有详情页
    wx.navigateTo({
      url: `/pages/detail/detail?id=${reportId}`
    });
  },

  // 查看全部专家
  viewAllExperts() {
    wx.navigateTo({
      url: `/pages/expertList/expertList?themeId=${this.data.themeId}`
    });
  },

  // 查看全部报告
  viewAllReports() {
    wx.navigateTo({
      url: `/pages/reportList/reportList?themeId=${this.data.themeId}`
    });
  },

  // 查看全部指标
  viewAllMetrics() {
    wx.navigateTo({
      url: `/pages/metricsDetail/metricsDetail?themeId=${this.data.themeId}`
    });
  },

  // 时间筛选
  onTimeFilterChange() {
    this.setData({ showFilterPopup: true });
  },

  // 关闭弹窗
  closeFilterPopup() {
    this.setData({ showFilterPopup: false });
  },

  // 阻止事件冒泡
  stopPropagation() {
    // 阻止点击穿透
  },

  // 选择时间筛选
  selectTimeFilter(e) {
    const value = e.currentTarget.dataset.value;
    this.setData({ 
      timeFilter: value,
      showFilterPopup: false 
    });
    // 重新加载数据
    this.loadMetrics(this.data.themeId);
  },

  // 返回上一页
  goBack() {
    wx.navigateBack();
  },

  // 分享
  onShare() {
    wx.showShareMenu({
      withShareTicket: true,
      menus: ['shareAppMessage', 'shareTimeline']
    });
  },

  // 分享配置
  onShareAppMessage() {
    const { themeName, themeId } = this.data;
    return {
      title: `${themeName}主题 - 沐禾智心`,
      path: `/pages/themeDetail/themeDetail?id=${themeId}`,
      imageUrl: '/assets/images/share-theme.png'
    };
  },

  onShareTimeline() {
    const { themeName, themeId } = this.data;
    return {
      title: `${themeName}主题 - 沐禾智心`,
      query: `id=${themeId}`
    };
  }
});