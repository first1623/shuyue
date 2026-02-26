// pages/search/search.js
Page({
  data: {
    keyword: '',
    hasSearched: false,
    loading: false,
    resultList: [],
    hotKeywords: ['小说', '文学', '历史', '科技', '经济', '心理', '教育', '艺术']
  },

  onInput(e) {
    this.setData({ keyword: e.detail.value });
  },

  // 执行搜索
  onSearch() {
    const keyword = this.data.keyword.trim();
    if (!keyword) return;
    
    this.setData({ 
      loading: true,
      hasSearched: true 
    });
    
    wx.cloud.callFunction({
      name: 'searchPdfs',
      data: { keyword }
    }).then(res => {
      if (res.result && res.result.data) {
        this.setData({
          resultList: res.result.data,
          loading: false
        });
      } else {
        this.setData({
          resultList: [],
          loading: false
        });
      }
    }).catch(err => {
      console.error('搜索失败', err);
      this.setData({ loading: false });
      wx.showToast({
        title: '搜索失败',
        icon: 'none'
      });
    });
  },

  // 清除搜索
  clearSearch() {
    this.setData({
      keyword: '',
      hasSearched: false,
      resultList: []
    });
  },

  // 热门关键词点击
  onHotTap(e) {
    const keyword = e.currentTarget.dataset.keyword;
    this.setData({ keyword });
    this.onSearch();
  },

  // 跳转到详情
  goToDetail(e) {
    const { id } = e.currentTarget.dataset;
    wx.navigateTo({
      url: `/pages/detail/detail?id=${id}`
    });
  },

  // 返回
  goBack() {
    wx.navigateBack();
  }
});
