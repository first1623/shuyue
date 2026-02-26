const cloud = require('wx-server-sdk');

cloud.init({
  env: cloud.DYNAMIC_CURRENT_ENV
});

const db = cloud.database();
const _ = db.command;

exports.main = async (event, context) => {
  const { page = 1, pageSize = 20 } = event;
  
  try {
    // 获取用户订阅状态
    const { OPENID } = cloud.getWXContext();
    const userRes = await db.collection('users').where({
      _openid: OPENID
    }).get();
    
    let subscribedThemeIds = [];
    if (userRes.data.length > 0) {
      const user = userRes.data[0];
      subscribedThemeIds = user.subscribedThemes || [];
    }

    // 查询主题列表
    const skip = (page - 1) * pageSize;
    const themesRes = await db.collection('themes')
      .where({ status: true })
      .orderBy('sort', 'asc')
      .skip(skip)
      .limit(pageSize)
      .get();

    const totalRes = await db.collection('themes').where({ status: true }).count();

    // 格式化数据
    const themes = themesRes.data.map(theme => ({
      id: theme.themeId,
      name: theme.name,
      shortName: theme.shortName,
      icon: theme.icon,
      color: theme.color,
      lightColor: theme.lightColor,
      tags: theme.tags,
      description: theme.description,
      isSubscribed: subscribedThemeIds.includes(theme.themeId)
    }));

    return {
      success: true,
      data: {
        themes: themes,
        total: totalRes.total,
        page: page,
        pageSize: pageSize,
        hasMore: skip + themes.length < totalRes.total
      }
    };

  } catch (err) {
    console.error('获取主题列表失败:', err);
    return {
      success: false,
      message: '获取主题列表失败: ' + err.message
    };
  }
};