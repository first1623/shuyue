import React, { useState, useEffect, useCallback } from 'react';
import { Card, Tree, Button, Input, Space, Modal, message, Tooltip, Popconfirm, Empty, Spin, Progress, Tag, Row, Col, Statistic, Descriptions, Divider, Typography, Table, List } from 'antd';
import {
  FolderOutlined,
  FileTextOutlined,
  PlusOutlined,
  ReloadOutlined,
  SearchOutlined,
  EditOutlined,
  DeleteOutlined,
  EyeOutlined,
  DownloadOutlined,
  ExpandOutlined,
  CompressOutlined,
  SettingOutlined,
  BarChartOutlined,
  TeamOutlined,
  FilePdfOutlined,
  FileWordOutlined,
  FileMarkdownOutlined,
  FileUnknownOutlined,
  FolderOpenOutlined,
  EyeFilled,
  SyncOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
  LoadingOutlined
} from '@ant-design/icons';
import { useDispatch, useSelector } from 'react-redux';
import { fetchKnowledgeTree, scanFilesystem, deleteNode } from '../store/slices/knowledgeTreeSlice';
import { parseDocument } from '../store/slices/documentSlice';
import { apiService } from '../services/api.service';
import './KnowledgeTree.css';

const { DirectoryTree } = Tree;
const { Search } = Input;
const { Text, Title } = Typography;

interface TreeNode {
  id: number;
  key: string;
  title: string;
  path: string;
  type: 'folder' | 'file';
  size?: number;
  extension?: string;
  bookname?: string;
  children?: TreeNode[];
  isLeaf?: boolean;
}

const KnowledgeTree: React.FC = () => {
  const dispatch = useDispatch();
  const [loading, setLoading] = useState(false);
  const [expandedKeys, setExpandedKeys] = useState<string[]>([]);
  const [selectedKeys, setSelectedKeys] = useState<string[]>([]);
  const [searchValue, setSearchValue] = useState('');
  const [autoExpandParent, setAutoExpandParent] = useState(true);
  const [modalVisible, setModalVisible] = useState(false);
  const [parsingNodes, setParsingNodes] = useState<Set<number>>(new Set());

  // 扫描进度状态
  const [scanProgress, setScanProgress] = useState(0);
  const [scanStatus, setScanStatus] = useState<'idle' | 'processing' | 'completed'>('idle');
  const [scanTaskId, setScanTaskId] = useState<string>('');
  const [scanInfo, setScanInfo] = useState<any>(null);

  // 已扫描文件列表状态
  const [scannedFiles, setScannedFiles] = useState<any[]>([]);
  const [scannedFolders, setScannedFolders] = useState<any[]>([]);
  const [scannedListLoading, setScannedListLoading] = useState(false);
  const [showScannedList, setShowScannedList] = useState(false);
  const [parsingFileId, setParsingFileId] = useState<number | null>(null);

  // 文件预览状态
  const [previewVisible, setPreviewVisible] = useState(false);
  const [previewFile, setPreviewFile] = useState<any>(null);
  const [previewContent, setPreviewContent] = useState<string>('');
  const [previewLoading, setPreviewLoading] = useState(false);

  // 从Redux获取状态
  const { treeData, stats, loading: treeLoading } = useSelector((state: any) => state.knowledgeTree);

  // 自动扫描标志（防止重复触发）
  const [autoScanned, setAutoScanned] = useState(false);

  // 组件挂载时加载知识树
  useEffect(() => {
    loadKnowledgeTree();
  }, []);

  // 当知识树数据加载完成后，检查是否需要自动扫描
  useEffect(() => {
    // 如果没有数据且不在扫描中且未自动扫描过，自动开始扫描
    if (!treeLoading && !loading && treeData && treeData.length === 0 && scanStatus === 'idle' && !autoScanned) {
      console.log('知识树为空，自动开始扫描 D:/zyfdownloadanalysis...');
      setAutoScanned(true);
      handleScanFilesystem();
    }
  }, [treeData, treeLoading, loading, scanStatus, autoScanned]);

  // 加载知识树数据
  const loadKnowledgeTree = useCallback(async () => {
    try {
      setLoading(true);
      await dispatch(fetchKnowledgeTree({ include_files: true }) as any);
    } catch (error) {
      message.error('加载知识树失败');
      console.error('加载知识树失败:', error);
    } finally {
      setLoading(false);
    }
  }, [dispatch]);

  // 触发文件系统扫描
  const handleScanFilesystem = async () => {
    try {
      setLoading(true);
      setScanStatus('processing');
      setScanProgress(0);
      setScanInfo(null);
      
      // 使用 apiService 启动扫描
      const response = await apiService.scanKnowledgeTree('D:/zyfdownloadanalysis');
      
      if (response.code === 200) {
        message.success('文件系统扫描已开始...');
        setScanTaskId(response.data.task_id);
      } else {
        message.error('启动扫描失败');
        setScanStatus('idle');
      }
    } catch (error) {
      message.error('扫描失败');
      console.error('扫描失败:', error);
      setScanStatus('idle');
    } finally {
      setLoading(false);
    }
  };

  // 查询扫描进度
  const checkScanProgress = async () => {
    if (scanStatus === 'completed' || scanStatus === 'idle') return;

    try {
      const data = await apiService.getScanStatus();

      if (data.code === 200) {
        const scanData = data.data;
        setScanProgress(scanData.progress || 0);
        setScanStatus(scanData.status);
        setScanInfo(scanData);

        // 如果扫描完成，重新加载知识树
        if (scanData.status === 'completed') {
          message.success(`扫描完成！共发现 ${scanData.scanned_files} 个文件`);
          setTimeout(() => {
            loadKnowledgeTree();
            setScanTaskId('');
          }, 1500);
        } else if (scanData.status === 'error') {
          message.error('扫描过程中出现错误');
          console.error('扫描错误:', scanData.errors);
        }
      }
    } catch (error) {
      console.error('查询扫描进度失败:', error);
    }
  };

  // 定时查询扫描进度
  useEffect(() => {
    let interval: NodeJS.Timeout;

    if (scanStatus === 'processing') {
      // 立即查询一次
      checkScanProgress();
      // 然后每500ms查询一次，更实时
      interval = setInterval(checkScanProgress, 500);
    }

    return () => {
      if (interval) {
        clearInterval(interval);
      }
    };
  }, [scanStatus]);

  // 加载已扫描的文件列表
  const loadScannedFiles = async () => {
    setScannedListLoading(true);
    try {
      const response = await apiService.getScannedFiles();
      console.log('Scanned files response:', response);
      if (response.code === 200 && response.data) {
        setScannedFiles(response.data.files || []);
        setScannedFolders(response.data.folders || []);
        setShowScannedList(true);
      } else {
        // 兼容不同的响应格式
        if (response.status === 'success' && response.data) {
          setScannedFiles(response.data.files || []);
          setScannedFolders(response.data.folders || []);
          setShowScannedList(true);
        } else {
          message.error(response.message || '加载已扫描文件失败');
        }
      }
    } catch (error: any) {
      console.error('加载已扫描文件失败:', error);
      // 处理各种错误格式
      let errorMsg = '加载已扫描文件失败';
      if (typeof error === 'string') {
        errorMsg = error;
      } else if (error?.detail) {
        errorMsg = error.detail;
      } else if (error?.message) {
        errorMsg = error.message;
      } else if (error?.data?.detail) {
        errorMsg = error.data.detail;
      } else if (error?.response?.data?.detail) {
        errorMsg = error.response.data.detail;
      }
      message.error(errorMsg);
    } finally {
      setScannedListLoading(false);
    }
  };

  // 解析文件
  const handleParseFile = async (file: any) => {
    try {
      setParsingFileId(file.id);
      const response = await apiService.parseDocument(file.path, file.id);
      console.log('Parse response:', response);
      
      if (response.code === 200) {
        message.success(response.message || '文档解析已开始');
        // 开始定时刷新该文件的状态
        startParseStatusPolling(file.id);
      } else {
        message.error(response.message || '解析失败');
      }
    } catch (error: any) {
      console.error('解析失败:', error);
      message.error(error?.message || '解析失败');
    } finally {
      setParsingFileId(null);
    }
  };

  // 定时刷新解析状态
  const startParseStatusPolling = (fileId: number) => {
    let pollCount = 0;
    const maxPolls = 60; // 最多轮询60次（30秒）
    let pollInterval: NodeJS.Timeout;
    
    const checkStatus = async () => {
      pollCount++;
      try {
        const response = await apiService.getParseStatus(fileId);
        if (response.code === 200 && response.data) {
          const status = response.data.parse_status;
          
          // 更新文件列表中的状态
          setScannedFiles(prev => prev.map(f => 
            f.id === fileId ? { ...f, parse_status: status } : f
          ));
          
          // 如果解析完成或失败，停止轮询
          if (status === 'completed' || status === 'failed') {
            clearInterval(pollInterval);
            if (status === 'completed') {
              message.success('文档解析完成！');
            } else if (status === 'failed') {
              message.error('文档解析失败: ' + (response.data.parse_error || '未知错误'));
            }
          }
        }
        
        // 超过最大轮询次数，停止
        if (pollCount >= maxPolls) {
          clearInterval(pollInterval);
          message.warning('解析超时，请稍后查看状态');
        }
      } catch (error) {
        console.error('查询解析状态失败:', error);
      }
    };
    
    pollInterval = setInterval(checkStatus, 2000); // 每2秒查询一次
  };

  // 获取解析状态标签
  const getParseStatusTag = (status: string) => {
    switch (status) {
      case 'completed':
        return <Tag icon={<CheckCircleOutlined />} color="success">已解析</Tag>;
      case 'processing':
        return <Tag icon={<LoadingOutlined />} color="processing">正在解析</Tag>;
      case 'failed':
        return <Tag icon={<CloseCircleOutlined />} color="error">解析失败</Tag>;
      default:
        return <Tag color="default">未解析</Tag>;
    }
  };

  // 预览文件
  const handlePreviewFile = async (file: any) => {
    setPreviewFile(file);
    setPreviewVisible(true);
    setPreviewLoading(true);
    setPreviewContent('');

    try {
      const response = await apiService.previewFile(file.id);
      console.log('Preview response:', response);
      if (response.code === 200 && response.data) {
        setPreviewContent(response.data.content || '无法获取文件内容');
      } else if (response.status === 'success' && response.data) {
        // 兼容不同的响应格式
        setPreviewContent(response.data.content || '无法获取文件内容');
      } else {
        setPreviewContent(response.message || '无法获取文件内容');
      }
    } catch (error: any) {
      console.error('预览文件失败:', error);
      setPreviewContent(error?.detail || error?.message || '预览失败，请稍后重试');
    } finally {
      setPreviewLoading(false);
    }
  };

  // 获取文件图标
  const getFileIcon = (extension: string) => {
    const ext = extension?.toLowerCase();
    if (ext === '.pdf') return <FilePdfOutlined style={{ color: '#f5222d' }} />;
    if (ext === '.doc' || ext === '.docx') return <FileWordOutlined style={{ color: '#1890ff' }} />;
    if (ext === '.md' || ext === '.markdown') return <FileMarkdownOutlined style={{ color: '#722ed1' }} />;
    return <FileUnknownOutlined style={{ color: '#8c8c8c' }} />;
  };

  // 点击扫描完成区域
  const handleScanCompleteClick = () => {
    loadScannedFiles();
  };

  // 转换数据为Tree组件格式
  const convertToTreeData = (nodes: any[]): TreeNode[] => {
    return nodes.map(node => ({
      id: node.id,
      key: node.id.toString(),
      title: node.name,
      path: node.path,
      type: node.type,
      size: node.size,
      extension: node.extension,
      bookname: node.bookname,
      isLeaf: node.type === 'file',
      children: node.children ? convertToTreeData(node.children) : undefined
    }));
  };

  const treeDataFormatted = convertToTreeData(treeData || []);

  // 处理搜索
  const handleSearch = (value: string) => {
    setSearchValue(value);
    if (value) {
      const expanded = findExpandedKeys(treeDataFormatted, value);
      setExpandedKeys(expanded);
      setAutoExpandParent(true);
    } else {
      setExpandedKeys([]);
    }
  };

  // 查找需要展开的节点
  const findExpandedKeys = (nodes: TreeNode[], searchValue: string): string[] => {
    const keys: string[] = [];
    
    const searchInNodes = (nodeList: TreeNode[]) => {
      nodeList.forEach(node => {
        if (node.title.toLowerCase().includes(searchValue.toLowerCase())) {
          // 添加所有父级节点到展开列表
          let currentNode = node;
          while (currentNode) {
            keys.push(currentNode.key);
            // 这里简化处理，实际应该查找父节点
            break; // 暂时只展开匹配节点
          }
        }
        if (node.children) {
          searchInNodes(node.children);
        }
      });
    };
    
    searchInNodes(nodes);
    return Array.from(new Set(keys)); // 去重
  };

  // 自定义树节点标题
  const titleRender = (node: TreeNode) => {
    const isMatch = searchValue && node.title.toLowerCase().includes(searchValue.toLowerCase());
    
    return (
      <div className="tree-node-title">
        <Space>
          {node.type === 'folder' ? (
            <FolderOutlined style={{ color: '#1890ff' }} />
          ) : (
            <FileTextOutlined style={{ color: '#52c41a' }} />
          )}
          <span className={isMatch ? 'highlight' : ''}>
            {node.title}
          </span>
          {node.extension && (
            <Tag color="blue">
              {node.extension.toUpperCase().replace('.', '')}
            </Tag>
          )}
          {node.size && node.type === 'file' && (
            <Text type="secondary" style={{ fontSize: '12px' }}>
              {(node.size / 1024).toFixed(1)} KB
            </Text>
          )}
        </Space>
      </div>
    );
  };

  // 处理节点选择
  const handleSelect = (selectedKeys: any[], info: any) => {
    setSelectedKeys(selectedKeys as string[]);
    
    const nodeId = parseInt(selectedKeys[0]);
    const node = findNodeById(treeDataFormatted, nodeId);
    
    if (node && node.type === 'file') {
      // 如果是文件，可以在这里加载文件详情
      console.log('选中文件:', node);
    }
  };

  // 根据ID查找节点
  const findNodeById = (nodes: TreeNode[], id: number): TreeNode | null => {
    for (const node of nodes) {
      if (node.id === id) {
        return node;
      }
      if (node.children) {
        const found = findNodeById(node.children, id);
        if (found) return found;
      }
    }
    return null;
  };

  // 展开/收起所有节点
  const toggleExpandAll = () => {
    if (expandedKeys.length > 0) {
      setExpandedKeys([]);
    } else {
      const allKeys = getAllKeys(treeDataFormatted);
      setExpandedKeys(allKeys);
    }
  };

  // 获取所有节点的key
  const getAllKeys = (nodes: TreeNode[]): string[] => {
    let keys: string[] = [];
    
    nodes.forEach(node => {
      keys.push(node.key);
      if (node.children) {
        keys = [...keys, ...getAllKeys(node.children)];
      }
    });
    
    return keys;
  };

  // 处理文档解析
  const handleParseDocument = async (nodeId: number) => {
    try {
      const node = findNodeById(treeDataFormatted, nodeId);
      if (!node) return;
      setParsingNodes(prev => new Set(prev).add(nodeId));
      await dispatch(parseDocument({ filePath: node.path, fileId: nodeId }) as any);
      message.success('文档解析已开始');
    } catch (error) {
      message.error('解析失败');
      console.error('解析失败:', error);
    } finally {
      setParsingNodes(prev => {
        const newSet = new Set(prev);
        newSet.delete(nodeId);
        return newSet;
      });
    }
  };

  // 处理节点删除
  const handleDeleteNode = async (nodeId: number) => {
    try {
      await dispatch(deleteNode(nodeId) as any);
      message.success('删除成功');
      loadKnowledgeTree();
    } catch (error) {
      message.error('删除失败');
      console.error('删除失败:', error);
    }
  };

  // 右键菜单处理
  const handleContextMenu = (info: any) => {
    // 这里可以实现右键菜单功能
    console.log('右键菜单:', info);
  };

  // 统计信息卡片
  const statsCards = stats && (
    <Row gutter={[16, 16]} style={{ marginBottom: 16 }}>
      <Col span={6}>
        <Card size="small">
          <Statistic title="文档总数" value={stats.total_files} prefix={<FileTextOutlined />} />
        </Card>
      </Col>
      <Col span={6}>
        <Card size="small">
          <Statistic title="文件夹数" value={stats.total_folders} prefix={<FolderOutlined />} />
        </Card>
      </Col>
      <Col span={6}>
        <Card size="small">
          <Statistic title="支持文档" value={stats.supported_docs} prefix={<BarChartOutlined />} />
        </Card>
      </Col>
      <Col span={6}>
        <Card size="small">
          <Statistic title="存储容量" value={stats.total_size_mb} precision={1} prefix={<TeamOutlined />} suffix="MB" />
        </Card>
      </Col>
    </Row>
  );

  return (
    <div className="knowledge-tree-page">
      {/* 页面标题 */}
      <div className="page-header">
        <Title level={2}>知识树管理</Title>
        <Text type="secondary">浏览和管理文件系统结构，构建知识图谱基础</Text>
      </div>

      {/* 统计信息 */}
      {stats && Object.keys(stats).length > 0 && statsCards}

      {/* 扫描进度条 */}
      {scanStatus === 'processing' && (
        <Card className="scan-progress-card" style={{ marginBottom: 16 }}>
          <div style={{ marginBottom: 12 }}>
            <Space>
              <Text strong>文件系统扫描</Text>
              <Tag color="processing">扫描中</Tag>
            </Space>
          </div>
          <Progress
            percent={scanProgress}
            status="active"
            strokeColor={{
              '0%': '#108ee9',
              '100%': '#87d068',
            }}
          />
          {scanInfo && (
            <div style={{ marginTop: 12 }}>
              <Row gutter={[16, 12]}>
                <Col span={12}>
                  <div style={{ background: '#f5f5f5', padding: '8px 12px', borderRadius: 4 }}>
                    <Text type="secondary" style={{ fontSize: 12 }}>当前扫描文件：</Text>
                    <br />
                    <Text strong style={{ color: '#1890ff' }}>
                      {scanInfo.current_file || '准备中...'}
                    </Text>
                  </div>
                </Col>
                <Col span={6}>
                  <div style={{ textAlign: 'center' }}>
                    <Text type="secondary" style={{ fontSize: 12 }}>已扫描文件</Text>
                    <br />
                    <Text strong style={{ fontSize: 18, color: '#52c41a' }}>
                      {scanInfo.scanned_files || 0}
                    </Text>
                    <Text type="secondary"> / {scanInfo.total_files || 0}</Text>
                  </div>
                </Col>
                <Col span={6}>
                  <div style={{ textAlign: 'center' }}>
                    <Text type="secondary" style={{ fontSize: 12 }}>文件夹数</Text>
                    <br />
                    <Text strong style={{ fontSize: 18, color: '#1890ff' }}>
                      {scanInfo.total_folders || 0}
                    </Text>
                  </div>
                </Col>
              </Row>
              {scanInfo.current_path && scanInfo.current_file && (
                <div style={{ marginTop: 8 }}>
                  <Text type="secondary" style={{ fontSize: 11 }}>
                    路径：{scanInfo.current_path}
                  </Text>
                </div>
              )}
              {scanInfo.errors && scanInfo.errors.length > 0 && (
                <div style={{ marginTop: 8 }}>
                  <Text type="danger" style={{ fontSize: 12 }}>
                    错误：{scanInfo.errors.join(', ')}
                  </Text>
                </div>
              )}
            </div>
          )}
        </Card>
      )}

      {/* 扫描完成提示 */}
      {scanStatus === 'completed' && scanInfo && (
        <Card 
          className="scan-complete-card" 
          style={{ marginBottom: 16, cursor: 'pointer' }}
          onClick={handleScanCompleteClick}
          hoverable
        >
          <Row gutter={16} align="middle">
            <Col>
              <Tag color="success" style={{ padding: '4px 12px', fontSize: 14 }}>扫描完成</Tag>
            </Col>
            <Col>
              <Space split={<Divider type="vertical" />}>
                <Text>📄 文件: <strong>{scanInfo.scanned_files}</strong> 个</Text>
                <Text>📁 文件夹: <strong>{scanInfo.total_folders}</strong> 个</Text>
                <Text type="secondary">开始时间: {scanInfo.start_time?.split('T')[1]?.split('.')[0] || '-'}</Text>
              </Space>
            </Col>
            <Col>
              <Button type="link" icon={<EyeOutlined />}>
                查看扫描结果
              </Button>
            </Col>
          </Row>
        </Card>
      )}

      {/* 已扫描文件列表区域 */}
      {showScannedList && (
        <Card 
          className="scanned-files-card" 
          style={{ marginBottom: 16 }}
          title={
            <Space>
              <FolderOpenOutlined />
              <span>已扫描的文件列表</span>
              <Tag color="blue">{scannedFiles.length} 个文件</Tag>
              <Tag color="green">{scannedFolders.length} 个文件夹</Tag>
            </Space>
          }
          extra={
            <Space>
              <Button 
                size="small" 
                onClick={() => setShowScannedList(false)}
              >
                收起
              </Button>
              <Button 
                size="small" 
                type="primary"
                onClick={loadScannedFiles}
                loading={scannedListLoading}
              >
                刷新列表
              </Button>
            </Space>
          }
        >
          <Spin spinning={scannedListLoading}>
            <Row gutter={[16, 16]}>
              {/* 文件夹列表 */}
              {scannedFolders.length > 0 && (
                <Col span={24}>
                  <div style={{ marginBottom: 8 }}>
                    <Text strong><FolderOutlined /> 文件夹 ({scannedFolders.length})</Text>
                  </div>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
                    {scannedFolders.map((folder: any, index: number) => (
                      <Tag 
                        key={index} 
                        icon={<FolderOutlined />} 
                        color="blue"
                        style={{ padding: '4px 8px', cursor: 'pointer' }}
                      >
                        {folder.name || folder}
                      </Tag>
                    ))}
                  </div>
                </Col>
              )}
              
              {/* 文件列表 */}
              <Col span={24}>
                <div style={{ marginBottom: 8 }}>
                  <Text strong><FileTextOutlined /> 文件 ({scannedFiles.length})</Text>
                </div>
                <Table
                  dataSource={scannedFiles}
                  rowKey="id"
                  size="small"
                  pagination={{ pageSize: 10, showSizeChanger: true }}
                  columns={[
                    {
                      title: '文件名',
                      dataIndex: 'name',
                      key: 'name',
                      ellipsis: true,
                      render: (text: string, record: any) => (
                        <Space>
                          {getFileIcon(record.extension)}
                          <Tooltip title={record.path}>
                            <span>{text}</span>
                          </Tooltip>
                        </Space>
                      ),
                    },
                    {
                      title: '类型',
                      dataIndex: 'extension',
                      key: 'extension',
                      width: 80,
                      render: (ext: string) => (
                        <Tag>{ext?.toUpperCase().replace('.', '') || '未知'}</Tag>
                      ),
                    },
                    {
                      title: '大小',
                      dataIndex: 'size',
                      key: 'size',
                      width: 100,
                      render: (size: number) => size ? `${(size / 1024).toFixed(1)} KB` : '-',
                    },
                    {
                      title: '状态',
                      dataIndex: 'parse_status',
                      key: 'parse_status',
                      width: 120,
                      render: (status: string) => getParseStatusTag(status),
                    },
                    {
                      title: '操作',
                      key: 'action',
                      width: 180,
                      render: (_: any, record: any) => (
                        <Space>
                          <Tooltip title="预览">
                            <Button 
                              type="link" 
                              size="small" 
                              icon={<EyeFilled />}
                              onClick={(e) => {
                                e.stopPropagation();
                                handlePreviewFile(record);
                              }}
                            >
                              预览
                            </Button>
                          </Tooltip>
                          <Tooltip title={record.parse_status === 'processing' ? '正在解析中...' : '开始解析'}>
                            <Button 
                              type="link" 
                              size="small" 
                              icon={record.parse_status === 'processing' ? <LoadingOutlined spin /> : <SyncOutlined />}
                              onClick={(e) => {
                                e.stopPropagation();
                                handleParseFile(record);
                              }}
                              disabled={record.parse_status === 'processing'}
                              loading={parsingFileId === record.id}
                            >
                              {record.parse_status === 'completed' ? '重新解析' : '解析'}
                            </Button>
                          </Tooltip>
                        </Space>
                      ),
                    },
                  ]}
                />
              </Col>
            </Row>
          </Spin>
        </Card>
      )}

      {/* 工具栏 */}
      <Card className="toolbar-card">
        <Space wrap>
          <Button 
            type="primary" 
            icon={<PlusOutlined />} 
            onClick={handleScanFilesystem}
            loading={loading}
          >
            扫描文件系统
          </Button>
          
          <Button 
            icon={<ReloadOutlined />} 
            onClick={loadKnowledgeTree}
            loading={treeLoading}
          >
            刷新数据
          </Button>
          
          <Button 
            icon={expandedKeys.length > 0 ? <CompressOutlined /> : <ExpandOutlined />}
            onClick={toggleExpandAll}
          >
            {expandedKeys.length > 0 ? '收起全部' : '展开全部'}
          </Button>
          
          <Divider type="vertical" />
          
          <Search
            placeholder="搜索文件或文件夹..."
            allowClear
            enterButton={<SearchOutlined />}
            size="middle"
            style={{ width: 300 }}
            onSearch={handleSearch}
            onChange={(e) => setSearchValue(e.target.value)}
          />
        </Space>
      </Card>

      {/* 知识树主体 */}
      <Row gutter={[16, 16]}>
        <Col span={18}>
          <Card 
            title="文件系统结构"
            className="tree-card"
            extra={
              <Space>
                <Text type="secondary">
                  {treeDataFormatted.length > 0 ? `${treeDataFormatted.length} 个项目` : '暂无数据'}
                </Text>
              </Space>
            }
          >
            <Spin spinning={loading || treeLoading} tip="加载中...">
              {treeDataFormatted.length > 0 ? (
                <DirectoryTree
                  treeData={treeDataFormatted}
                  expandedKeys={expandedKeys}
                  selectedKeys={selectedKeys}
                  autoExpandParent={autoExpandParent}
                  onExpand={(keys) => {
                    setExpandedKeys(keys as string[]);
                    setAutoExpandParent(false);
                  }}
                  onSelect={handleSelect}
                  titleRender={titleRender}
                  onRightClick={handleContextMenu}
                  className="knowledge-tree"
                />
              ) : (
                <Empty 
                  description="暂无数据"
                  image={Empty.PRESENTED_IMAGE_SIMPLE}
                >
                  <Button type="primary" onClick={handleScanFilesystem}>
                    开始扫描文件系统
                  </Button>
                </Empty>
              )}
            </Spin>
          </Card>
        </Col>
        
        {/* 节点详情面板 */}
        <Col span={6}>
          <Card 
            title="节点详情"
            className="details-card"
            extra={
              selectedKeys.length > 0 && (
                <Space>
                  <Tooltip title="查看详情">
                    <Button icon={<EyeOutlined />} size="small" />
                  </Tooltip>
                  <Tooltip title="下载">
                    <Button icon={<DownloadOutlined />} size="small" />
                  </Tooltip>
                  <Popconfirm
                    title="确定要删除这个节点吗？"
                    onConfirm={() => handleDeleteNode(parseInt(selectedKeys[0]))}
                    okText="确定"
                    cancelText="取消"
                  >
                    <Tooltip title="删除">
                      <Button icon={<DeleteOutlined />} size="small" danger />
                    </Tooltip>
                  </Popconfirm>
                </Space>
              )
            }
          >
            {selectedKeys.length > 0 ? (
              <NodeDetails 
                nodeId={parseInt(selectedKeys[0])}
                onParse={() => handleParseDocument(parseInt(selectedKeys[0]))}
                isParsing={parsingNodes.has(parseInt(selectedKeys[0]))}
              />
            ) : (
              <Empty description="选择一个节点查看详情" />
            )}
          </Card>
        </Col>
      </Row>

      {/* 文件预览Modal */}
      <Modal
        title={
          <Space>
            <EyeOutlined />
            <span>文件预览</span>
            {previewFile && (
              <Tag color="blue">{previewFile.name}</Tag>
            )}
          </Space>
        }
        open={previewVisible}
        onCancel={() => {
          setPreviewVisible(false);
          setPreviewFile(null);
          setPreviewContent('');
        }}
        width={900}
        footer={[
          <Button key="close" onClick={() => setPreviewVisible(false)}>
            关闭
          </Button>,
          previewFile && (
            <Button 
              key="download" 
              type="primary" 
              icon={<DownloadOutlined />}
              onClick={() => {
                if (previewFile?.path) {
                  message.info('下载功能开发中...');
                }
              }}
            >
              下载原文件
            </Button>
          ),
        ]}
      >
        {previewLoading ? (
          <div style={{ textAlign: 'center', padding: 50 }}>
            <Spin tip="加载预览内容..." />
          </div>
        ) : (
          <div className="file-preview-content">
            {previewFile && (
              <Descriptions column={2} size="small" style={{ marginBottom: 16 }}>
                <Descriptions.Item label="文件名">{previewFile.name}</Descriptions.Item>
                <Descriptions.Item label="类型">{previewFile.extension}</Descriptions.Item>
                <Descriptions.Item label="大小">
                  {previewFile.size ? `${(previewFile.size / 1024).toFixed(1)} KB` : '-'}
                </Descriptions.Item>
                <Descriptions.Item label="状态">
                  {getParseStatusTag(previewFile.parse_status)}
                </Descriptions.Item>
                <Descriptions.Item label="路径" span={2}>
                  <Text ellipsis style={{ maxWidth: 700 }}>{previewFile.path}</Text>
                </Descriptions.Item>
              </Descriptions>
            )}
            <Divider />
            <div 
              style={{ 
                maxHeight: 400, 
                overflow: 'auto', 
                padding: 16, 
                background: '#fafafa', 
                borderRadius: 4,
                whiteSpace: 'pre-wrap',
                wordBreak: 'break-word',
                fontFamily: 'monospace',
                fontSize: 13,
                lineHeight: 1.6
              }}
            >
              {previewContent || '无预览内容'}
            </div>
          </div>
        )}
      </Modal>
    </div>
  );
};

// 节点详情组件
const NodeDetails: React.FC<{ 
  nodeId: number; 
  onParse: () => void; 
  isParsing: boolean 
}> = ({ nodeId, onParse, isParsing }) => {
  const [node, setNode] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // 从API获取节点详情
    const fetchNodeDetail = async () => {
      setLoading(true);
      try {
        const response = await apiService.getDocumentDetail(nodeId);
        if (response.code === 200 && response.data) {
          setNode(response.data);
        }
      } catch (error) {
        console.error('获取节点详情失败:', error);
      } finally {
        setLoading(false);
      }
    };
    
    fetchNodeDetail();
  }, [nodeId]);

  if (loading) {
    return <Spin tip="加载详情..." />;
  }

  if (!node) {
    return <Empty description="无法加载节点详情" />;
  }

  return (
    <div className="node-details">
      <Descriptions column={1} size="small">
        <Descriptions.Item label="名称">{node.name}</Descriptions.Item>
        <Descriptions.Item label="类型">
          <Tag color={node.type === 'folder' ? 'blue' : 'green'}>
            {node.type === 'folder' ? '文件夹' : '文件'}
          </Tag>
        </Descriptions.Item>
        <Descriptions.Item label="路径">{node.path}</Descriptions.Item>
        {node.size && (
          <Descriptions.Item label="大小">{(node.size / 1024 / 1024).toFixed(2)} MB</Descriptions.Item>
        )}
        {node.extension && (
          <Descriptions.Item label="格式">{node.extension.toUpperCase()}</Descriptions.Item>
        )}
        {node.bookname && (
          <Descriptions.Item label="书名">{node.bookname}</Descriptions.Item>
        )}
        <Descriptions.Item label="修改时间">{node.modified_time}</Descriptions.Item>
        {node.parse_status && (
          <Descriptions.Item label="解析状态">
            {getParseStatusTag(node.parse_status)}
          </Descriptions.Item>
        )}
      </Descriptions>

      {node.keywords && node.keywords.length > 0 && (
        <div style={{ marginTop: 16 }}>
          <Text strong>关键词：</Text>
          <div style={{ marginTop: 4 }}>
            {node.keywords.map((keyword: string, index: number) => (
              <Tag key={index} style={{ margin: '2px' }}>{keyword}</Tag>
            ))}
          </div>
        </div>
      )}

      {node.abstract && (
        <div style={{ marginTop: 16 }}>
          <Text strong>摘要：</Text>
          <div style={{ marginTop: 4, fontSize: '12px', color: '#666', lineHeight: '1.4' }}>
            {node.abstract}
          </div>
        </div>
      )}

      {node.type === 'file' && (
        <div style={{ marginTop: 20 }}>
          <Button 
            type="primary" 
            icon={<FileTextOutlined />} 
            onClick={onParse}
            loading={isParsing}
            block
          >
            {node.parse_status === 'completed' ? '重新解析' : '开始解析'}
          </Button>
        </div>
      )}
    </div>
  );
};

export default KnowledgeTree;