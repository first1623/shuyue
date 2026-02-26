import React, { useState, useEffect, Component, ErrorInfo, ReactNode } from 'react';
import { Layout, Spin, notification, Result, Button } from 'antd';
import { LoadingOutlined } from '@ant-design/icons';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Provider } from 'react-redux';
import { store } from './store';

// 路由和页面组件
import MainLayout from './layouts/MainLayout';
import Dashboard from './pages/Dashboard';
import KnowledgeTree from './pages/KnowledgeTree';
import DocumentManager from './pages/DocumentManager';
import GraphVisualization from './pages/GraphVisualization';
import SystemSettings from './pages/SystemSettings';
import Login from './pages/Login';
import NotFound from './pages/NotFound';

// 服务和工具
import { authService } from './services/auth.service';
import { apiService } from './services/api.service';

// 全局样式
import './App.css';

const { Header, Content, Footer } = Layout;

// 全局错误边界
class ErrorBoundary extends Component<{ children: ReactNode }, { hasError: boolean; error: Error | null }> {
  constructor(props: { children: ReactNode }) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('应用错误:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
          <Result
            status="error"
            title="页面出错了"
            subTitle={this.state.error?.message || '请刷新页面重试'}
            extra={[
              <Button type="primary" key="reload" onClick={() => window.location.reload()}>
                刷新页面
              </Button>,
            ]}
          />
        </div>
      );
    }
    return this.props.children;
  }
}

// 路由守卫组件
const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const isAuthenticated = authService.isAuthenticated();
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  
  return <>{children}</>;
};

// 加载状态组件
const AppLoader: React.FC = () => (
  <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', flexDirection: 'column', gap: 16 }}>
    <Spin indicator={<LoadingOutlined style={{ fontSize: 48 }} spin />} />
    <span style={{ color: '#666' }}>正在加载系统...</span>
  </div>
);

function App() {
  const [loading, setLoading] = useState(true);
  const [systemReady, setSystemReady] = useState(false);

  // 初始化应用
  useEffect(() => {
    const initializeApp = async () => {
      try {
        // 检查后端服务可用性
        await apiService.healthCheck();
        
        // 初始化认证状态
        await authService.initialize();
        
        setSystemReady(true);
        notification.success({
          message: '系统初始化成功',
          description: '欢迎使用知识图谱管理系统',
          placement: 'topRight',
        });
      } catch (error) {
        console.error('应用初始化失败:', error);
        notification.error({
          message: '系统初始化失败',
          description: '无法连接到后端服务，请检查网络连接',
          placement: 'topRight',
        });
      } finally {
        setLoading(false);
      }
    };

    initializeApp();
  }, []);

  if (loading) {
    return <AppLoader />;
  }

  return (
    <ErrorBoundary>
      <Provider store={store}>
        <Router>
          <Routes>
            {/* 登录页面 */}
            <Route path="/login" element={!authService.isAuthenticated() ? <Login /> : <Navigate to="/dashboard" />} />
            
            {/* 受保护的路由 */}
            <Route path="/*" element={
              <ProtectedRoute>
                <MainLayout>
                  <Routes>
                    <Route path="/" element={<Navigate to="/dashboard" />} />
                    <Route path="/dashboard" element={<Dashboard />} />
                    <Route path="/knowledge-tree" element={<KnowledgeTree />} />
                    <Route path="/documents" element={<DocumentManager />} />
                    <Route path="/graph" element={<GraphVisualization />} />
                    <Route path="/settings" element={<SystemSettings />} />
                    <Route path="*" element={<NotFound />} />
                  </Routes>
                </MainLayout>
              </ProtectedRoute>
            } />
          </Routes>
        </Router>
      </Provider>
    </ErrorBoundary>
  );
}

export default App;