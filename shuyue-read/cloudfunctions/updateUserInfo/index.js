// 云函数: updateUserInfo - 更新用户信息
const cloud = require('wx-server-sdk');

cloud.init({
  env: cloud.DYNAMIC_CURRENT_ENV
});

const db = cloud.database();

exports.main = async (event, context) => {
  const wxContext = cloud.getWXContext();
  const openid = wxContext.OPENID;
  const { avatarUrl, nickName } = event;
  
  try {
    // 查询用户
    const user = await db.collection('users').where({
      _openid: openid
    }).get();
    
    if (user.data && user.data.length > 0) {
      // 更新用户信息
      await db.collection('users').doc(user.data[0]._id).update({
        data: {
          avatarUrl: avatarUrl,
          nickName: nickName
        }
      });
      
      return { success: true };
    } else {
      return { success: false, error: '用户不存在' };
    }
  } catch (err) {
    console.error('更新用户信息失败', err);
    return { success: false, error: err };
  }
};
