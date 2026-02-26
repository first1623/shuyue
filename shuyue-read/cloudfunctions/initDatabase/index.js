const cloud = require('wx-server-sdk');

cloud.init({
  env: cloud.DYNAMIC_CURRENT_ENV
});

const db = cloud.database();
const _ = db.command;

// ==================== 栏目数据定义 ====================
// 定义与主题关联的栏目结构
const categoriesData = [
  // 碳中和相关栏目
  { categoryId: 'cat_env_policy', name: '环保政策', sort: 1, type: 'theme_related' },
  { categoryId: 'cat_carbon_trading', name: '碳交易市场', sort: 2, type: 'theme_related' },
  { categoryId: 'cat_green_tech', name: '绿色技术', sort: 3, type: 'theme_related' },
  // 十三五规划相关栏目
  { categoryId: 'cat_national_plan', name: '国家规划', sort: 4, type: 'theme_related' },
  { categoryId: 'cat_digital_case', name: '数字化案例', sort: 5, type: 'theme_related' },
  // 能源相关栏目
  { categoryId: 'cat_energy_policy', name: '能源政策', sort: 6, type: 'theme_related' },
  { categoryId: 'cat_smart_grid', name: '智能电网', sort: 7, type: 'theme_related' },
  { categoryId: 'cat_renewable', name: '新能源', sort: 8, type: 'theme_related' },
  // 煤炭产业相关栏目
  { categoryId: 'cat_coal_tech', name: '煤炭技术', sort: 9, type: 'theme_related' },
  { categoryId: 'cat_clean_energy', name: '清洁能源', sort: 10, type: 'theme_related' },
  // 政务数字化相关栏目
  { categoryId: 'cat_gov_digital', name: '政务数字化', sort: 11, type: 'theme_related' },
  { categoryId: 'cat_smart_city', name: '智慧城市', sort: 12, type: 'theme_related' },
  // 基础栏目
  { categoryId: 'cat_think_tank', name: '智库报告', sort: 13, type: 'base' },
  { categoryId: 'cat_data_report', name: '数据报告', sort: 14, type: 'base' }
];

// ==================== 主题与栏目关联映射 ====================
const themeCategoryMapping = {
  'carbon': ['cat_env_policy', 'cat_carbon_trading', 'cat_green_tech', 'cat_think_tank', 'cat_data_report'],
  '13th-five': ['cat_national_plan', 'cat_digital_case', 'cat_think_tank', 'cat_data_report'],
  'coal': ['cat_energy_policy', 'cat_coal_tech', 'cat_clean_energy', 'cat_think_tank'],
  'power': ['cat_energy_policy', 'cat_smart_grid', 'cat_renewable', 'cat_think_tank', 'cat_data_report'],
  'digital-gov': ['cat_gov_digital', 'cat_smart_city', 'cat_digital_case', 'cat_think_tank'],
  'energy-transition': ['cat_energy_policy', 'cat_renewable', 'cat_clean_energy', 'cat_think_tank', 'cat_data_report']
};

// 动态生成主题数据（categoryIds 将在初始化时填入）
const getThemesData = (categoryMap) => [
  {
    themeId: 'carbon',
    name: '碳中和',
    shortName: '碳中和',
    color: '#10B981',
    darkenColor: '#059669',
    lightColor: 'rgba(16, 185, 129, 0.15)',
    icon: '🌿',
    bgImage: 'https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=800',
    tags: ['绿色发展', '环保领域'],
    description: '双碳目标政策解读与企业碳中和实施路径，涵盖碳盘查、碳交易等核心内容。',
    subtitle: '聚焦双碳目标、政策解读与行业案例',
    categoryIds: categoryMap['carbon'] || [],
    sort: 1,
    status: true
  },
  {
    themeId: '13th-five',
    name: '十三五规划',
    shortName: '十三五',
    color: '#DC2626',
    darkenColor: '#B91C1C',
    lightColor: 'rgba(220, 38, 38, 0.15)',
    icon: '📊',
    bgImage: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800',
    tags: ['国家规划', '宏观政策'],
    description: '十三五规划数字化项目落地案例与政策解读，助力政企高效执行。',
    subtitle: '国家规划数字化落地案例与政策解读',
    categoryIds: categoryMap['13th-five'] || [],
    sort: 2,
    status: true
  },
  {
    themeId: 'coal',
    name: '煤炭产业',
    shortName: '煤炭',
    color: '#4B5563',
    darkenColor: '#374151',
    lightColor: 'rgba(75, 85, 99, 0.15)',
    icon: '⛏️',
    bgImage: 'https://images.unsplash.com/photo-1565626424178-c699f6601afd?w=800',
    tags: ['传统能源', '产业转型'],
    description: '煤炭行业智能化转型与清洁利用技术，推动产业升级与绿色发展。',
    subtitle: '煤炭行业智能化转型与清洁利用技术',
    categoryIds: categoryMap['coal'] || [],
    sort: 3,
    status: true
  },
  {
    themeId: 'power',
    name: '电力能源',
    shortName: '电力',
    color: '#F59E0B',
    darkenColor: '#D97706',
    lightColor: 'rgba(245, 158, 11, 0.15)',
    icon: '⚡',
    bgImage: 'https://images.unsplash.com/photo-1473341304170-971dccb5ac1e?w=800',
    tags: ['电力行业', '新能源'],
    description: '智能电网建设与新能源并网技术，聚焦电力行业数字化转型实践。',
    subtitle: '智能电网建设与新能源并网技术',
    categoryIds: categoryMap['power'] || [],
    sort: 4,
    status: true
  },
  {
    themeId: 'digital-gov',
    name: '数字化政务',
    shortName: '数字政务',
    color: '#3B82F6',
    darkenColor: '#2563EB',
    lightColor: 'rgba(59, 130, 246, 0.15)',
    icon: '🏛️',
    bgImage: 'https://images.unsplash.com/photo-1563986768609-322da13575f3?w=800',
    tags: ['政府数字化', '智慧城市'],
    description: '政务服务数字化转型最佳实践，一网通办、数据共享等创新应用。',
    subtitle: '政务服务数字化转型最佳实践',
    categoryIds: categoryMap['digital-gov'] || [],
    sort: 5,
    status: true
  },
  {
    themeId: 'energy-transition',
    name: '能源转型',
    shortName: '能源转型',
    color: '#8B5CF6',
    darkenColor: '#7C3AED',
    lightColor: 'rgba(139, 92, 246, 0.15)',
    icon: '🔄',
    bgImage: 'https://images.unsplash.com/photo-1509391366360-2e959784a276?w=800',
    tags: ['能源革命', '可再生'],
    description: '传统能源向可再生能源转型战略，储能技术与多能互补解决方案。',
    subtitle: '传统能源向可再生能源转型战略',
    categoryIds: categoryMap['energy-transition'] || [],
    sort: 6,
    status: true
  }
];
    darkenColor: '#2563EB',
    lightColor: 'rgba(59, 130, 246, 0.15)',
    icon: '🏛️',
    bgImage: 'https://images.unsplash.com/photo-1563986768609-322da13575f3?w=800',
    tags: ['政府数字化', '智慧城市'],
    description: '政务服务数字化转型最佳实践，一网通办、数据共享等创新应用。',
    subtitle: '政务服务数字化转型最佳实践',
    categoryIds: [],
    sort: 5,
    status: true
  },
  {
    themeId: 'energy-transition',
    name: '能源转型',
    shortName: '能源转型',
    color: '#8B5CF6',
    darkenColor: '#7C3AED',
    lightColor: 'rgba(139, 92, 246, 0.15)',
    icon: '🔄',
    bgImage: 'https://images.unsplash.com/photo-1509391366360-2e959784a276?w=800',
    tags: ['能源革命', '可再生'],
    description: '传统能源向可再生能源转型战略，储能技术与多能互补解决方案。',
    subtitle: '传统能源向可再生能源转型战略',
    categoryIds: [],
    sort: 6,
    status: true
  }
];

// 初始化专家数据
const expertsData = [
  {
    expertId: 'expert_001',
    name: '吴擎中',
    title: '碳中和首席专家',
    avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=1',
    themeIds: ['carbon', 'energy-transition'],
    bio: '20年环保领域研究经验，主导多项国家级碳中和项目',
    organization: '国家环境科学研究院',
    specialty: ['碳盘查', '碳交易', '政策研究'],
    status: true
  },
  {
    expertId: 'expert_002',
    name: '赵峰峰',
    title: '环境政策研究员',
    avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=2',
    themeIds: ['carbon'],
    bio: '专注环境政策研究15年，参与起草多项国家环保标准',
    organization: '生态环境部政策研究中心',
    specialty: ['环境政策', '碳排放核算'],
    status: true
  },
  {
    expertId: 'expert_003',
    name: '李清华',
    title: '能源转型顾问',
    avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=3',
    themeIds: ['carbon', 'energy-transition', 'power'],
    bio: '能源领域资深专家，曾任职于国际能源署',
    organization: '清华大学能源环境经济研究所',
    specialty: ['能源转型', '可再生能源'],
    status: true
  },
  {
    expertId: 'expert_004',
    name: '王绿原',
    title: '碳交易分析师',
    avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=4',
    themeIds: ['carbon'],
    bio: '全国碳市场建设核心成员，碳交易机制设计专家',
    organization: '上海环境能源交易所',
    specialty: ['碳交易', '碳市场'],
    status: true
  },
  {
    expertId: 'expert_005',
    name: '张建国',
    title: '国家规划专家',
    avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=5',
    themeIds: ['13th-five', 'digital-gov'],
    bio: '国家发改委规划司前司长，参与多期国家规划制定',
    organization: '国务院发展研究中心',
    specialty: ['国家规划', '政策制定'],
    status: true
  },
  {
    expertId: 'expert_006',
    name: '刘政策',
    title: '宏观经济研究员',
    avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=6',
    themeIds: ['13th-five'],
    bio: '宏观经济研究专家，专注于五年规划评估',
    organization: '中国社会科学院',
    specialty: ['宏观经济', '规划评估'],
    status: true
  }
];

// 初始化报告数据
const reportsData = [
  {
    reportId: 'report_carbon_001',
    title: '2024年中国碳中和实施路径研究报告',
    author: '碳中和研究院',
    icon: '📑',
    themeIds: ['carbon'],
    categoryIds: ['cat_env_policy', 'cat_think_tank'],
    pages: 128,
    type: '研究报告',
    description: '全面分析中国碳中和目标的实施路径与关键举措',
    publishDate: '2024-01',
    viewCount: 1250,
    downloadCount: 368,
    status: true
  },
  {
    reportId: 'report_carbon_002',
    title: '企业碳盘查与碳足迹核算指南',
    author: '环保部标准司',
    icon: '📊',
    themeIds: ['carbon'],
    categoryIds: ['cat_green_tech', 'cat_data_report'],
    pages: 86,
    type: '政策指南',
    description: '企业碳盘查标准化操作指南与核算方法',
    publishDate: '2024-02',
    viewCount: 890,
    downloadCount: 245,
    status: true
  },
  {
    reportId: 'report_carbon_003',
    title: '全球碳交易市场发展现状分析',
    author: '国际金融中心',
    icon: '🌍',
    themeIds: ['carbon'],
    categoryIds: ['cat_carbon_trading', 'cat_data_report'],
    pages: 156,
    type: '市场分析',
    description: '全球主要碳交易市场运行机制与价格走势分析',
    publishDate: '2024-03',
    viewCount: 2100,
    downloadCount: 567,
    status: true
  },
  {
    reportId: 'report_13th_001',
    title: '十三五规划数字化项目落地案例汇编',
    author: '发改委数字中心',
    icon: '📋',
    themeIds: ['13th-five'],
    categoryIds: ['cat_national_plan', 'cat_digital_case'],
    pages: 245,
    type: '案例汇编',
    description: '汇总十三五期间数字化项目成功案例',
    publishDate: '2024-02',
    viewCount: 1500,
    downloadCount: 420,
    status: true
  }
];

// 动态转换报告的categoryIds为真实ID
const getReportsData = (categoryIdMap) => {
  return reportsData.map(report => ({
    ...report,
    categoryIds: report.categoryIds.map(catId => categoryIdMap[catId]).filter(id => id)
  }));
};

// 初始化指标数据
const metricsData = [
  {
    metricId: 'metric_carbon_001',
    themeId: 'carbon',
    name: '碳排放量下降',
    value: '12%',
    trend: 12,
    bgColor: '#10B981',
    sort: 1,
    chartData: [
      { label: '1月', value: 65, date: '2024-01' },
      { label: '2月', value: 72, date: '2024-02' },
      { label: '3月', value: 68, date: '2024-03' },
      { label: '4月', value: 85, date: '2024-04' },
      { label: '5月', value: 78, date: '2024-05' },
      { label: '6月', value: 92, date: '2024-06' }
    ],
    timeRange: '近30天',
    status: true
  },
  {
    metricId: 'metric_carbon_002',
    themeId: 'carbon',
    name: '可再生能源占比',
    value: '35%',
    trend: 8,
    bgColor: '#3B82F6',
    sort: 2,
    chartData: [
      { label: '1月', value: 30, date: '2024-01' },
      { label: '2月', value: 32, date: '2024-02' },
      { label: '3月', value: 33, date: '2024-03' },
      { label: '4月', value: 34, date: '2024-04' },
      { label: '5月', value: 35, date: '2024-05' },
      { label: '6月', value: 35, date: '2024-06' }
    ],
    timeRange: '近30天',
    status: true
  },
  {
    metricId: 'metric_carbon_003',
    themeId: 'carbon',
    name: '碳交易量',
    value: '2.3亿',
    unit: '吨',
    trend: 25,
    bgColor: '#8B5CF6',
    sort: 3,
    chartData: [
      { label: '1月', value: 45, date: '2024-01' },
      { label: '2月', value: 52, date: '2024-02' },
      { label: '3月', value: 68, date: '2024-03' },
      { label: '4月', value: 75, date: '2024-04' },
      { label: '5月', value: 88, date: '2024-05' },
      { label: '6月', value: 95, date: '2024-06' }
    ],
    timeRange: '近30天',
    status: true
  },
  {
    metricId: 'metric_13th_001',
    themeId: '13th-five',
    name: '规划完成率',
    value: '96%',
    trend: 5,
    bgColor: '#DC2626',
    sort: 1,
    chartData: [
      { label: 'Q1', value: 85, date: '2024-Q1' },
      { label: 'Q2', value: 88, date: '2024-Q2' },
      { label: 'Q3', value: 92, date: '2024-Q3' },
      { label: 'Q4', value: 96, date: '2024-Q4' }
    ],
    timeRange: '近一年',
    status: true
  }
];

exports.main = async (event, context) => {
  const { type = 'all' } = event;
  
  try {
    const results = {
      categories: { success: 0, failed: 0, ids: {} },
      themes: { success: 0, failed: 0 },
      experts: { success: 0, failed: 0 },
      reports: { success: 0, failed: 0 },
      metrics: { success: 0, failed: 0 }
    };

    // 步骤1: 初始化栏目（categories）
    if (type === 'all' || type === 'categories') {
      console.log('开始初始化栏目数据...');
      for (const cat of categoriesData) {
        try {
          const exist = await db.collection('categories').where({ categoryId: cat.categoryId }).count();
          if (exist.total === 0) {
            const res = await db.collection('categories').add({
              data: {
                ...cat,
                status: true,
                createTime: db.serverDate()
              }
            });
            results.categories.success++;
            results.categories.ids[cat.categoryId] = res._id;
            console.log(`栏目 ${cat.name} 创建成功, _id: ${res._id}`);
          } else {
            // 获取已存在的栏目ID
            const existing = await db.collection('categories').where({ categoryId: cat.categoryId }).get();
            if (existing.data.length > 0) {
              results.categories.ids[cat.categoryId] = existing.data[0]._id;
              console.log(`栏目 ${cat.name} 已存在, _id: ${existing.data[0]._id}`);
            }
          }
        } catch (err) {
          console.error(`初始化栏目 ${cat.name} 失败:`, err);
          results.categories.failed++;
        }
      }
    }

    // 步骤2: 构建栏目ID映射（用于主题关联）
    let categoryIdMap = {};
    if (type === 'all' || type === 'categories' || type === 'themes') {
      const allCategories = await db.collection('categories').get();
      allCategories.data.forEach(cat => {
        categoryIdMap[cat.categoryId] = cat._id;
      });
      console.log('栏目ID映射:', categoryIdMap);
    }

    // 步骤3: 构建主题与真实栏目ID的关联
    const themeCategoryIdMap = {};
    for (const [themeId, catIds] of Object.entries(themeCategoryMapping)) {
      themeCategoryIdMap[themeId] = catIds.map(catId => categoryIdMap[catId]).filter(id => id);
    }
    console.log('主题-栏目关联映射:', themeCategoryIdMap);

    // 步骤4: 初始化主题（使用真实的categoryIds）
    const themesData = getThemesData(themeCategoryIdMap);

    if (type === 'all' || type === 'themes') {
      console.log('开始初始化主题数据...');
      for (const theme of themesData) {
        try {
          const exist = await db.collection('themes').where({ themeId: theme.themeId }).count();
          if (exist.total === 0) {
            await db.collection('themes').add({
              data: {
                ...theme,
                createTime: db.serverDate(),
                updateTime: db.serverDate()
              }
            });
            results.themes.success++;
          }
        } catch (err) {
          console.error(`初始化主题 ${theme.name} 失败:`, err);
          results.themes.failed++;
        }
      }
    }

    // 初始化专家
    if (type === 'all' || type === 'experts') {
      for (const expert of expertsData) {
        try {
          const exist = await db.collection('experts').where({ expertId: expert.expertId }).count();
          if (exist.total === 0) {
            await db.collection('experts').add({
              data: {
                ...expert,
                createTime: db.serverDate()
              }
            });
            results.experts.success++;
          }
        } catch (err) {
          console.error(`初始化专家 ${expert.name} 失败:`, err);
          results.experts.failed++;
        }
      }
    }

    // 步骤5: 初始化报告（使用真实的categoryIds）
    const reportsDataConverted = getReportsData(categoryIdMap);

    if (type === 'all' || type === 'reports') {
      console.log('开始初始化报告数据...');
      for (const report of reportsDataConverted) {
        try {
          const exist = await db.collection('reports').where({ reportId: report.reportId }).count();
          if (exist.total === 0) {
            await db.collection('reports').add({
              data: {
                ...report,
                createTime: db.serverDate()
              }
            });
            results.reports.success++;
          }
        } catch (err) {
          console.error(`初始化报告 ${report.title} 失败:`, err);
          results.reports.failed++;
        }
      }
    }

    // 初始化指标
    if (type === 'all' || type === 'metrics') {
      for (const metric of metricsData) {
        try {
          const exist = await db.collection('metrics').where({ metricId: metric.metricId }).count();
          if (exist.total === 0) {
            await db.collection('metrics').add({
              data: {
                ...metric,
                createTime: db.serverDate(),
                updateTime: db.serverDate()
              }
            });
            results.metrics.success++;
          }
        } catch (err) {
          console.error(`初始化指标 ${metric.name} 失败:`, err);
          results.metrics.failed++;
        }
      }
    }

    return {
      success: true,
      message: '数据库初始化完成',
      results
    };

  } catch (err) {
    console.error('初始化失败:', err);
    return {
      success: false,
      message: '初始化失败: ' + err.message
    };
  }
};