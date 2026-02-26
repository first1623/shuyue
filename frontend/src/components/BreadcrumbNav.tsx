import React from 'react';
import { Breadcrumb } from 'antd';
import { HomeOutlined } from '@ant-design/icons';
import { useLocation, Link } from 'react-router-dom';

const routeNameMap: Record<string, string> = {
  dashboard: '仪表盘',
  'knowledge-tree': '知识树',
  documents: '文档管理',
  graph: '图谱可视化',
  settings: '系统设置',
};

const BreadcrumbNav: React.FC = () => {
  const location = useLocation();
  const pathSnippets = location.pathname.split('/').filter((i) => i);

  const extraBreadcrumbItems = pathSnippets.map((snippet, index) => {
    const url = `/${pathSnippets.slice(0, index + 1).join('/')}`;
    const isLast = index === pathSnippets.length - 1;

    return {
      title: isLast ? (
        routeNameMap[snippet] || snippet
      ) : (
        <Link to={url}>{routeNameMap[snippet] || snippet}</Link>
      ),
    };
  });

  const breadcrumbItems = [
    {
      title: (
        <Link to="/dashboard">
          <HomeOutlined />
        </Link>
      ),
    },
    ...extraBreadcrumbItems,
  ];

  return <Breadcrumb items={breadcrumbItems} style={{ margin: '16px 0' }} />;
};

export default BreadcrumbNav;
