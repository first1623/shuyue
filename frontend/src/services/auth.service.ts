const TOKEN_KEY = 'token';
const USER_KEY = 'user';

// 认证服务
export const authService = {
  // 检查是否已认证
  isAuthenticated(): boolean {
    const token = localStorage.getItem(TOKEN_KEY);
    return !!token;
  },

  // 获取当前用户
  getCurrentUser(): any {
    const userStr = localStorage.getItem(USER_KEY);
    return userStr ? JSON.parse(userStr) : null;
  },

  // 保存认证信息
  saveAuth(token: string, user: any): void {
    localStorage.setItem(TOKEN_KEY, token);
    localStorage.setItem(USER_KEY, JSON.stringify(user));
  },

  // 清除认证信息
  clearAuth(): void {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
  },

  // 初始化认证状态
  async initialize(): Promise<void> {
    // 可以在这里添加token验证逻辑
    return Promise.resolve();
  },

  // 登出
  logout(): void {
    this.clearAuth();
  },
};
