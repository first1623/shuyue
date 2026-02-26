import React, { useState } from 'react';
import {
  Card,
  Form,
  Input,
  Button,
  Switch,
  Select,
  Divider,
  message,
  Typography,
  Row,
  Col,
  Tabs,
  Space,
  Alert,
  Descriptions,
} from 'antd';
import {
  SaveOutlined,
  ReloadOutlined,
  ApiOutlined,
  DatabaseOutlined,
  SettingOutlined,
  UserOutlined,
} from '@ant-design/icons';

const { Title, Text, Paragraph } = Typography;
const { Option } = Select;
const { TabPane } = Tabs;

const SystemSettings: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [apiForm] = Form.useForm();
  const [dbForm] = Form.useForm();
  const [userForm] = Form.useForm();

  const handleSaveApiSettings = async (values: any) => {
    setLoading(true);
    try {
      console.log('保存API设置:', values);
      message.success('API设置保存成功');
    } catch (error) {
      message.error('保存失败');
    } finally {
      setLoading(false);
    }
  };

  const handleSaveDbSettings = async (values: any) => {
    setLoading(true);
    try {
      console.log('保存数据库设置:', values);
      message.success('数据库设置保存成功');
    } catch (error) {
      message.error('保存失败');
    } finally {
      setLoading(false);
    }
  };

  const handleSaveUserSettings = async (values: any) => {
    setLoading(true);
    try {
      console.log('保存用户设置:', values);
      message.success('用户设置保存成功');
    } catch (error) {
      message.error('保存失败');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="system-settings-page">
      <div className="page-header">
        <Title level={2}>系统设置</Title>
        <Text type="secondary">配置系统参数和用户信息</Text>
      </div>

      <Tabs defaultActiveKey="api">
        <TabPane tab={<span><ApiOutlined /> API配置</span>} key="api">
          <Card>
            <Form
              form={apiForm}
              layout="vertical"
              onFinish={handleSaveApiSettings}
              initialValues={{
                deepseek_api_key: 'sk-****',
                api_timeout: 30,
                max_retries: 3,
                enable_cache: true,
              }}
            >
              <Alert
                message="API配置"
                description="配置DeepSeek API和其他外部服务的连接参数"
                type="info"
                showIcon
                style={{ marginBottom: 24 }}
              />

              <Row gutter={24}>
                <Col span={12}>
                  <Form.Item
                    name="deepseek_api_key"
                    label="DeepSeek API Key"
                    rules={[{ required: true, message: '请输入API Key' }]}
                  >
                    <Input.Password placeholder="sk-xxxxx" />
                  </Form.Item>
                </Col>
                <Col span={12}>
                  <Form.Item
                    name="api_base_url"
                    label="API Base URL"
                  >
                    <Input placeholder="https://api.deepseek.com/v1" />
                  </Form.Item>
                </Col>
              </Row>

              <Row gutter={24}>
                <Col span={8}>
                  <Form.Item
                    name="api_timeout"
                    label="请求超时(秒)"
                  >
                    <Input type="number" />
                  </Form.Item>
                </Col>
                <Col span={8}>
                  <Form.Item
                    name="max_retries"
                    label="最大重试次数"
                  >
                    <Input type="number" />
                  </Form.Item>
                </Col>
                <Col span={8}>
                  <Form.Item
                    name="enable_cache"
                    label="启用缓存"
                    valuePropName="checked"
                  >
                    <Switch />
                  </Form.Item>
                </Col>
              </Row>

              <Form.Item>
                <Button type="primary" htmlType="submit" icon={<SaveOutlined />} loading={loading}>
                  保存设置
                </Button>
              </Form.Item>
            </Form>
          </Card>
        </TabPane>

        <TabPane tab={<span><DatabaseOutlined /> 数据库配置</span>} key="database">
          <Card>
            <Form
              form={dbForm}
              layout="vertical"
              onFinish={handleSaveDbSettings}
              initialValues={{
                database_type: 'sqlite',
                database_url: 'sqlite:///./knowledge_graph.db',
                neo4j_enabled: false,
                redis_enabled: false,
              }}
            >
              <Alert
                message="数据库配置"
                description="配置SQLite、PostgreSQL、Neo4j和Redis数据库连接"
                type="info"
                showIcon
                style={{ marginBottom: 24 }}
              />

              <Row gutter={24}>
                <Col span={12}>
                  <Form.Item
                    name="database_type"
                    label="数据库类型"
                  >
                    <Select>
                      <Option value="sqlite">SQLite</Option>
                      <Option value="postgresql">PostgreSQL</Option>
                      <Option value="mysql">MySQL</Option>
                    </Select>
                  </Form.Item>
                </Col>
                <Col span={12}>
                  <Form.Item
                    name="database_url"
                    label="数据库连接URL"
                  >
                    <Input placeholder="数据库连接字符串" />
                  </Form.Item>
                </Col>
              </Row>

              <Divider>高级数据库</Divider>

              <Row gutter={24}>
                <Col span={12}>
                  <Form.Item
                    name="neo4j_url"
                    label="Neo4j URL"
                  >
                    <Input placeholder="bolt://localhost:7687" />
                  </Form.Item>
                </Col>
                <Col span={12}>
                  <Form.Item
                    name="neo4j_enabled"
                    label="启用Neo4j"
                    valuePropName="checked"
                  >
                    <Switch />
                  </Form.Item>
                </Col>
              </Row>

              <Row gutter={24}>
                <Col span={12}>
                  <Form.Item
                    name="redis_url"
                    label="Redis URL"
                  >
                    <Input placeholder="redis://localhost:6379" />
                  </Form.Item>
                </Col>
                <Col span={12}>
                  <Form.Item
                    name="redis_enabled"
                    label="启用Redis"
                    valuePropName="checked"
                  >
                    <Switch />
                  </Form.Item>
                </Col>
              </Row>

              <Form.Item>
                <Button type="primary" htmlType="submit" icon={<SaveOutlined />} loading={loading}>
                  保存设置
                </Button>
                <Button style={{ marginLeft: 8 }} icon={<ReloadOutlined />}>
                  测试连接
                </Button>
              </Form.Item>
            </Form>
          </Card>
        </TabPane>

        <TabPane tab={<span><UserOutlined /> 用户设置</span>} key="user">
          <Card>
            <Form
              form={userForm}
              layout="vertical"
              onFinish={handleSaveUserSettings}
              initialValues={{
                username: 'admin',
                email: 'admin@example.com',
                full_name: '管理员',
              }}
            >
              <Alert
                message="用户设置"
                description="修改当前用户的个人信息"
                type="info"
                showIcon
                style={{ marginBottom: 24 }}
              />

              <Row gutter={24}>
                <Col span={12}>
                  <Form.Item
                    name="username"
                    label="用户名"
                  >
                    <Input disabled />
                  </Form.Item>
                </Col>
                <Col span={12}>
                  <Form.Item
                    name="email"
                    label="邮箱"
                    rules={[{ type: 'email', message: '请输入有效的邮箱地址' }]}
                  >
                    <Input placeholder="user@example.com" />
                  </Form.Item>
                </Col>
              </Row>

              <Row gutter={24}>
                <Col span={12}>
                  <Form.Item
                    name="full_name"
                    label="全名"
                  >
                    <Input placeholder="用户全名" />
                  </Form.Item>
                </Col>
                <Col span={12}>
                  <Form.Item
                    name="role"
                    label="角色"
                  >
                    <Select disabled>
                      <Option value="admin">管理员</Option>
                      <Option value="user">普通用户</Option>
                    </Select>
                  </Form.Item>
                </Col>
              </Row>

              <Divider>修改密码</Divider>

              <Row gutter={24}>
                <Col span={8}>
                  <Form.Item
                    name="old_password"
                    label="旧密码"
                  >
                    <Input.Password placeholder="输入旧密码" />
                  </Form.Item>
                </Col>
                <Col span={8}>
                  <Form.Item
                    name="new_password"
                    label="新密码"
                  >
                    <Input.Password placeholder="输入新密码" />
                  </Form.Item>
                </Col>
                <Col span={8}>
                  <Form.Item
                    name="confirm_password"
                    label="确认密码"
                  >
                    <Input.Password placeholder="确认新密码" />
                  </Form.Item>
                </Col>
              </Row>

              <Form.Item>
                <Button type="primary" htmlType="submit" icon={<SaveOutlined />} loading={loading}>
                  保存设置
                </Button>
              </Form.Item>
            </Form>
          </Card>
        </TabPane>

        <TabPane tab={<span><SettingOutlined /> 系统信息</span>} key="system">
          <Card>
            <Descriptions bordered column={2}>
              <Descriptions.Item label="系统版本">1.0.0</Descriptions.Item>
              <Descriptions.Item label="API版本">v1</Descriptions.Item>
              <Descriptions.Item label="Python版本">3.13.12</Descriptions.Item>
              <Descriptions.Item label="数据库">SQLite</Descriptions.Item>
              <Descriptions.Item label="后端框架">FastAPI</Descriptions.Item>
              <Descriptions.Item label="前端框架">React + Ant Design</Descriptions.Item>
              <Descriptions.Item label="AI模型">DeepSeek API</Descriptions.Item>
              <Descriptions.Item label="图数据库">Neo4j (可选)</Descriptions.Item>
            </Descriptions>

            <Divider />

            <Paragraph>
              <Text strong>功能特性:</Text>
            </Paragraph>
            <ul>
              <li>多格式文档解析 (PDF, DOCX, TXT, MD)</li>
              <li>DeepSeek AI 智能内容分析</li>
              <li>知识图谱自动构建</li>
              <li>文档内容搜索</li>
              <li>图谱可视化展示</li>
            </ul>
          </Card>
        </TabPane>
      </Tabs>
    </div>
  );
};

export default SystemSettings;
