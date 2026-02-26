import React, { useState, useEffect } from 'react';
import {
  Card,
  Table,
  Button,
  Space,
  Input,
  Tag,
  Modal,
  Descriptions,
  message,
  Popconfirm,
  Upload,
  Progress,
  Typography,
  Row,
  Col,
  Statistic,
  Tooltip,
  Empty,
} from 'antd';
import {
  FileTextOutlined,
  SearchOutlined,
  DeleteOutlined,
  EyeOutlined,
  ReloadOutlined,
  UploadOutlined,
  FolderOpenOutlined,
  CheckCircleOutlined,
  ClockCircleOutlined,
  ExclamationCircleOutlined,
} from '@ant-design/icons';
import { useDispatch, useSelector } from 'react-redux';
import { fetchDocuments, fetchDocumentDetail, parseDocument } from '../store/slices/documentSlice';

const { Search } = Input;
const { Text, Title } = Typography;

interface Document {
  id: number;
  file_name: string;
  file_path: string;
  file_type: string;
  file_size?: number;
  parse_status?: string;
  created_at: string;
  updated_at: string;
  // 兼容后端返回的字段名
  name?: string;
  path?: string;
  type?: string;
  size?: number;
}

const DocumentManager: React.FC = () => {
  const dispatch = useDispatch();
  const [loading, setLoading] = useState(false);
  const [detailVisible, setDetailVisible] = useState(false);
  const [selectedDocument, setSelectedDocument] = useState<any>(null);
  const [searchQuery, setSearchQuery] = useState('');

  const { documents, currentDocument } = useSelector((state: any) => state.document);

  // 确保 documents 是数组
  const safeDocuments = Array.isArray(documents) ? documents : [];

  useEffect(() => {
    loadDocuments();
  }, []);

  const loadDocuments = async () => {
    setLoading(true);
    try {
      await dispatch(fetchDocuments({}) as any);
    } catch (error) {
      message.error('加载文档列表失败');
    } finally {
      setLoading(false);
    }
  };

  const handleViewDetail = async (doc: Document) => {
    try {
      await dispatch(fetchDocumentDetail(doc.id) as any);
      setSelectedDocument(doc);
      setDetailVisible(true);
    } catch (error) {
      message.error('获取文档详情失败');
    }
  };

  const handleParseDocument = async (doc: Document) => {
    try {
      const filePath = doc.file_path || doc.path || '';
      await dispatch(parseDocument({ filePath, fileId: doc.id }) as any);
      message.success('文档解析已开始');
      loadDocuments();
    } catch (error) {
      message.error('解析失败');
    }
  };

  const getStatusTag = (status?: string) => {
    switch (status) {
      case 'completed':
        return <Tag icon={<CheckCircleOutlined />} color="success">已解析</Tag>;
      case 'pending':
        return <Tag icon={<ClockCircleOutlined />} color="warning">待解析</Tag>;
      case 'failed':
        return <Tag icon={<ExclamationCircleOutlined />} color="error">解析失败</Tag>;
      default:
        return <Tag color="default">未知</Tag>;
    }
  };

  const formatFileSize = (bytes?: number) => {
    if (!bytes) return '-';
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(1024));
    return `${(bytes / Math.pow(1024, i)).toFixed(2)} ${sizes[i]}`;
  };

  const columns = [
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
      width: 60,
    },
    {
      title: '文件名',
      dataIndex: 'file_name',
      key: 'file_name',
      ellipsis: true,
      render: (text: string, record: Document) => (
        <Space>
          <FileTextOutlined />
          <Text strong>{text || record.name}</Text>
        </Space>
      ),
    },
    {
      title: '文件路径',
      dataIndex: 'file_path',
      key: 'file_path',
      ellipsis: true,
      width: 300,
      render: (text: string, record: Document) => text || record.path,
    },
    {
      title: '文件大小',
      dataIndex: 'file_size',
      key: 'file_size',
      width: 100,
      render: (size: number, record: Document) => formatFileSize(size || record.size),
    },
    {
      title: '解析状态',
      dataIndex: 'parse_status',
      key: 'parse_status',
      width: 100,
      render: (status: string) => getStatusTag(status),
    },
    {
      title: '创建时间',
      dataIndex: 'created_at',
      key: 'created_at',
      width: 180,
      render: (time: string) => time ? new Date(time).toLocaleString() : '-',
    },
    {
      title: '操作',
      key: 'action',
      width: 200,
      render: (_: any, record: Document) => (
        <Space>
          <Tooltip title="查看详情">
            <Button
              type="text"
              icon={<EyeOutlined />}
              onClick={() => handleViewDetail(record)}
            />
          </Tooltip>
          <Tooltip title="解析文档">
            <Button
              type="text"
              icon={<FileTextOutlined />}
              onClick={() => handleParseDocument(record)}
            />
          </Tooltip>
          <Popconfirm
            title="确定要删除这个文档吗？"
            onConfirm={() => message.success('删除成功')}
            okText="确定"
            cancelText="取消"
          >
            <Tooltip title="删除">
              <Button type="text" icon={<DeleteOutlined />} danger />
            </Tooltip>
          </Popconfirm>
        </Space>
      ),
    },
  ];

  return (
    <div className="document-manager-page">
      <div className="page-header">
        <Title level={2}>文档管理</Title>
        <Text type="secondary">管理所有文档，进行解析和查看</Text>
      </div>

      <Row gutter={[16, 16]} style={{ marginBottom: 16 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="文档总数"
              value={safeDocuments.length}
              prefix={<FileTextOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="已解析"
              value={safeDocuments.filter((d: Document) => d.parse_status === 'completed').length}
              prefix={<CheckCircleOutlined />}
              valueStyle={{ color: '#52c41a' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="待解析"
              value={safeDocuments.filter((d: Document) => d.parse_status === 'pending').length}
              prefix={<ClockCircleOutlined />}
              valueStyle={{ color: '#faad14' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="解析失败"
              value={safeDocuments.filter((d: Document) => d.parse_status === 'failed').length}
              prefix={<ExclamationCircleOutlined />}
              valueStyle={{ color: '#ff4d4f' }}
            />
          </Card>
        </Col>
      </Row>

      <Card>
        <div style={{ marginBottom: 16 }}>
          <Space>
            <Button icon={<ReloadOutlined />} onClick={loadDocuments} loading={loading}>
              刷新
            </Button>
            <Button icon={<FolderOpenOutlined />} onClick={() => message.info('请使用知识树页面扫描文件夹')}>
              扫描文件夹
            </Button>
            <Search
              placeholder="搜索文档..."
              allowClear
              enterButton={<SearchOutlined />}
              style={{ width: 300 }}
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onSearch={(value) => message.info(`搜索: ${value}`)}
            />
          </Space>
        </div>

        <Table
          columns={columns}
          dataSource={safeDocuments}
          rowKey="id"
          loading={loading}
          pagination={{
            pageSize: 10,
            showSizeChanger: true,
            showTotal: (total) => `共 ${total} 条`,
          }}
        />
      </Card>

      <Modal
        title="文档详情"
        open={detailVisible}
        onCancel={() => setDetailVisible(false)}
        footer={null}
        width={800}
      >
        {currentDocument ? (
          <Descriptions bordered column={1}>
            <Descriptions.Item label="摘要">{currentDocument.abstract || '-'}</Descriptions.Item>
            <Descriptions.Item label="关键词">
              {currentDocument.keywords?.map((k: string, i: number) => (
                <Tag key={i} color="blue">{k}</Tag>
              )) || '-'}
            </Descriptions.Item>
            <Descriptions.Item label="理论">{currentDocument.theories?.join(', ') || '-'}</Descriptions.Item>
            <Descriptions.Item label="实验流程">{currentDocument.experiment_flow || '-'}</Descriptions.Item>
            <Descriptions.Item label="统计方法">{currentDocument.statistical_methods?.join(', ') || '-'}</Descriptions.Item>
            <Descriptions.Item label="结论">{currentDocument.conclusion || '-'}</Descriptions.Item>
            <Descriptions.Item label="解析状态">
              {getStatusTag(currentDocument.parse_status)}
            </Descriptions.Item>
            <Descriptions.Item label="置信度">
              {currentDocument.confidence_score ? `${(currentDocument.confidence_score * 100).toFixed(1)}%` : '-'}
            </Descriptions.Item>
          </Descriptions>
        ) : (
          <Empty description="暂无详情" />
        )}
      </Modal>
    </div>
  );
};

export default DocumentManager;
