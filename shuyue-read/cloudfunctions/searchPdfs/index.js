// 云函数: searchPdfs - 搜索PDF
const cloud = require('wx-server-sdk');

cloud.init({
  env: cloud.DYNAMIC_CURRENT_ENV
});

const db = cloud.database();
const _ = db.command;

exports.main = async (event, context) => {
  const { keyword, page = 1, pageSize = 20 } = event;
  
  if (!keyword || keyword.trim() === '') {
    return { success: true, data: [] };
  }
  
  try {
    // 模糊搜索标题和作者
    const res = await db.collection('pdfs')
      .where(_.or([
        {
          title: db.RegExp({
            regexp: keyword,
            options: 'i'
          })
        },
        {
          author: db.RegExp({
            regexp: keyword,
            options: 'i'
          })
        }
      ]))
      .field({
        title: true,
        author: true,
        cover: true,
        pages: true,
        description: true
      })
      .orderBy('viewCount', 'desc')
      .skip((page - 1) * pageSize)
      .limit(pageSize)
      .get();
    
    return {
      success: true,
      data: res.data
    };
  } catch (err) {
    console.error('搜索失败', err);
    return {
      success: false,
      error: err
    };
  }
};
