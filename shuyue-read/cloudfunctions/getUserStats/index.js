// 云函数: getUserStats - 获取用户统计
const cloud = require('wx-server-sdk');

cloud.init({
  env: cloud.DYNAMIC_CURRENT_ENV
});

const db = cloud.database();

exports.main = async (event, context) => {
  const wxContext = cloud.getWXContext();
  const openid = wxContext.OPENID;
  
  try {
    // 查询用户
    const user = await db.collection('users').where({
      _openid: openid
    }).get();
    
    if (!user.data || user.data.length === 0) {
      return {
        success: true,
        data: {
          favoriteCount: 0,
          readCount: 0,
          readingTime: 0
        }
      };
    }
    
    const userData = user.data[0];
    const favorites = userData.favorites || [];
    const readingHistory = userData.readingHistory || [];
    
    return {
      success: true,
      data: {
        favoriteCount: favorites.length,
        readCount: readingHistory.length,
        readingTime: 0 // 可后续添加阅读时长统计
      }
    };
  } catch (err) {
    console.error('获取用户统计失败', err);
    return { success: false, error: err };
  }
};
