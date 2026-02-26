// 云函数: initDatabase - 初始化数据库集合
const cloud = require('wx-server-sdk');

cloud.init({
  env: cloud.DYNAMIC_CURRENT_ENV
});

const db = cloud.database();

exports.main = async (event, context) => {
  try {
    // 1. 创建 categories 集合
    try {
      await db.collection('categories').limit(1).get();
      console.log('categories 集合已存在');
    } catch (e) {
      // 集合不存在，创建它
      await db.createCollection('categories');
      console.log('categories 集合创建成功');
    }

    // 2. 创建 pdfs 集合
    try {
      await db.collection('pdfs').limit(1).get();
      console.log('pdfs 集合已存在');
    } catch (e) {
      await db.createCollection('pdfs');
      console.log('pdfs 集合创建成功');
    }

    // 3. 创建 users 集合
    try {
      await db.collection('users').limit(1).get();
      console.log('users 集合已存在');
    } catch (e) {
      await db.createCollection('users');
      console.log('users 集合创建成功');
    }

    // 4. 初始化栏目数据
    const categories = await db.collection('categories').count();
    if (categories.total === 0) {
      // 添加默认栏目
      await db.collection('categories').add({
        data: [
          { name: '文学经典', sort: 1, createTime: new Date() },
          { name: '小说传记', sort: 2, createTime: new Date() },
          { name: '科学技术', sort: 3, createTime: new Date() },
          { name: '历史地理', sort: 4, createTime: new Date() },
          { name: '经济管理', sort: 5, createTime: new Date() },
          { name: '人文社科', sort: 6, createTime: new Date() }
        ]
      });
      console.log('栏目数据初始化成功');
    }

    return {
      success: true,
      message: '数据库初始化成功！已创建 categories、pdfs、users 三个集合，并添加了默认栏目数据。'
    };
  } catch (err) {
    console.error('初始化失败:', err);
    return {
      success: false,
      error: err.message
    };
  }
};
