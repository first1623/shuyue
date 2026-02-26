import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { apiService } from '../../services/api.service';

interface Document {
  id: number;
  file_name: string;
  file_path: string;
  file_type: string;
  file_size?: number;
  parse_status?: string;
  created_at: string;
  updated_at: string;
  // 兼容后端字段
  name?: string;
  path?: string;
  type?: string;
  size?: number;
  extension?: string;
}

interface DocumentDetail {
  id: number;
  file_id: number;
  abstract?: string;
  keywords?: string[];
  theories?: string[];
  experiment_flow?: string;
  statistical_methods?: string[];
  conclusion?: string;
  parse_status?: string;
  parse_time?: string;
  confidence_score?: number;
}

interface DocumentState {
  documents: Document[];
  currentDocument: DocumentDetail | null;
  loading: boolean;
  error: string | null;
  total: number;
}

const initialState: DocumentState = {
  documents: [],
  currentDocument: null,
  loading: false,
  error: null,
  total: 0,
};

// 获取文档列表
export const fetchDocuments = createAsyncThunk(
  'document/fetchList',
  async (params: { skip?: number; limit?: number; file_type?: string } = {}, { rejectWithValue }) => {
    try {
      const response = await apiService.getDocuments(params.skip, params.limit, params.file_type);
      // response 已经是 axios 响应的 data 部分
      const data = response.data || response;
      const documents = Array.isArray(data?.documents) ? data.documents : [];
      
      // 映射字段名以兼容前后端
      const mappedDocuments = documents.map((doc: any) => ({
        id: doc.id,
        file_name: doc.file_name || doc.name || '',
        file_path: doc.file_path || doc.path || '',
        file_type: doc.file_type || doc.type || '',
        file_size: doc.file_size || doc.size || 0,
        parse_status: doc.parse_status || 'pending',
        created_at: doc.created_at || new Date().toISOString(),
        updated_at: doc.updated_at || new Date().toISOString(),
        extension: doc.extension || '',
      }));
      
      return { documents: mappedDocuments, total: data?.total || mappedDocuments.length };
    } catch (error: any) {
      return rejectWithValue(error.message);
    }
  }
);

// 获取文档详情
export const fetchDocumentDetail = createAsyncThunk(
  'document/fetchDetail',
  async (documentId: number, { rejectWithValue }) => {
    try {
      const response = await apiService.getDocumentDetail(documentId);
      return response.data || null;
    } catch (error: any) {
      return rejectWithValue(error.message);
    }
  }
);

// 解析文档
export const parseDocument = createAsyncThunk(
  'document/parse',
  async ({ filePath, fileId }: { filePath: string; fileId: number }, { rejectWithValue }) => {
    try {
      const response = await apiService.parseDocument(filePath, fileId);
      return response;
    } catch (error: any) {
      return rejectWithValue(error.message);
    }
  }
);

// 搜索文档
export const searchDocuments = createAsyncThunk(
  'document/search',
  async (query: string, { rejectWithValue }) => {
    try {
      const response = await apiService.searchDocuments(query);
      return response;
    } catch (error: any) {
      return rejectWithValue(error.message);
    }
  }
);

const documentSlice = createSlice({
  name: 'document',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    clearCurrentDocument: (state) => {
      state.currentDocument = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchDocuments.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchDocuments.fulfilled, (state, action) => {
        state.loading = false;
        state.documents = action.payload.documents || [];
        state.total = action.payload.total || 0;
      })
      .addCase(fetchDocuments.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      .addCase(fetchDocumentDetail.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchDocumentDetail.fulfilled, (state, action) => {
        state.loading = false;
        state.currentDocument = action.payload;
      })
      .addCase(fetchDocumentDetail.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      .addCase(parseDocument.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(parseDocument.fulfilled, (state, action) => {
        state.loading = false;
      })
      .addCase(parseDocument.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      });
  },
});

export const { clearError, clearCurrentDocument } = documentSlice.actions;
export default documentSlice.reducer;
