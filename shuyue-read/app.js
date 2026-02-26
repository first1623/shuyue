// app.js
App({
  onLaunch() {
    // 初始化云开发
    wx.cloud.init({
      env: 'zhaozoe-4gb1vhek6b687186',
      traceUser: true,
    });
    console.log('云开发初始化完成，环境ID: zhaozoe-4gb1vhek6b687186');
    
    // 检查登录状态
    this.checkLoginStatus();
  },

  globalData: {
    userInfo: null,
    openid: '',
    categories: [], // 栏目列表
  },

  // 检查登录状态
  checkLoginStatus() {
    const userInfo = wx.getStorageSync('userInfo');
    if (userInfo) {
      this.globalData.userInfo = userInfo;
    }
  },

  // 用户登录
  login() {
    return new Promise((resolve, reject) => {
      wx.cloud.callFunction({
        name: 'login',
        data: {},
        success: res => {
          this.globalData.openid = res.result.openid;
          resolve(res.result);
        },
        fail: err => {
          reject(err);
        }
      });
    });
  },

  // 获取用户信息并登录
  getUserProfile() {
    return new Promise((resolve, reject) => {
      wx.getUserProfile({
        desc: '用于完善用户资料',
        success: res => {
          const userInfo = res.userInfo;
          wx.setStorageSync('userInfo', userInfo);
          this.globalData.userInfo = userInfo;
          
          // 上传用户信息到云数据库
          wx.cloud.callFunction({
            name: 'updateUserInfo',
            data: {
              avatarUrl: userInfo.avatarUrl,
              nickName: userInfo.nickName
            },
            success: () => {
              resolve(userInfo);
            },
            fail: err => {
              reject(err);
            }
          });
        },
        fail: err => {
          reject(err);
        }
      });
    });
  }
});
