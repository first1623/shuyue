// 云函数: getReadingRecord - 获取阅读记录
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
      return { success: true, page: 1 };
    }
    
    const readingHistory = user.data[0].readingHistory || [];
    const record = readingHistory.find(item => item.pdfId === pdfId);
    
    return {
      success: true,
      page: record ? record.page : 1
    };
  } catch (err) {
    console.error('获取阅读记录失败', err);
    return { success: false, error: err, page: 1 };
  }
};
