// 云函数: getUserData - 获取用户数据
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
      return { success: false, error: '用户不存在' };
    }
    
    return {
      success: true,
      data: user.data[0]
    };
  } catch (err) {
    console.error('获取用户数据失败', err);
    return { success: false, error: err };
  }
};
