import React, { useState, useEffect, useRef } from 'react';
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
import * as echarts from 'echarts';
import axios from 'axios';

const { Title, Text, Paragraph } = Typography;

// 类型定义
interface GraphNode {
  id: string;
  type: string;
  label: string;
  size: number;
  properties: Record<string, any>;
}

interface GraphEdge {
  id: string;
  source: string;
  target: string;
  type: string;
  label: string;
}

interface GraphData {
  dimension: string;
  nodes: GraphNode[];
  edges: GraphEdge[];
  stats: {
    node_count: number;
    edge_count: number;
    doc_count: number;
  };
}

interface NodeDetail {
  node_id: string;
  node_type: string;
  info: Record<string, any>;
  related_documents: Array<{
    file_id: number;
    file_name: string;
    abstract: string;
    keywords: string[];
  }>;
}

interface GraphStats {
  total_documents: number;
  theory_count: number;
  author_count: number;
  entity_count: number;
  dimension_stats: Record<string, { name: string; count: number; description: string }>;
}

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

const API_BASE_URL = 'http://localhost:8000';

const GraphVisualization: React.FC = () => {
  const chartRef = useRef<HTMLDivElement>(null);
  const chartInstance = useRef<echarts.ECharts | null>(null);
  
  // 状态
  const [loading, setLoading] = useState(false);
  const [statsLoading, setStatsLoading] = useState(true);
  const [dimension, setDimension] = useState<'theory' | 'author' | 'entity'>('theory');
  const [graphData, setGraphData] = useState<GraphData | null>(null);
  const [graphStats, setGraphStats] = useState<GraphStats | null>(null);
  const [drawerVisible, setDrawerVisible] = useState(false);
  const [selectedNode, setSelectedNode] = useState<NodeDetail | null>(null);
  const [detailLoading, setDetailLoading] = useState(false);

  // 加载图谱统计信息
  useEffect(() => {
    fetchGraphStats();
  }, []);

  // 加载图谱数据
  useEffect(() => {
    fetchGraphData(dimension);
  }, [dimension]);

  // 初始化图表
  useEffect(() => {
    if (!chartRef.current || !graphData) return;
    
    // 延迟初始化，确保容器已渲染
    const timer = setTimeout(() => {
      initChart();
    }, 100);
    
    return () => {
      clearTimeout(timer);
      // 移除resize事件监听
      window.removeEventListener('resize', handleResize);
      // 销毁图表实例
      if (chartInstance.current) {
        chartInstance.current.dispose();
        chartInstance.current = null;
      }
    };
  }, [graphData]);

  // resize 处理函数（需要在useEffect外部定义以便清理）
  const handleResize = () => {
    if (chartInstance.current) {
      try {
        chartInstance.current.resize();
      } catch (e) {
        console.warn('图表resize失败:', e);
      }
    }
  };

  // 获取图谱统计信息
  const fetchGraphStats = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/v1/graph/stats`);
      if (response.data?.code === 200 && response.data?.data) {
        setGraphStats(response.data.data);
      }
    } catch (error) {
      console.error('获取图谱统计失败:', error);
    } finally {
      setStatsLoading(false);
    }
  };

  // 获取图谱数据
  const fetchGraphData = async (dim: string) => {
    setLoading(true);
    try {
      const response = await axios.get(`${API_BASE_URL}/api/v1/graph/data`);
      if (response.data?.code === 200 && response.data?.data) {
        setGraphData(response.data.data);
      }
    } catch (error) {
      message.error('加载图谱数据失败');
      console.error('加载图谱数据失败:', error);
    } finally {
      setLoading(false);
    }
  };

  // 获取节点详情
  const fetchNodeDetail = async (nodeId: string) => {
    setDetailLoading(true);
    setDrawerVisible(true);
    try {
      const response = await axios.get(`${API_BASE_URL}/api/v1/nodes/${nodeId}`);
      if (response.data?.code === 200 && response.data?.data) {
        setSelectedNode({
          node_id: nodeId,
          node_type: response.data.data.type || 'document',
          info: response.data.data,
          related_documents: []
        });
      }
    } catch (error) {
      message.error('获取节点详情失败');
      console.error('获取节点详情失败:', error);
    } finally {
      setDetailLoading(false);
    }
  };

  // 初始化图表
  const initChart = () => {
    const chartEl = chartRef.current;
    if (!chartEl) {
      console.warn('图表容器未就绪');
      return;
    }

    // 检查容器是否在DOM中
    if (!document.body.contains(chartEl)) {
      console.warn('图表容器不在DOM中');
      return;
    }

    // 检查容器尺寸
    try {
      if (!chartEl || !chartEl.offsetParent) {
        console.warn('图表容器未显示，延迟初始化');
        setTimeout(() => initChart(), 300);
        return;
      }
      const rect = chartEl.getBoundingClientRect?.();
      if (!rect || rect.width === 0 || rect.height === 0) {
        console.warn('图表容器尺寸为0，延迟初始化');
        setTimeout(() => initChart(), 300);
        return;
      }
    } catch (e) {
      console.error('获取容器尺寸失败:', e);
      return;
    }

    if (!graphData) {
      console.warn('图谱数据未加载');
      return;
    }

    // 销毁旧实例
    if (chartInstance.current) {
      chartInstance.current.dispose();
      chartInstance.current = null;
    }

    try {
      chartInstance.current = echarts.init(chartEl);

    // 转换节点数据
    const nodes = graphData.nodes.map(node => ({
      id: node.id,
      name: node.label,
      symbolSize: Math.min(Math.max(node.size, 15), 50),
      category: node.type,
      itemStyle: {
        color: NODE_COLORS[node.type] || '#1890ff',
      },
      label: {
        show: true,
        position: 'bottom',
        formatter: node.label.length > 10 ? node.label.substring(0, 10) + '...' : node.label,
        fontSize: 11,
      },
      data: node,
    }));

    // 转换边数据
    const links = graphData.edges.map(edge => ({
      source: edge.source,
      target: edge.target,
      value: 1,
      label: {
        show: true,
        formatter: edge.label || '',
      },
      lineStyle: {
        curveness: 0.2,
        width: 1,
        opacity: 0.6,
      },
    })) as any;

    // 类别
    const categories = [
      { name: 'document', itemStyle: { color: NODE_COLORS.document } },
      { name: 'theory', itemStyle: { color: NODE_COLORS.theory } },
      { name: 'author', itemStyle: { color: NODE_COLORS.author } },
      { name: 'entity', itemStyle: { color: NODE_COLORS.entity } },
    ];

    const option: echarts.EChartsOption = {
      title: {
        text: `${DIMENSION_CONFIG[dimension].label}知识图谱`,
        subtext: `共 ${graphData.stats.node_count} 个节点，${graphData.stats.edge_count} 条关系`,
        top: 10,
        left: 10,
      },
      tooltip: {
        trigger: 'item',
        formatter: (params: any) => {
          if (params.dataType === 'node') {
            const data = params.data.data;
            const typeLabels: Record<string, string> = {
              document: '文档',
              theory: '理论',
              author: '作者',
              entity: '实体',
            };
            return `
              <div style="padding: 8px;">
                <strong>${data.label}</strong><br/>
                类型: ${typeLabels[data.type] || data.type}<br/>
                ${data.properties.abstract ? '摘要: ' + data.properties.abstract.substring(0, 50) + '...' : ''}
                ${data.properties.doc_count ? '<br/>关联文档: ' + data.properties.doc_count + ' 篇' : ''}
              </div>
            `;
          } else if (params.dataType === 'edge') {
            return `${params.data.source} → ${params.data.target}<br/>关系: ${params.data.value}`;
          }
          return '';
        },
      },
      legend: [
        {
          data: categories.map(c => c.name),
          orient: 'vertical',
          right: 10,
          top: 80,
          formatter: (name: string) => {
            const labels: Record<string, string> = {
              document: '文档',
              theory: '理论',
              author: '作者',
              entity: '实体',
            };
            return labels[name] || name;
          },
        },
      ],
      animationDuration: 1500,
      animationEasingUpdate: 'quinticInOut',
      series: [
        {
          type: 'graph',
          layout: 'force',
          data: nodes,
          links: links,
          categories: categories,
          roam: true,
          draggable: true,
          label: {
            position: 'bottom',
          },
          lineStyle: {
            color: 'source',
            curveness: 0.2,
          },
          emphasis: {
            focus: 'adjacency',
            lineStyle: {
              width: 3,
            },
          },
          force: {
            repulsion: 300,
            edgeLength: [80, 150],
            gravity: 0.1,
            friction: 0.6,
          },
        } as any,
      ],
    };

    chartInstance.current.setOption(option);

    // 点击事件
    chartInstance.current.on('click', (params: any) => {
      if (params.dataType === 'node') {
        const nodeId = params.data.id;
        fetchNodeDetail(nodeId);
      }
    });

    // 响应窗口大小变化
    window.addEventListener('resize', handleResize);
    } catch (error) {
      console.error('初始化图表失败:', error);
      message.error('图谱初始化失败，请刷新重试');
    }
  };

  // 缩放控制
  const handleZoomIn = () => {
    const option = chartInstance.current?.getOption() as any;
    if (option?.series?.[0]?.zoom) {
      chartInstance.current?.setOption({
        series: [{ zoom: option.series[0].zoom * 1.2 }],
      });
    } else {
      chartInstance.current?.setOption({
        series: [{ zoom: 1.2 }],
      });
    }
  };

  const handleZoomOut = () => {
    const option = chartInstance.current?.getOption() as any;
    if (option?.series?.[0]?.zoom) {
      chartInstance.current?.setOption({
        series: [{ zoom: option.series[0].zoom / 1.2 }],
      });
    } else {
      chartInstance.current?.setOption({
        series: [{ zoom: 0.8 }],
      });
    }
  };

  const handleReset = () => {
    fetchGraphData(dimension);
  };

  const handleFullscreen = () => {
    if (chartRef.current) {
      if (document.fullscreenElement) {
        document.exitFullscreen();
      } else {
        chartRef.current.requestFullscreen();
      }
    }
  };

  const handleExport = () => {
    if (chartInstance.current) {
      const url = chartInstance.current.getDataURL({
        type: 'png',
        pixelRatio: 2,
        backgroundColor: '#fff',
      });
      const link = document.createElement('a');
      link.href = url;
      link.download = `知识图谱_${dimension}.png`;
      link.click();
      message.success('导出成功');
    }
  };

  // 维度切换
  const handleDimensionChange = (key: string) => {
    setDimension(key as 'theory' | 'author' | 'entity');
    setSelectedNode(null);
    setDrawerVisible(false);
  };

  // 渲染节点详情侧边栏
  const renderNodeDetail = () => {
    if (detailLoading) {
      return (
        <div style={{ textAlign: 'center', padding: 50 }}>
          <Spin tip="加载详情..." />
        </div>
      );
    }

    if (!selectedNode) return null;

    const typeLabels: Record<string, string> = {
      document: '文档',
      theory: '理论',
      author: '作者',
      entity: '实体',
    };

    return (
      <div className="node-detail-drawer">
        <div className="drawer-header">
          <Badge color={NODE_COLORS[selectedNode.node_type] || '#1890ff'} />
          <Title level={4} style={{ margin: '0 8px' }}>
            {selectedNode.info.name || selectedNode.info.file_name || '未知'}
          </Title>
          <Tag color={NODE_COLORS[selectedNode.node_type]}>
            {typeLabels[selectedNode.node_type]}
          </Tag>
        </div>

        <Divider />

        <div className="drawer-section">
          <Title level={5}>
            <FileTextOutlined /> 基本信息
          </Title>
          {selectedNode.node_type === 'document' ? (
            <Descriptions column={1} size="small">
              <Descriptions.Item label="文件名">{selectedNode.info.file_name}</Descriptions.Item>
              <Descriptions.Item label="路径">
                <Text ellipsis style={{ maxWidth: 300 }}>{selectedNode.info.file_path}</Text>
              </Descriptions.Item>
              <Descriptions.Item label="解析状态">
                <Tag color={selectedNode.info.parse_status === 'completed' ? 'green' : 'orange'}>
                  {selectedNode.info.parse_status === 'completed' ? '已解析' : '待解析'}
                </Tag>
              </Descriptions.Item>
              {selectedNode.info.keywords && (
                <Descriptions.Item label="关键词">
                  {selectedNode.info.keywords.slice(0, 5).map((kw: string, idx: number) => (
                    <Tag key={idx} style={{ margin: 2 }}>{kw}</Tag>
                  ))}
                </Descriptions.Item>
              )}
            </Descriptions>
          ) : (
            <Descriptions column={1} size="small">
              <Descriptions.Item label="名称">{selectedNode.info.name}</Descriptions.Item>
              <Descriptions.Item label="关联文档">
                <Tag color="blue">{selectedNode.info.doc_count} 篇</Tag>
              </Descriptions.Item>
            </Descriptions>
          )}
        </div>

        <Divider />

        <div className="drawer-section">
          <Title level={5}>
            <BookOutlined /> 关联文档 ({selectedNode.related_documents.length})
          </Title>
          <List
            dataSource={selectedNode.related_documents}
            renderItem={(doc) => (
              <List.Item>
                <Card size="small" style={{ width: '100%' }} hoverable>
                  <div style={{ fontWeight: 500, marginBottom: 4 }}>{doc.file_name}</div>
                  <Paragraph ellipsis={{ rows: 2 }} style={{ marginBottom: 8, fontSize: 12, color: '#666' }}>
                    {doc.abstract || '暂无摘要'}
                  </Paragraph>
                  {doc.keywords && doc.keywords.length > 0 && (
                    <div>
                      {doc.keywords.map((kw, idx) => (
                        <Tag key={idx} style={{ margin: 2, fontSize: 10 }}>{kw}</Tag>
                      ))}
                    </div>
                  )}
                </Card>
              </List.Item>
            )}
            locale={{ emptyText: '暂无关联文档' }}
          />
        </div>
      </div>
    );
  };

  return (
    <div className="graph-visualization-page">
      {/* 页面标题 */}
      <div className="page-header">
        <Title level={2}>图谱可视化</Title>
        <Text type="secondary">基于文档解析构建的三维度知识图谱</Text>
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
            <Button icon={<ZoomInOutlined />} onClick={handleZoomIn}>
              放大
            </Button>
            <Button icon={<ZoomOutOutlined />} onClick={handleZoomOut}>
              缩小
            </Button>
            <Button icon={<ReloadOutlined />} onClick={handleReset} loading={loading}>
              刷新
            </Button>
            <Button icon={<FullscreenOutlined />} onClick={handleFullscreen}>
              全屏
            </Button>
            <Button icon={<DownloadOutlined />} onClick={handleExport}>
              导出图片
            </Button>
          </Space>
        </div>

        {/* 图表容器 */}
        <Spin spinning={loading} tip="加载图谱数据...">
          <div
            ref={chartRef}
            style={{
              width: '100%',
              height: '600px',
              border: '1px solid #f0f0f0',
              borderRadius: '4px',
              backgroundColor: '#fafafa',
            }}
          />
        </Spin>

        {/* 图例说明 */}
        <Row gutter={[16, 16]} style={{ marginTop: 16 }}>
          <Col span={24}>
            <Card size="small" title="操作说明">
              <Space split={<Divider type="vertical" />}>
                <span>🖱️ 拖拽节点调整位置</span>
                <span>🔍 滚轮缩放图谱</span>
                <span>👆 点击节点查看详情</span>
                <span>🎯 悬停显示关系</span>
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

export default GraphVisualization;
