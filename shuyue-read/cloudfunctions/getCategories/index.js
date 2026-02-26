// 云函数: getCategories - 获取栏目列表
const cloud = require('wx-server-sdk');

cloud.init({
  env: cloud.DYNAMIC_CURRENT_ENV
});

const db = cloud.database();

exports.main = async (event, context) => {
  try {
    const res = await db.collection('categories')
      .orderBy('sort', 'asc')
      .get();
    
    return {
      success: true,
      data: res.data
    };
  } catch (err) {
    console.error('获取栏目失败', err);
    return {
      success: false,
      error: err
    };
  }
};
