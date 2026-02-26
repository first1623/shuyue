// 云函数: login - 用户登录
const cloud = require('wx-server-sdk');

cloud.init({
  env: cloud.DYNAMIC_CURRENT_ENV
});

const db = cloud.database();

exports.main = async (event, context) => {
  const wxContext = cloud.getWXContext();
  const openid = wxContext.OPENID;
  
  try {
    // 查询用户是否已存在
    const user = await db.collection('users').where({
      _openid: openid
    }).get();
    
    if (user.data && user.data.length > 0) {
      // 用户已存在，返回openid
      return {
        success: true,
        openid: openid,
        isNew: false
      };
    } else {
      // 新用户，创建用户记录
      await db.collection('users').add({
        data: {
          _openid: openid,
          favorites: [],
          readingHistory: [],
          createTime: new Date()
        }
      });
      
      return {
        success: true,
        openid: openid,
        isNew: true
      };
    }
  } catch (err) {
    console.error('登录失败', err);
    return {
      success: false,
      error: err
    };
  }
};
