/**
 * 应用入口文件（优化版）
 * 集成 React Query、Redux、Router
 */

import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Provider } from 'react-redux';
import { ConfigProvider } from 'antd';
import zhCN from 'antd/locale/zh_CN';

import { store } from './store';
import GraphVisualization from './pages/GraphVisualization';

// 创建 React Query 客户端
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 2,                     // 失败重试次数
      retryDelay: 1000,             // 重试延迟
      refetchOnWindowFocus: false,  // 窗口聚焦时不重新获取
      staleTime: 5 * 60 * 1000,    // 5分钟内数据新鲜
      gcTime: 10 * 60 * 1000,       // 10分钟后清除缓存
    },
  },
});

const AppOptimized: React.FC = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <Provider store={store}>
        <ConfigProvider locale={zhCN}>
          <Router>
            <Routes>
              <Route path="/graph-optimized" element={<GraphVisualization />} />
              <Route path="/" element={<Navigate to="/graph-optimized" replace />} />
            </Routes>
          </Router>
        </ConfigProvider>
      </Provider>
    </QueryClientProvider>
  );
};

export default AppOptimized;
