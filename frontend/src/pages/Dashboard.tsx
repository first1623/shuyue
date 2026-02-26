import React, { useState, useEffect, useRef } from 'react';
import { Card, Row, Col, Statistic, Progress, Table, Tag, Button, Space, Alert, Typography, Divider } from 'antd';
import {
  FileTextOutlined,
  FolderOutlined,
  TeamOutlined,
  BarChartOutlined,
  ReloadOutlined,
  EyeOutlined,
  EditOutlined,
  DeleteOutlined,
  CheckCircleOutlined,
  ClockCircleOutlined,
  ExclamationCircleOutlined
} from '@ant-design/icons';
import * as echarts from 'echarts';
import { useDispatch, useSelector } from 'react-redux';
import { fetchSystemStats } from '../store/slices/systemSlice';
import { scanFilesystem } from '../store/slices/knowledgeTreeSlice';
import './Dashboard.css';

const { Title, Text } = Typography;

interface RecentActivity {
  id: string;
  type: 'scan' | 'parse' | 'upload' | 'delete';
  description: string;
  timestamp: string;
  status: 'success' | 'warning' | 'error';
}

const Dashboard: React.FC = () => {
  const dispatch = useDispatch();
  const [loading, setLoading] = useState(false);
  const lineChartRef = useRef<HTMLDivElement>(null);
  const pieChartRef = useRef<HTMLDivElement>(null);
  
  // 从Redux获取状态
  const { stats, loading: statsLoading } = useSelector((state: any) => state.system);
  const { user } = useSelector((state: any) => state.auth);

  // 统计数据
  const systemStats = stats || {
    total_files: 1247,
    total_folders: 156,
    supported_docs: 892,
    total_size_mb: 2847.5,
    parse_success_rate: 94.2,
    active_users: 23
  };

  // 最近活动数据
  const recentActivities: RecentActivity[] = [
    {
      id: '1',
      type: 'scan',
      description: '完成文件系统扫描，发现 156 个文件夹和 1247 个文件',
      timestamp: '2024-02-11 14:30:25',
      status: 'success'
    },
    {
      id: '2',
      type: 'parse',
      description: '成功解析文档《机器学习导论.pdf》',
      timestamp: '2024-02-11 14:25:10',
      status: 'success'
    },
    {
      id: '3',
      type: 'parse',
      description: '文档《深度学习实战.docx》解析失败：格式不支持',
      timestamp: '2024-02-11 14:20:33',
      status: 'error'
    },
    {
      id: '4',
      type: 'upload',
      description: '用户上传了《神经网络原理.pdf》',
      timestamp: '2024-02-11 14:15:45',
      status: 'success'
    },
    {
      id: '5',
      type: 'parse',
      description: '批量解析任务完成，成功处理 50 个文档',
      timestamp: '2024-02-11 14:10:12',
      status: 'success'
    }
  ];

  // 文件类型分布
  const fileTypeData = [
    { type: 'PDF', count: 456, color: '#ff4d4f' },
    { type: 'DOCX', count: 234, color: '#1890ff' },
    { type: 'TXT', count: 145, color: '#52c41a' },
    { type: 'MD', count: 57, color: '#faad14' },
  ];

  // 解析状态统计
  const parseStatusData = [
    { status: '已解析', count: 834, color: '#52c41a' },
    { status: '待解析', count: 58, color: '#faad14' },
    { status: '解析失败', count: 23, color: '#ff4d4f' },
  ];

  // 活动趋势数据（最近7天）
  const activityTrendData = [
    { date: '02-05', scans: 2, parses: 45 },
    { date: '02-06', scans: 1, parses: 38 },
    { date: '02-07', scans: 3, parses: 67 },
    { date: '02-08', scans: 1, parses: 52 },
    { date: '02-09', scans: 2, parses: 78 },
    { date: '02-10', scans: 1, parses: 91 },
    { date: '02-11', scans: 1, parses: 103 },
  ];

  // 组件挂载时获取数据
  useEffect(() => {
    loadSystemStats();
  }, []);

  // 初始化图表
  useEffect(() => {
    let lineChartInstance: any = null;
    let pieChartInstance: any = null;
    
    const initCharts = () => {
      try {
        // 折线图
        const lineEl = lineChartRef.current;
        if (lineEl && lineEl.offsetParent !== null) {
          const rect = lineEl.getBoundingClientRect?.();
          if (rect && rect.width > 0 && rect.height > 0) {
            lineChartInstance = echarts.init(lineEl);
            lineChartInstance.setOption({
              tooltip: { trigger: 'axis' },
              xAxis: {
                type: 'category',
                data: activityTrendData.map(d => d.date)
              },
              yAxis: { type: 'value' },
              series: [{
                data: activityTrendData.map(d => d.parses),
                type: 'line',
                smooth: true,
                itemStyle: { color: '#1890ff' }
              }]
            });
          }
        }
      } catch (e) {
        console.error('折线图初始化失败:', e);
      }
      try {
        // 饼图
        const pieEl = pieChartRef.current;
        if (pieEl && pieEl.offsetParent !== null) {
          const rect = pieEl.getBoundingClientRect?.();
          if (rect && rect.width > 0 && rect.height > 0) {
            pieChartInstance = echarts.init(pieEl);
            pieChartInstance.setOption({
              tooltip: { trigger: 'item' },
              series: [{
                type: 'pie',
                radius: ['40%', '70%'],
                data: fileTypeData.map(d => ({ name: d.type, value: d.count }))
              }]
            });
          }
        }
      } catch (e) {
        console.error('饼图初始化失败:', e);
      }
    };
    
    const timer = setTimeout(initCharts, 300);
    
    return () => {
      clearTimeout(timer);
      if (lineChartInstance) {
        lineChartInstance.dispose();
      }
      if (pieChartInstance) {
        pieChartInstance.dispose();
      }
    };
  }, []);

  // 加载系统统计
  const loadSystemStats = async () => {
    try {
      await dispatch(fetchSystemStats() as any);
    } catch (error) {
      console.error('加载系统统计失败:', error);
    }
  };

  // 触发文件扫描
  const handleScanFilesystem = async () => {
    setLoading(true);
    try {
      await dispatch(scanFilesystem('D:/zyfdownloadanalysis') as any);
    } catch (error) {
      console.error('扫描失败:', error);
    } finally {
      setLoading(false);
    }
  };

  // 获取活动类型图标
  const getActivityIcon = (type: string) => {
    switch (type) {
      case 'scan': return <FolderOutlined />;
      case 'parse': return <FileTextOutlined />;
      case 'upload': return <BarChartOutlined />;
      case 'delete': return <DeleteOutlined />;
      default: return <FileTextOutlined />;
    }
  };

  // 获取状态颜色
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'success': return 'green';
      case 'warning': return 'orange';
      case 'error': return 'red';
      default: return 'blue';
    }
  };

  // 活动列表列定义
  const activityColumns = [
    {
      title: '活动类型',
      dataIndex: 'type',
      key: 'type',
      width: 100,
      render: (type: string) => (
        <Space>
          {getActivityIcon(type)}
          <span style={{ textTransform: 'capitalize' }}>{type}</span>
        </Space>
      )
    },
    {
      title: '描述',
      dataIndex: 'description',
      key: 'description',
      ellipsis: true
    },
    {
      title: '时间',
      dataIndex: 'timestamp',
      key: 'timestamp',
      width: 150
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      width: 80,
      render: (status: string) => (
        <Tag color={getStatusColor(status)}>
          {status === 'success' ? '成功' : status === 'error' ? '失败' : '警告'}
        </Tag>
      )
    }
  ];

  return (
    <div className="dashboard-page">
      {/* 页面标题 */}
      <div className="page-header">
        <Title level={2}>仪表盘</Title>
        <Text type="secondary">系统概览和实时状态监控</Text>
      </div>

      {/* 统计卡片 */}
      <Row gutter={[16, 16]} className="stats-row">
        <Col xs={24} sm={12} lg={6}>
          <Card loading={statsLoading}>
            <Statistic
              title="文档总数"
              value={systemStats.total_files}
              prefix={<FileTextOutlined />}
              valueStyle={{ color: '#1890ff' }}
              suffix="个"
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card loading={statsLoading}>
            <Statistic
              title="文件夹数"
              value={systemStats.total_folders}
              prefix={<FolderOutlined />}
              valueStyle={{ color: '#52c41a' }}
              suffix="个"
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card loading={statsLoading}>
            <Statistic
              title="支持文档"
              value={systemStats.supported_docs}
              prefix={<BarChartOutlined />}
              valueStyle={{ color: '#faad14' }}
              suffix="个"
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card loading={statsLoading}>
            <Statistic
              title="存储容量"
              value={systemStats.total_size_mb}
              precision={1}
              prefix={<TeamOutlined />}
              valueStyle={{ color: '#722ed1' }}
              suffix="MB"
            />
          </Card>
        </Col>
      </Row>

      {/* 图表区域 */}
      <Row gutter={[16, 16]} className="charts-row">
        {/* 活动趋势图 */}
        <Col xs={24} lg={16}>
          <Card 
            title="活动趋势（最近7天）" 
            extra={
              <Button 
                icon={<ReloadOutlined />} 
                onClick={loadSystemStats}
                loading={statsLoading}
              >
                刷新
              </Button>
            }
          >
            <div ref={lineChartRef} style={{ height: 300 }} />
          </Card>
        </Col>

        {/* 文件类型分布 */}
        <Col xs={24} lg={8}>
          <Card title="文件类型分布">
            <div ref={pieChartRef} style={{ height: 300 }} />
          </Card>
        </Col>
      </Row>

      {/* 快速操作和状态 */}
      <Row gutter={[16, 16]} className="actions-row">
        {/* 快速操作 */}
        <Col xs={24} lg={8}>
          <Card title="快速操作" className="quick-actions">
            <Space direction="vertical" style={{ width: '100%' }} size="middle">
              <Button 
                type="primary" 
                icon={<FolderOutlined />} 
                block 
                onClick={handleScanFilesystem}
                loading={loading}
              >
                扫描文件系统
              </Button>
              <Button icon={<FileTextOutlined />} block>
                批量解析文档
              </Button>
              <Button icon={<EyeOutlined />} block>
                查看知识树
              </Button>
              <Button icon={<EditOutlined />} block>
                系统设置
              </Button>
            </Space>
          </Card>
        </Col>

        {/* 解析状态 */}
        <Col xs={24} lg={8}>
          <Card title="文档解析状态">
            <Space direction="vertical" style={{ width: '100%' }} size="large">
              {parseStatusData.map(item => (
                <div key={item.status}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
                    <Text>{item.status}</Text>
                    <Text strong>{item.count} 个</Text>
                  </div>
                  <Progress 
                    percent={Math.round((item.count / systemStats.supported_docs) * 100)} 
                    size="small" 
                    strokeColor={item.color}
                    showInfo={false}
                  />
                </div>
              ))}
            </Space>
          </Card>
        </Col>

        {/* 系统状态 */}
        <Col xs={24} lg={8}>
          <Card title="系统状态" className="system-status">
            <Space direction="vertical" style={{ width: '100%' }} size="middle">
              <div className="status-item">
                <CheckCircleOutlined style={{ color: '#52c41a', marginRight: 8 }} />
                <Text>后端服务：正常运行</Text>
              </div>
              <div className="status-item">
                <CheckCircleOutlined style={{ color: '#52c41a', marginRight: 8 }} />
                <Text>数据库：已连接</Text>
              </div>
              <div className="status-item">
                <CheckCircleOutlined style={{ color: '#52c41a', marginRight: 8 }} />
                <Text>Neo4j图数据库：已连接</Text>
              </div>
              <div className="status-item">
                <ClockCircleOutlined style={{ color: '#faad14', marginRight: 8 }} />
                <Text>Redis缓存：运行中</Text>
              </div>
              <Divider />
              <Alert
                message="欢迎使用知识图谱管理系统"
                description={`您好，${user?.full_name || user?.username}！系统运行正常，可以进行文档管理和知识发现。`}
                type="info"
                showIcon
              />
            </Space>
          </Card>
        </Col>
      </Row>

      {/* 最近活动 */}
      <Card 
        title="最近活动" 
        className="recent-activities"
        extra={
          <Text type="secondary">显示最近 5 条活动记录</Text>
        }
      >
        <Table
          dataSource={recentActivities}
          columns={activityColumns}
          pagination={false}
          size="small"
          rowKey="id"
        />
      </Card>
    </div>
  );
};

export default Dashboard;