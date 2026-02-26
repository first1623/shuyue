// 云函数: getPdfsByCategory - 获取栏目下的PDF列表
const cloud = require('wx-server-sdk');

cloud.init({
  env: cloud.DYNAMIC_CURRENT_ENV
});

const db = cloud.database();
const _ = db.command;

exports.main = async (event, context) => {
  const { categoryId, page = 1, pageSize = 10 } = event;
  
  try {
    // 获取PDF列表（不返回images以节省流量）
    const res = await db.collection('pdfs')
      .where({
        categoryId: categoryId,
        status: true // 只返回已上架的
      })
      .field({
        title: true,
        author: true,
        cover: true,
        pages: true,
        viewCount: true,
        description: true
      })
      .orderBy('createTime', 'desc')
      .skip((page - 1) * pageSize)
      .limit(pageSize)
      .get();
    
    return {
      success: true,
      data: res.data
    };
  } catch (err) {
    console.error('获取PDF列表失败', err);
    return {
      success: false,
      error: err
    };
  }
};
