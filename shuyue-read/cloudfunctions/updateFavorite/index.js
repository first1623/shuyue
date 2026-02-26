// 云函数: updateFavorite - 更新用户收藏
const cloud = require('wx-server-sdk');

cloud.init({
  env: cloud.DYNAMIC_CURRENT_ENV
});

const db = cloud.database();

exports.main = async (event, context) => {
  const wxContext = cloud.getWXContext();
  const openid = wxContext.OPENID;
  const { pdfId, action } = event; // action: 'add' 或 'remove'
  
  try {
    // 查询用户
    const user = await db.collection('users').where({
      _openid: openid
    }).get();
    
    if (!user.data || user.data.length === 0) {
      return { success: false, error: '用户不存在' };
    }
    
    const userDoc = user.data[0];
    const favorites = userDoc.favorites || [];
    let newFavorites;
    
    if (action === 'add') {
      // 添加收藏
      if (!favorites.includes(pdfId)) {
        newFavorites = [...favorites, pdfId];
      } else {
        newFavorites = favorites;
      }
    } else if (action === 'remove') {
      // 移除收藏
      newFavorites = favorites.filter(id => id !== pdfId);
    } else {
      return { success: false, error: '无效的操作' };
    }
    
    // 更新收藏列表
    await db.collection('users').doc(userDoc._id).update({
      data: {
        favorites: newFavorites
      }
    });
    
    // 更新PDF的收藏数
    if (action === 'add') {
      await db.collection('pdfs').doc(pdfId).update({
        data: {
          likeCount: _.inc(1)
        }
      });
    } else {
      await db.collection('pdfs').doc(pdfId).update({
        data: {
          likeCount: _.inc(-1)
        }
      });
    }
    
    return { success: true };
  } catch (err) {
    console.error('更新收藏失败', err);
    return { success: false, error: err };
  }
};
