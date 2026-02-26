// pages/index/index.js
const app = getApp();

Page({
  data: {
    categories: [], // 栏目列表
    currentCategoryIndex: 0, // 当前选中的栏目索引
    pdfList: [], // PDF列表
    page: 1, // 当前页码
    pageSize: 10, // 每页数量
    hasMore: true, // 是否还有更多
    loading: true, // 加载中
    refreshing: false, // 下拉刷新中
    dbError: false, // 数据库错误状态
    errorMessage: '', // 错误信息
  },

  onLoad() {
    this.loadCategories();
  },

  onShow() {
    // 每次显示页面时刷新数据
    if (this.data.categories.length > 0 && !this.data.dbError) {
      this.loadPdfList();
    }
  },

  // 加载栏目列表
  async loadCategories() {
    try {
      // 方法1: 尝试使用云函数
      let categories = [];
      try {
        const res = await wx.cloud.callFunction({
          name: 'getCategories',
          data: {}
        });
        console.log('getCategories返回:', res.result);
        if (res.result && res.result.data && res.result.data.length > 0) {
          categories = res.result.data;
        }
      } catch (cfErr) {
        console.log('云函数失败，使用数据库直连', cfErr);
      }
      
      // 方法2: 如果云函数没数据，使用数据库直连
      if (categories.length === 0) {
        try {
          const dbRes = await wx.cloud.database().collection('categories')
            .orderBy('sort', 'asc')
            .get();
          console.log('数据库直连结果:', dbRes.data);
          categories = dbRes.data || [];
        } catch (dbErr) {
          console.error('数据库查询失败', dbErr);
        }
      }
      
      // 如果有数据，显示数据
      if (categories.length > 0) {
        app.globalData.categories = categories;
        this.setData({
          categories: categories,
          currentCategoryIndex: 0,
          dbError: false
        });
        this.loadPdfList();
      } else {
        // 没有数据，使用模拟数据
        console.log('没有获取到栏目数据，使用模拟数据');
        this.useMockData();
      }
    } catch (err) {
      console.error('获取栏目失败', err);
      // 使用模拟数据让界面可以预览
      this.useMockData();
    }
  },

  // 使用模拟数据（开发测试用）
  useMockData() {
    console.log('正在加载模拟数据...');
    
    const mockCategories = [
      { _id: '1', name: '文学经典', sort: 1 },
      { _id: '2', name: '小说传记', sort: 2 },
      { _id: '3', name: '科学技术', sort: 3 },
      { _id: '4', name: '历史地理', sort: 4 }
    ];

    // 模拟PDF数据
    const mockPdfs = [
      {
        _id: 'pdf001',
        title: '红楼梦',
        author: '曹雪芹',
        cover: 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=300&h=400&fit=crop',
        pages: 120,
        description: '中国古典四大名著之一'
      },
      {
        _id: 'pdf002',
        title: '西游记',
        author: '吴承恩',
        cover: 'https://images.unsplash.com/photo-1512820790803-83ca734da794?w=300&h=400&fit=crop',
        pages: 100,
        description: '中国古代第一部浪漫主义章回体长篇神魔小说'
      },
      {
        _id: 'pdf003',
        title: '水浒传',
        author: '施耐庵',
        cover: 'https://images.unsplash.com/photo-1495446815901-a7297e633e8d?w=300&h=400&fit=crop',
        pages: 90,
        description: '中国四大名著之一'
      },
      {
        _id: 'pdf004',
        title: '三国演义',
        author: '罗贯中',
        cover: 'https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=300&h=400&fit=crop',
        pages: 110,
        description: '中国第一部长篇章回体历史演义小说'
      },
      {
        _id: 'pdf005',
        title: '活着',
        author: '余华',
        cover: 'https://images.unsplash.com/photo-1516979187457-637abb4f9353?w=300&h=400&fit=crop',
        pages: 80,
        description: '讲述了农村人福贵悲惨的人生遭遇'
      },
      {
        _id: 'pdf006',
        title: '围城',
        author: '钱钟书',
        cover: 'https://images.unsplash.com/photo-1543002588-bfa74002ed7e?w=300&h=400&fit=crop',
        pages: 95,
        description: '一部充满智慧的讽刺小说'
      }
    ];

    this.setData({
      categories: mockCategories,
      currentCategoryIndex: 0,
      loading: false,
      pdfList: mockPdfs,
      hasMore: false
    });

    wx.showToast({
      title: '使用模拟数据预览',
      icon: 'none'
    });
  },

  // 加载PDF列表
  async loadPdfList(isLoadMore = false) {
    if (isLoadMore && !this.data.hasMore) return;
    
    const currentCategory = this.data.categories[this.data.currentCategoryIndex];
    if (!currentCategory) return;

    console.log('当前栏目:', currentCategory);

    if (!isLoadMore) {
      this.setData({ loading: true, page: 1 });
    }

    let pdfList = [];
    
    // 方法1: 尝试使用云函数
    try {
      const res = await wx.cloud.callFunction({
        name: 'getPdfsByCategory',
        data: {
          categoryId: currentCategory._id,
          page: this.data.page,
          pageSize: this.data.pageSize
        }
      });
      console.log('PDF列表返回:', res.result);
      if (res.result && res.result.data && res.result.data.length > 0) {
        pdfList = res.result.data;
      }
    } catch (cfErr) {
      console.log('云函数失败，使用数据库直连', cfErr);
    }
    
    // 方法2: 如果云函数没数据，使用数据库直连
    if (pdfList.length === 0) {
      try {
        const dbRes = await wx.cloud.database().collection('pdfs')
          .where({
            categoryId: currentCategory._id,
            status: true
          })
          .field({
            _id: true,
            title: true,
            author: true,
            cover: true,
            pages: true,
            viewCount: true,
            description: true
          })
          .orderBy('createTime', 'desc')
          .skip((this.data.page - 1) * this.data.pageSize)
          .limit(this.data.pageSize)
          .get();
        
        console.log('数据库直连结果:', dbRes.data);
        pdfList = dbRes.data || [];
      } catch (dbErr) {
        console.error('数据库查询失败', dbErr);
      }
    }

    // 更新数据
    if (pdfList.length > 0) {
      let newList = isLoadMore 
        ? [...this.data.pdfList, ...pdfList]
        : pdfList;
      
      // 转换云存储路径为临时URL
      newList = await this.convertCloudPaths(newList);
      
      this.setData({
        pdfList: newList,
        hasMore: pdfList.length >= this.data.pageSize,
        loading: false,
        refreshing: false
      });
    } else {
      this.setData({
        loading: false,
        refreshing: false
      });
    }
  },

  // 批量转换云存储路径
  async convertCloudPaths(list) {
    if (!list || list.length === 0) return list;
    
    // 收集所有云存储路径
    const cloudCovers = [];
    const pdfMap = {};
    
    list.forEach((pdf, index) => {
      if (pdf.cover && pdf.cover.startsWith('cloud://')) {
        cloudCovers.push(pdf.cover);
        pdfMap[pdf.cover] = index;
      }
    });
    
    if (cloudCovers.length === 0) return list;
    
    // 批量获取临时URL
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

  // 栏目切换
  onCategoryChange(e) {
    const { index } = e.currentTarget.dataset;
    if (index === this.data.currentCategoryIndex) return;

    this.setData({
      currentCategoryIndex: index,
      pdfList: [],
      page: 1,
      hasMore: true
    });

    this.loadPdfList();
  },

  // 下拉刷新
  onRefresh() {
    if (this.data.dbError) {
      this.loadCategories();
      return;
    }
    this.setData({ refreshing: true });
    this.loadPdfList();
  },

  // 上拉加载更多
  onLoadMore() {
    if (this.data.hasMore && !this.data.loading) {
      this.setData({ page: this.data.page + 1 });
      this.loadPdfList(true);
    }
  },

  // 跳转到搜索页
  goToSearch() {
    wx.navigateTo({
      url: '/pages/search/search'
    });
  },

  // 跳转到详情页
  goToDetail(e) {
    const { id } = e.currentTarget.dataset;
    wx.navigateTo({
      url: `/pages/detail/detail?id=${id}`
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
