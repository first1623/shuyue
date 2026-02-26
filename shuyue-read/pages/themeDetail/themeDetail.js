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
    chartData: []
  },

  // 主题配置
  themeConfigs: {
    'carbon': {
      name: '碳中和',
      icon: '🌿',
      color: '#10B981',
      darkenColor: '#059669',
      bgImage: 'https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=800',
      subtitle: '聚焦双碳目标、政策解读与行业案例',
      chartTitle: '碳排放趋势'
    },
    '13th-five': {
      name: '十三五规划',
      icon: '📊',
      color: '#DC2626',
      darkenColor: '#B91C1C',
      bgImage: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800',
      subtitle: '国家规划数字化落地案例与政策解读',
      chartTitle: '规划完成率'
    },
    'coal': {
      name: '煤炭产业',
      icon: '⛏️',
      color: '#4B5563',
      darkenColor: '#374151',
      bgImage: 'https://images.unsplash.com/photo-1565626424178-c699f6601afd?w=800',
      subtitle: '煤炭行业智能化转型与清洁利用技术',
      chartTitle: '产量趋势'
    },
    'power': {
      name: '电力能源',
      icon: '⚡',
      color: '#F59E0B',
      darkenColor: '#D97706',
      bgImage: 'https://images.unsplash.com/photo-1473341304170-971dccb5ac1e?w=800',
      subtitle: '智能电网建设与新能源并网技术',
      chartTitle: '发电量统计'
    },
    'digital-gov': {
      name: '数字化政务',
      icon: '🏛️',
      color: '#3B82F6',
      darkenColor: '#2563EB',
      bgImage: 'https://images.unsplash.com/photo-1563986768609-322da13575f3?w=800',
      subtitle: '政务服务数字化转型最佳实践',
      chartTitle: '服务指数'
    },
    'energy-transition': {
      name: '能源转型',
      icon: '🔄',
      color: '#8B5CF6',
      darkenColor: '#7C3AED',
      bgImage: 'https://images.unsplash.com/photo-1509391366360-2e959784a276?w=800',
      subtitle: '传统能源向可再生能源转型战略',
      chartTitle: '转型进度'
    }
  },

  onLoad(options) {
    // 获取系统信息
    const systemInfo = wx.getSystemInfoSync();
    this.setData({ statusBarHeight: systemInfo.statusBarHeight });
    
    // 获取主题ID
    const themeId = options.id || 'carbon';
    this.loadThemeData(themeId);
  },

  onShow() {
    // 刷新订阅状态
    this.checkSubscriptionStatus();
  },

  // 加载主题数据
  loadThemeData(themeId) {
    const config = this.themeConfigs[themeId] || this.themeConfigs['carbon'];
    
    this.setData({
      themeId: themeId,
      themeName: config.name,
      themeIcon: config.icon,
      themeColor: config.color,
      darkenColor: config.darkenColor,
      themeBgImage: config.bgImage,
      themeSubtitle: config.subtitle,
      chartTitle: config.chartTitle
    });
    
    // 加载专家团队
    this.loadExperts(themeId);
    
    // 加载智库报告
    this.loadReports(themeId);
    
    // 加载数据指标
    this.loadMetrics(themeId);
    
    // 检查订阅状态
    this.checkSubscriptionStatus();
  },

  // 检查订阅状态
  checkSubscriptionStatus() {
    const subscribedIds = wx.getStorageSync('subscribedThemes') || [];
    this.setData({
      isSubscribed: subscribedIds.includes(this.data.themeId)
    });
  },

  // 加载专家团队
  loadExperts(themeId) {
    // 模拟数据，实际应从云数据库获取
    const expertsData = {
      'carbon': [
        { id: 'e1', name: '吴擎中', title: '碳中和首席专家', avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=1' },
        { id: 'e2', name: '赵峰峰', title: '环境政策研究员', avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=2' },
        { id: 'e3', name: '李清华', title: '能源转型顾问', avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=3' },
        { id: 'e4', name: '王绿原', title: '碳交易分析师', avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=4' }
      ],
      '13th-five': [
        { id: 'e5', name: '张建国', title: '国家规划专家', avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=5' },
        { id: 'e6', name: '刘政策', title: '宏观经济研究员', avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=6' },
        { id: 'e7', name: '陈数字', title: '数字化转型顾问', avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=7' }
      ]
    };
    
    const experts = expertsData[themeId] || expertsData['carbon'];
    this.setData({ experts });
  },

  // 加载智库报告
  loadReports(themeId) {
    // 模拟数据，实际应从云数据库获取
    const reportsData = {
      'carbon': [
        { id: 'r1', icon: '📑', title: '2024年中国碳中和实施路径研究报告', author: '碳中和研究院', publishDate: '2024-01', pages: 128, type: '研究报告' },
        { id: 'r2', icon: '📊', title: '企业碳盘查与碳足迹核算指南', author: '环保部标准司', publishDate: '2024-02', pages: 86, type: '政策指南' },
        { id: 'r3', icon: '🌍', title: '全球碳交易市场发展现状分析', author: '国际金融中心', publishDate: '2024-03', pages: 156, type: '市场分析' },
        { id: 'r4', icon: '🏭', title: '重点行业碳减排技术路线白皮书', author: '工信部节能司', publishDate: '2024-01', pages: 203, type: '技术白皮书' }
      ],
      '13th-five': [
        { id: 'r5', icon: '📋', title: '十三五规划数字化项目落地案例汇编', author: '发改委数字中心', publishDate: '2024-02', pages: 245, type: '案例汇编' },
        { id: 'r6', icon: '📈', title: '规划中期评估与调整建议报告', author: '国务院发展中心', publishDate: '2024-01', pages: 167, type: '评估报告' }
      ]
    };
    
    const reports = reportsData[themeId] || reportsData['carbon'];
    this.setData({ reports });
  },

  // 加载数据指标
  loadMetrics(themeId) {
    // 模拟数据
    const metricsData = {
      'carbon': [
        { id: 'm1', value: '12%', label: '排放量下降', trend: 12, bgColor: '#10B981' },
        { id: 'm2', value: '35%', label: '可再生能源占比', trend: 8, bgColor: '#3B82F6' },
        { id: 'm3', value: '2.3亿', label: '碳交易量(吨)', trend: 25, bgColor: '#8B5CF6' }
      ],
      '13th-five': [
        { id: 'm4', value: '96%', label: '规划完成率', trend: 5, bgColor: '#DC2626' },
        { id: 'm5', value: '1.2万亿', label: '数字化投入', trend: 15, bgColor: '#F59E0B' },
        { id: 'm6', value: '85%', label: '项目落地率', trend: 10, bgColor: '#10B981' }
      ]
    };
    
    const keyMetrics = metricsData[themeId] || metricsData['carbon'];
    
    // 模拟图表数据
    const chartData = [
      { label: '1月', value: 65 },
      { label: '2月', value: 72 },
      { label: '3月', value: 68 },
      { label: '4月', value: 85 },
      { label: '5月', value: 78 },
      { label: '6月', value: 92 }
    ];
    
    this.setData({ keyMetrics, chartData });
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