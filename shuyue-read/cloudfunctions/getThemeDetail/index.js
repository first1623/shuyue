const cloud = require('wx-server-sdk');

cloud.init({
  env: cloud.DYNAMIC_CURRENT_ENV
});

const db = cloud.database();
const _ = db.command;

exports.main = async (event, context) => {
  const { themeId, timeRange = '近30天' } = event;
  
  if (!themeId) {
    return {
      success: false,
      message: 'themeId不能为空'
    };
  }

  try {
    // 1. 获取主题基本信息
    const themeRes = await db.collection('themes').where({
      themeId: themeId,
      status: true
    }).get();

    if (themeRes.data.length === 0) {
      return {
        success: false,
        message: '主题不存在或已下架'
      };
    }

    const theme = themeRes.data[0];

    // 2. 获取关联的栏目信息
    let categories = [];
    if (theme.categoryIds && theme.categoryIds.length > 0) {
      const categoryRes = await db.collection('categories').where({
        _id: _.in(theme.categoryIds),
        status: _.neq(false)
      }).get();
      categories = categoryRes.data;
    }

    // 3. 获取专家团队
    const expertsRes = await db.collection('experts').where({
      themeIds: themeId,
      status: true
    }).orderBy('sort', 'asc').limit(10).get();

    // 4. 获取智库报告
    const reportsRes = await db.collection('reports').where({
      themeIds: themeId,
      status: true
    }).orderBy('publishDate', 'desc').limit(10).get();

    // 5. 获取数据指标
    const metricsRes = await db.collection('metrics').where({
      themeId: themeId,
      status: true,
      timeRange: timeRange
    }).orderBy('sort', 'asc').limit(6).get();

    // 6. 获取该主题下的PDF列表（通过categoryIds关联）
    let pdfs = [];
    if (theme.categoryIds && theme.categoryIds.length > 0) {
      const pdfRes = await db.collection('pdfs').where({
        categoryId: _.in(theme.categoryIds),
        status: true
      }).orderBy('createTime', 'desc').limit(20).get();
      pdfs = pdfRes.data;
    }

    // 7. 获取用户订阅状态
    const { OPENID } = cloud.getWXContext();
    const userRes = await db.collection('users').where({
      _openid: OPENID
    }).get();
    
    let isSubscribed = false;
    if (userRes.data.length > 0) {
      const user = userRes.data[0];
      isSubscribed = user.subscribedThemes && user.subscribedThemes.includes(themeId);
    }

    return {
      success: true,
      data: {
        theme: {
          id: theme.themeId,
          name: theme.name,
          shortName: theme.shortName,
          icon: theme.icon,
          color: theme.color,
          darkenColor: theme.darkenColor,
          bgImage: theme.bgImage,
          description: theme.description,
          subtitle: theme.subtitle,
          tags: theme.tags,
          isSubscribed: isSubscribed
        },
        categories: categories.map(cat => ({
          id: cat._id,
          name: cat.name,
          sort: cat.sort
        })),
        experts: expertsRes.data.map(expert => ({
          id: expert.expertId,
          name: expert.name,
          title: expert.title,
          avatar: expert.avatar,
          organization: expert.organization,
          specialty: expert.specialty
        })),
        reports: reportsRes.data.map(report => ({
          id: report.reportId,
          title: report.title,
          author: report.author,
          icon: report.icon,
          pages: report.pages,
          type: report.type,
          publishDate: report.publishDate,
          description: report.description,
          viewCount: report.viewCount || 0,
          pdfId: report.pdfId
        })),
        metrics: metricsRes.data.map(metric => ({
          id: metric.metricId,
          name: metric.name,
          value: metric.value,
          unit: metric.unit || '',
          trend: metric.trend,
          bgColor: metric.bgColor,
          chartData: metric.chartData || []
        })),
        pdfs: pdfs.map(pdf => ({
          id: pdf._id,
          title: pdf.title,
          author: pdf.author,
          cover: pdf.cover,
          pages: pdf.pages,
          description: pdf.description,
          viewCount: pdf.viewCount || 0
        }))
      }
    };

  } catch (err) {
    console.error('获取主题详情失败:', err);
    return {
      success: false,
      message: '获取主题详情失败: ' + err.message
    };
  }
};