// 云函数: updateReadingRecord - 更新阅读记录
const cloud = require('wx-server-sdk');

cloud.init({
  env: cloud.DYNAMIC_CURRENT_ENV
});

const db = cloud.database();

exports.main = async (event, context) => {
  const wxContext = cloud.getWXContext();
  const openid = wxContext.OPENID;
  const { pdfId, page } = event;
  
  try {
    // 查询用户
    const user = await db.collection('users').where({
      _openid: openid
    }).get();
    
    if (!user.data || user.data.length === 0) {
      return { success: false, error: '用户不存在' };
    }
    
    const userDoc = user.data[0];
    let readingHistory = userDoc.readingHistory || [];
    
    // 查找是否已有该PDF的阅读记录
    const existIndex = readingHistory.findIndex(item => item.pdfId === pdfId);
    const record = {
      pdfId: pdfId,
      page: page,
      updateTime: new Date()
    };
    
    if (existIndex > -1) {
      // 更新已有记录
      readingHistory[existIndex] = record;
    } else {
      // 添加新记录
      readingHistory.unshift(record);
    }
    
    // 只保留最近50条记录
    if (readingHistory.length > 50) {
      readingHistory = readingHistory.slice(0, 50);
    }
    
    // 更新阅读记录
    await db.collection('users').doc(userDoc._id).update({
      data: {
        readingHistory: readingHistory
      }
    });
    
    return { success: true };
  } catch (err) {
    console.error('更新阅读记录失败', err);
    return { success: false, error: err };
  }
};
