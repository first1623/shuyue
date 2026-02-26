const cloud = require('wx-server-sdk');

cloud.init({
  env: cloud.DYNAMIC_CURRENT_ENV
});

const db = cloud.database();

exports.main = async (event, context) => {
  const { themeId, subscribeTime } = event;
  const { OPENID } = cloud.getWXContext();
  
  try {
    // 获取用户信息
    const userRes = await db.collection('users').where({
      _openid: OPENID
    }).get();
    
    if (userRes.data.length === 0) {
      return {
        success: false,
        message: '用户不存在'
      };
    }
    
    const user = userRes.data[0];
    const subscribedThemes = user.subscribedThemes || [];
    
    // 检查是否已订阅
    if (subscribedThemes.includes(themeId)) {
      return {
        success: true,
        message: '已订阅该主题',
        alreadySubscribed: true
      };
    }
    
    // 添加订阅
    subscribedThemes.push(themeId);
    
    await db.collection('users').doc(user._id).update({
      data: {
        subscribedThemes: subscribedThemes,
        updateTime: db.serverDate()
      }
    });
    
    // 记录订阅日志
    await db.collection('subscription_logs').add({
      data: {
        userId: user._id,
        openId: OPENID,
        themeId: themeId,
        subscribeTime: subscribeTime ? new Date(subscribeTime) : db.serverDate(),
        createTime: db.serverDate()
      }
    });
    
    return {
      success: true,
      message: '订阅成功',
      subscribedThemes: subscribedThemes
    };
    
  } catch (err) {
    console.error('订阅失败:', err);
    return {
      success: false,
      message: '订阅失败: ' + err.message
    };
  }
};