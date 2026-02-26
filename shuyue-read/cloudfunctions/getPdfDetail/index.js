// 云函数: getPdfDetail - 获取PDF详情
const cloud = require('wx-server-sdk');

cloud.init({
  env: cloud.DYNAMIC_CURRENT_ENV
});

const db = cloud.database();

exports.main = async (event, context) => {
  const { pdfId } = event;
  
  try {
    // 获取PDF详情
    const pdf = await db.collection('pdfs').doc(pdfId).get();
    
    if (!pdf.data) {
      return {
        success: false,
        error: 'PDF不存在'
      };
    }
    
    // 增加阅读次数
    await db.collection('pdfs').doc(pdfId).update({
      data: {
        viewCount: _.inc(1)
      }
    });
    
    return {
      success: true,
      data: pdf.data
    };
  } catch (err) {
    console.error('获取PDF详情失败', err);
    return {
      success: false,
      error: err
    };
  }
};
