import axios, { AxiosInstance, AxiosRequestConfig } from 'axios';

// API 基础配置
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// 创建 axios 实例
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 请求拦截器
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// 响应拦截器
apiClient.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error.response?.data || error.message);
  }
);

// API 服务类
export const apiService = {
  // 健康检查
  async healthCheck(): Promise<any> {
    return apiClient.get('/health');
  },

  // 获取系统统计
  async getSystemStats(): Promise<any> {
    return apiClient.get('/api/v1/system/stats');
  },

  // 获取文档列表
  async getDocuments(skip: number = 0, limit: number = 20, fileType?: string): Promise<any> {
    const params: any = { skip, limit };
    if (fileType) params.file_type = fileType;
    return apiClient.get('/api/v1/documents', { params });
  },

  // 获取文档详情
  async getDocumentDetail(documentId: number): Promise<any> {
    return apiClient.get(`/api/v1/documents/${documentId}`);
  },

  // 解析文档
  async parseDocument(filePath: string, fileId: number): Promise<any> {
    return apiClient.post('/api/v1/documents/parse', { file_path: filePath, file_id: fileId });
  },

  // 扫描文件夹
  async scanFolder(folderPath: string, recursive: boolean = true): Promise<any> {
    return apiClient.post('/api/v1/folders/scan', { folder_path: folderPath, recursive });
  },

  // 获取知识树
  async getKnowledgeTree(): Promise<any> {
    return apiClient.get('/api/v1/knowledge-tree');
  },

  // 扫描知识树文件夹
  async scanKnowledgeTree(folderPath: string = 'D:/zyfdownloadanalysis'): Promise<any> {
    return apiClient.post(`/api/v1/knowledge-tree/scan?folder_path=${encodeURIComponent(folderPath)}`);
  },

  // 获取扫描进度
  async getScanStatus(): Promise<any> {
    return apiClient.get('/api/v1/knowledge-tree/scan/status');
  },

  // 搜索文档
  async searchDocuments(query: string, skip: number = 0, limit: number = 20): Promise<any> {
    return apiClient.get('/api/v1/search', { params: { q: query, skip, limit } });
  },

  // 获取已扫描的文件列表
  async getScannedFiles(): Promise<any> {
    return apiClient.get('/api/v1/knowledge-tree/scanned-files');
  },

  // 预览文件
  async previewFile(fileId: number): Promise<any> {
    return apiClient.get(`/api/v1/knowledge-tree/files/${fileId}/preview`);
  },

  // 获取文档解析状态
  async getParseStatus(documentId: number): Promise<any> {
    return apiClient.get(`/api/v1/documents/${documentId}/parse/status`);
  },

  // 批量获取解析状态
  async getBatchParseStatus(fileIds: number[]): Promise<any> {
    return apiClient.post('/api/v1/documents/parse/status/batch', { file_ids: fileIds });
  },
};
