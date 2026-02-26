import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { apiService } from '../../services/api.service';

interface SystemStats {
  total_files: number;
  total_folders: number;
  supported_docs: number;
  total_size_mb: number;
  parse_success_rate: number;
  active_users: number;
}

interface SystemState {
  stats: SystemStats | null;
  loading: boolean;
  error: string | null;
}

const initialState: SystemState = {
  stats: null,
  loading: false,
  error: null,
};

// 获取系统统计
export const fetchSystemStats = createAsyncThunk(
  'system/fetchStats',
  async (_, { rejectWithValue }) => {
    try {
      const response = await apiService.getSystemStats();
      // response 已经是 axios 响应的 data 部分，即 {code, data: {...}}
      return response.data || response;
    } catch (error: any) {
      return rejectWithValue(error.message);
    }
  }
);

const systemSlice = createSlice({
  name: 'system',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchSystemStats.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchSystemStats.fulfilled, (state, action) => {
        state.loading = false;
        state.stats = action.payload;
      })
      .addCase(fetchSystemStats.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      });
  },
});

export const { clearError } = systemSlice.actions;
export default systemSlice.reducer;
