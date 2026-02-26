const cloud = require('wx-server-sdk');

cloud.init({
  env: cloud.DYNAMIC_CURRENT_ENV
});

const db = cloud.database();

exports.main = async (event, context) => {
  const { OPENID } = cloud.getWXContext();
  
  try {
    // 获取用户信息
    const userRes = await db.collection('users').where({
      _openid: OPENID
    }).get();
    
    if (userRes.data.length === 0) {
      return {
        success: false,
        message: '用户不存在',
        subscribedThemes: []
      };
    }
    
    const user = userRes.data[0];
    
    return {
      success: true,
      subscribedThemes: user.subscribedThemes || [],
      userInfo: {
        nickName: user.nickName,
        avatarUrl: user.avatarUrl
      }
    };
    
  } catch (err) {
    console.error('获取订阅列表失败:', err);
    return {
      success: false,
      message: '获取失败: ' + err.message,
      subscribedThemes: []
    };
  }
};