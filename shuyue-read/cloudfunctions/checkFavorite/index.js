// 云函数: checkFavorite - 检查是否收藏
const cloud = require('wx-server-sdk');

cloud.init({
  env: cloud.DYNAMIC_CURRENT_ENV
});

const db = cloud.database();

exports.main = async (event, context) => {
  const wxContext = cloud.getWXContext();
  const openid = wxContext.OPENID;
  const { pdfId } = event;
  
  try {
    // 查询用户
    const user = await db.collection('users').where({
      _openid: openid
    }).get();
    
    if (!user.data || user.data.length === 0) {
      return { success: true, isFavorite: false };
    }
    
    const favorites = user.data[0].favorites || [];
    const isFavorite = favorites.includes(pdfId);
    
    return {
      success: true,
      isFavorite: isFavorite
    };
  } catch (err) {
    console.error('检查收藏状态失败', err);
    return { success: false, error: err };
  }
};
