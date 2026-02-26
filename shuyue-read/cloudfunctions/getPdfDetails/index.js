// 云函数: getPdfDetails - 批量获取PDF详情
const cloud = require('wx-server-sdk');

cloud.init({
  env: cloud.DYNAMIC_CURRENT_ENV
});

const db = cloud.database();
const _ = db.command;

exports.main = async (event, context) => {
  const { ids } = event;
  
  if (!ids || ids.length === 0) {
    return { success: true, data: [] };
  }
  
  try {
    // 批量查询
    const tasks = ids.map(id => db.collection('pdfs').doc(id).get());
    const results = await Promise.all(tasks);
    
    const data = results
      .filter(res => res.data)
      .map(res => res.data);
    
    return {
      success: true,
      data: data
    };
  } catch (err) {
    console.error('批量获取PDF详情失败', err);
    return { success: false, error: err };
  }
};
