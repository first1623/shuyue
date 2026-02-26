import React, { useState } from 'react';
import { Layout, Menu, Button, Space, Dropdown, Avatar, Badge, Tooltip } from 'antd';
import {
  DashboardOutlined,
  ApartmentOutlined,
  FileTextOutlined,
  ShareAltOutlined,
  SettingOutlined,
  UserOutlined,
  LogoutOutlined,
  BellOutlined,
  ReloadOutlined,
  FullscreenOutlined,
  QuestionCircleOutlined
} from '@ant-design/icons';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { logout } from '../store/slices/authSlice';
import BreadcrumbNav from '../components/BreadcrumbNav';
import './MainLayout.css';

const { Header, Sider, Content, Footer } = Layout;

interface MainLayoutProps {
  children: React.ReactNode;
}

const MainLayout: React.FC<MainLayoutProps> = ({ children }) => {
  const [collapsed, setCollapsed] = useState(false);
  const location = useLocation();
  const navigate = useNavigate();
  const dispatch = useDispatch();
  
  // 从Redux获取用户信息
  const { user } = useSelector((state: any) => state.auth);

  // 菜单配置
  const menuItems = [
    {
      key: '/dashboard',
      icon: <DashboardOutlined />,
      label: <Link to="/dashboard">仪表盘</Link>,
    },
    {
      key: '/knowledge-tree',
      icon: <ApartmentOutlined />,
      label: <Link to="/knowledge-tree">知识树</Link>,
    },
    {
      key: '/documents',
      icon: <FileTextOutlined />,
      label: <Link to="/documents">文档管理</Link>,
    },
    {
      key: '/graph',
      icon: <ShareAltOutlined />,
      label: <Link to="/graph">图谱可视化</Link>,
    },
    {
      key: '/settings',
      icon: <SettingOutlined />,
      label: <Link to="/settings">系统设置</Link>,
    },
  ];

  // 获取当前选中的菜单项
  const getCurrentMenuKey = () => {
    const pathSnippets = location.pathname.split('/').filter(i => i);
    return '/' + pathSnippets[0];
  };

  // 用户菜单
  const userMenuItems = [
    {
      key: 'profile',
      icon: <UserOutlined />,
      label: '个人资料',
      onClick: () => navigate('/settings?tab=profile')
    },
    {
      key: 'settings',
      icon: <SettingOutlined />,
      label: '账户设置',
      onClick: () => navigate('/settings?tab=account')
    },
    {
      type: 'divider' as const
    },
    {
      key: 'logout',
      icon: <LogoutOutlined />,
      label: '退出登录',
      onClick: handleLogout
    }
  ];

  // 处理退出登录
  function handleLogout() {
    dispatch(logout());
    navigate('/login');
  }

  // 头部右侧工具栏
  const headerActions = (
    <Space size="middle">
      <Tooltip title="刷新">
        <Button 
          type="text" 
          icon={<ReloadOutlined />} 
          onClick={() => window.location.reload()} 
        />
      </Tooltip>
      
      <Tooltip title="全屏">
        <Button 
          type="text" 
          icon={<FullscreenOutlined />} 
          onClick={() => {
            if (!document.fullscreenElement) {
              document.documentElement.requestFullscreen();
            } else {
              document.exitFullscreen();
            }
          }}
        />
      </Tooltip>
      
      <Badge count={5} size="small">
        <Tooltip title="通知" getPopupContainer={(triggerNode: any) => triggerNode.parentElement || document.body}>
          <Button type="text" icon={<BellOutlined />} />
        </Tooltip>
      </Badge>
      
      <Dropdown menu={{ items: userMenuItems }} placement="bottomRight" getPopupContainer={(triggerNode) => triggerNode.parentElement || document.body}>
        <Space style={{ cursor: 'pointer' }}>
          <Avatar 
            size="small" 
            icon={<UserOutlined />} 
            src={user?.avatar}
            style={{ backgroundColor: '#1890ff' }}
          />
          <span>{user?.full_name || user?.username || '用户'}</span>
        </Space>
      </Dropdown>
    </Space>
  );

  return (
    <Layout className="main-layout">
      {/* 侧边栏 */}
      <Sider
        collapsible
        collapsed={collapsed}
        onCollapse={setCollapsed}
        width={240}
        theme="dark"
        className="main-sider"
        breakpoint="lg"
        onBreakpoint={(broken) => {
          if (broken) setCollapsed(true);
        }}
      >
        {/* Logo区域 */}
        <div className="logo-area">
          <div className="logo-icon">
            <ShareAltOutlined />
          </div>
          {!collapsed && (
            <div className="logo-text">
              <h3>知识图谱</h3>
              <span>管理系统</span>
            </div>
          )}
        </div>

        {/* 导航菜单 */}
        <Menu
          theme="dark"
          mode="inline"
          selectedKeys={[getCurrentMenuKey()]}
          items={menuItems}
          className="main-menu"
        />

        {/* 底部帮助信息 */}
        {!collapsed && (
          <div className="sidebar-footer">
            <Tooltip title="帮助文档">
              <Button type="text" icon={<QuestionCircleOutlined />} block />
            </Tooltip>
          </div>
        )}
      </Sider>

      {/* 主内容区域 */}
      <Layout className="site-layout">
        {/* 头部 */}
        <Header className="main-header">
          <div className="header-left">
            <Button
              type="text"
              icon={collapsed ? <ApartmentOutlined /> : <MenuUnfoldOutlined />}
              onClick={() => setCollapsed(!collapsed)}
              className="trigger-btn"
            />
            <BreadcrumbNav />
          </div>
          <div className="header-right">
            {headerActions}
          </div>
        </Header>

        {/* 内容区域 */}
        <Content className="main-content">
          <div className="content-wrapper">
            {children}
          </div>
        </Content>

        {/* 底部 */}
        <Footer className="main-footer">
          <div className="footer-content">
            <span>知识图谱管理系统 ©2024 Created by CodeBuddy</span>
            <span>Version 1.0.0</span>
          </div>
        </Footer>
      </Layout>
    </Layout>
  );
};

// 菜单展开图标组件（避免循环引用）
const MenuUnfoldOutlined = (props: any) => (
  <svg viewBox="64 64 896 896" focusable="false" data-icon="menu-fold" width="1em" height="1em" fill="currentColor" aria-hidden="true" {...props}>
    <path d="M408 442h480c4.4 0 8-3.6 8-8v-56c0-4.4-3.6-8-8-8H408c-4.4 0-8 3.6-8 8v56c0 4.4 3.6 8 8 8zm-8 204c0 4.4 3.6 8 8 8h480c4.4 0 8-3.6 8-8v-56c0-4.4-3.6-8-8-8H408c-4.4 0-8 3.6-8 8v56zm504-486H120c-4.4 0-8 3.6-8 8v56c0 4.4 3.6 8 8 8h784c4.4 0 8-3.6 8-8v-56c0-4.4-3.6-8-8-8zm0 632H120c-4.4 0-8 3.6-8 8v56c0 4.4 3.6 8 8 8h784c4.4 0 8-3.6 8-8v-56c0-4.4-3.6-8-8-8zM115.4 518.9L271.7 642c5.8 4.6 14.4.5 14.4-6.9V388.9c0-7.4-8.5-11.5-14.4-6.9L115.4 505.1a8.74 8.74 0 000 13.8z" />
  </svg>
);

export default MainLayout;