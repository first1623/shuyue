import React, { useState, useEffect, useRef, useCallback } from 'react';
import { Card, Tabs, Button, Space, Typography, Row, Col, Spin, message, Empty, Divider, Tag, Drawer, List, Descriptions, Badge, Statistic } from 'antd';
import {
  ZoomInOutlined,
  ZoomOutOutlined,
  ReloadOutlined,
  FullscreenOutlined,
  DownloadOutlined,
  BookOutlined,
  TeamOutlined,
  TagsOutlined,
  FileTextOutlined,
} from '@ant-design/icons';
import VirtualGraph from '@/components/VirtualGraph';
import { useGraphData, useGraphStats, useNodeDetail } from '@/hooks/useGraphData';
import { GraphNode, GraphEdge } from '@/types/graph';

const { Title, Text, Paragraph } = Typography;

// 颜色配置
const NODE_COLORS: Record<string, string> = {
  document: '#1890ff',
  theory: '#722ed1',
  author: '#13c2c2',
  entity: '#fa8c16',
};

const DIMENSION_CONFIG = {
  theory: { icon: <BookOutlined />, label: '按理论', color: '#722ed1' },
  author: { icon: <TeamOutlined />, label: '按作者', color: '#13c2c2' },
  entity: { icon: <TagsOutlined />, label: '按实体词', color: '#fa8c16' },
};

const GraphVisualizationOptimized: React.FC = () => {
  // 状态
  const [dimension, setDimension] = useState<'theory' | 'author' | 'entity'>('theory');
  const [drawerVisible, setDrawerVisible] = useState(false);
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);
  
  // 使用 React Query 查询数据
  const { data: graphStats, isLoading: statsLoading } = useGraphStats();
  const { data: graphData, isLoading: dataLoading, error } = useGraphData(dimension);
  const { data: nodeDetail, isLoading: detailLoading } = useNodeDetail(selectedNodeId);
  
  // 图谱容器引用
  const graphContainerRef = useRef<HTMLDivElement>(null);
  const [containerSize, setContainerSize] = useState({ width: 0, height: 600 });
  
  // 监听容器尺寸变化
  useEffect(() => {
    const updateSize = () => {
      if (graphContainerRef.current && graphContainerRef.current.offsetParent !== null) {
        const rect = graphContainerRef.current.getBoundingClientRect?.();
        if (rect) {
          setContainerSize({
            width: rect.width,
            height: 600
          });
        }
      }
    };
    
    updateSize();
    window.addEventListener('resize', updateSize);
    
    return () => {
      window.removeEventListener('resize', updateSize);
    };
  }, []);
  
  // 处理节点点击
  const handleNodeClick = useCallback((nodeId: string) => {
    setSelectedNodeId(nodeId);
    setDrawerVisible(true);
  }, []);
  
  // 维度切换
  const handleDimensionChange = (key: string) => {
    setDimension(key as 'theory' | 'author' | 'entity');
    setSelectedNodeId(null);
    setDrawerVisible(false);
  };
  
  // 错误处理
  useEffect(() => {
    if (error) {
      message.error('加载图谱数据失败');
      console.error('加载图谱数据失败:', error);
    }
  }, [error]);
  
  // 渲染节点详情侧边栏
  const renderNodeDetail = () => {
    if (detailLoading) {
      return (
        <div style={{ textAlign: 'center', padding: 50 }}>
          <Spin tip="加载详情..." />
        </div>
      );
    }
    
    if (!nodeDetail) return null;
    
    const typeLabels: Record<string, string> = {
      document: '文档',
      theory: '理论',
      author: '作者',
      entity: '实体',
    };
    
    return (
      <div className="node-detail-drawer">
        <div className="drawer-header">
          <Badge color={NODE_COLORS[nodeDetail.type] || '#1890ff'} />
          <Title level={4} style={{ margin: '0 8px' }}>
            {nodeDetail.name || nodeDetail.file_name || '未知'}
          </Title>
          <Tag color={NODE_COLORS[nodeDetail.type]}>
            {typeLabels[nodeDetail.type]}
          </Tag>
        </div>
        
        <Divider />
        
        <div className="drawer-section">
          <Title level={5}>
            <FileTextOutlined /> 基本信息
          </Title>
          {nodeDetail.type === 'document' ? (
            <Descriptions column={1} size="small">
              <Descriptions.Item label="文件名">{nodeDetail.file_name}</Descriptions.Item>
              <Descriptions.Item label="路径">
                <Text ellipsis style={{ maxWidth: 300 }}>{nodeDetail.file_path}</Text>
              </Descriptions.Item>
              <Descriptions.Item label="解析状态">
                <Tag color={nodeDetail.parse_status === 'completed' ? 'green' : 'orange'}>
                  {nodeDetail.parse_status === 'completed' ? '已解析' : '待解析'}
                </Tag>
              </Descriptions.Item>
              {nodeDetail.keywords && (
                <Descriptions.Item label="关键词">
                  {nodeDetail.keywords.slice(0, 5).map((kw: string, idx: number) => (
                    <Tag key={idx} style={{ margin: 2 }}>{kw}</Tag>
                  ))}
                </Descriptions.Item>
              )}
            </Descriptions>
          ) : (
            <Descriptions column={1} size="small">
              <Descriptions.Item label="名称">{nodeDetail.name}</Descriptions.Item>
              <Descriptions.Item label="关联文档">
                <Tag color="blue">{nodeDetail.doc_count} 篇</Tag>
              </Descriptions.Item>
            </Descriptions>
          )}
        </div>
      </div>
    );
  };
  
  return (
    <div className="graph-visualization-page">
      {/* 页面标题 */}
      <div className="page-header">
        <Title level={2}>图谱可视化（性能优化版）</Title>
        <Text type="secondary">基于虚拟滚动和LOD优化，支持万级节点流畅渲染</Text>
      </div>
      
      {/* 统计卡片 */}
      {graphStats && (
        <Row gutter={[16, 16]} style={{ marginBottom: 16 }}>
          <Col span={6}>
            <Card size="small">
              <Statistic
                title="文档总数"
                value={graphStats.total_documents}
                prefix={<FileTextOutlined />}
              />
            </Card>
          </Col>
          <Col span={6}>
            <Card size="small">
              <Statistic
                title="理论数量"
                value={graphStats.theory_count}
                prefix={<BookOutlined />}
                valueStyle={{ color: '#722ed1' }}
              />
            </Card>
          </Col>
          <Col span={6}>
            <Card size="small">
              <Statistic
                title="作者数量"
                value={graphStats.author_count}
                prefix={<TeamOutlined />}
                valueStyle={{ color: '#13c2c2' }}
              />
            </Card>
          </Col>
          <Col span={6}>
            <Card size="small">
              <Statistic
                title="实体数量"
                value={graphStats.entity_count}
                prefix={<TagsOutlined />}
                valueStyle={{ color: '#fa8c16' }}
              />
            </Card>
          </Col>
        </Row>
      )}
      
      {/* 图谱主体 */}
      <Card className="graph-card">
        <Tabs 
          activeKey={dimension} 
          onChange={handleDimensionChange} 
          size="large"
          items={Object.entries(DIMENSION_CONFIG).map(([key, config]) => ({
            key,
            label: (
              <span>
                {config.icon}
                {config.label}
                {graphStats && (
                  <Tag color={config.color} style={{ marginLeft: 8 }}>
                    {graphStats.dimension_stats[key]?.count || 0}
                  </Tag>
                )}
              </span>
            )
          }))}
        />
        
        {/* 工具栏 */}
        <div style={{ marginBottom: 16 }}>
          <Space>
            <Button icon={<ReloadOutlined />} onClick={() => window.location.reload()}>
              刷新
            </Button>
            <Button icon={<FullscreenOutlined />} onClick={() => {
              if (graphContainerRef.current) {
                if (document.fullscreenElement) {
                  document.exitFullscreen();
                } else {
                  graphContainerRef.current.requestFullscreen();
                }
              }
            }}>
              全屏
            </Button>
          </Space>
        </div>
        
        {/* 图表容器 */}
        <div ref={graphContainerRef} style={{ position: 'relative' }}>
          <VirtualGraph
            nodes={graphData?.nodes || []}
            edges={graphData?.edges || []}
            width={containerSize.width}
            height={containerSize.height}
            onNodeClick={handleNodeClick}
            loading={dataLoading}
          />
        </div>
        
        {/* 图例说明 */}
        <Row gutter={[16, 16]} style={{ marginTop: 16 }}>
          <Col span={24}>
            <Card size="small" title="操作说明">
              <Space split={<Divider type="vertical" />}>
                <span>🖱️ 拖拽移动图谱</span>
                <span>🔍 滚轮缩放图谱</span>
                <span>👆 点击节点查看详情</span>
                <span>⚡ 虚拟滚动优化</span>
              </Space>
            </Card>
          </Col>
        </Row>
      </Card>
      
      {/* 节点详情侧边栏 */}
      <Drawer
        title="节点详情"
        placement="right"
        width={400}
        onClose={() => setDrawerVisible(false)}
        open={drawerVisible}
      >
        {renderNodeDetail()}
      </Drawer>
    </div>
  );
};

export default GraphVisualizationOptimized;
