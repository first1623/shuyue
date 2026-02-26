import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { apiService } from '../../services/api.service';

interface TreeNode {
  id: number;
  name: string;
  path: string;
  type: 'folder' | 'file';
  size?: number;
  extension?: string;
  bookname?: string;
  children?: TreeNode[];
}

interface KnowledgeTreeStats {
  total_files: number;
  total_folders: number;
  supported_docs: number;
  total_size_mb: number;
}

interface KnowledgeTreeState {
  treeData: TreeNode[];
  stats: KnowledgeTreeStats | null;
  loading: boolean;
  error: string | null;
}

const initialState: KnowledgeTreeState = {
  treeData: [],
  stats: null,
  loading: false,
  error: null,
};

// 获取知识树
export const fetchKnowledgeTree = createAsyncThunk(
  'knowledgeTree/fetchTree',
  async (params: { include_files?: boolean } = {}, { rejectWithValue }) => {
    try {
      const response = await apiService.getKnowledgeTree();
      // response 已经是 axios 响应的 data 部分，即 {code, data: [...], stats: {...}}
      const data = response.data || response;
      const stats = response.stats || null;
      
      // 数据已经是树形结构
      const treeData = Array.isArray(data) ? data : [];
      
      return { treeData, stats };
    } catch (error: any) {
      return rejectWithValue(error.message);
    }
  }
);

// 扫描文件系统
export const scanFilesystem = createAsyncThunk(
  'knowledgeTree/scanFilesystem',
  async (folderPath: string = 'D:/zyfdownloadanalysis', { rejectWithValue }) => {
    try {
      const response = await apiService.scanFolder(folderPath);
      // response 已经是 axios 响应的 data 部分
      return response.data || response;
    } catch (error: any) {
      return rejectWithValue(error.message);
    }
  }
);

// 删除节点
export const deleteNode = createAsyncThunk(
  'knowledgeTree/deleteNode',
  async (nodeId: number, { rejectWithValue }) => {
    try {
      // 实际应该调用API删除
      return nodeId;
    } catch (error: any) {
      return rejectWithValue(error.message);
    }
  }
);

const knowledgeTreeSlice = createSlice({
  name: 'knowledgeTree',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    setTreeData: (state, action: PayloadAction<TreeNode[]>) => {
      state.treeData = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchKnowledgeTree.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchKnowledgeTree.fulfilled, (state, action) => {
        state.loading = false;
        state.treeData = action.payload.treeData;
        state.stats = action.payload.stats;
      })
      .addCase(fetchKnowledgeTree.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      .addCase(scanFilesystem.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(scanFilesystem.fulfilled, (state, action) => {
        state.loading = false;
      })
      .addCase(scanFilesystem.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      .addCase(deleteNode.fulfilled, (state, action) => {
        // 从树中移除节点
        const removeNode = (nodes: TreeNode[], id: number): TreeNode[] => {
          return nodes.filter(node => {
            if (node.id === id) return false;
            if (node.children) {
              node.children = removeNode(node.children, id);
            }
            return true;
          });
        };
        state.treeData = removeNode(state.treeData, action.payload);
      });
  },
});

export const { clearError, setTreeData } = knowledgeTreeSlice.actions;
export default knowledgeTreeSlice.reducer;
