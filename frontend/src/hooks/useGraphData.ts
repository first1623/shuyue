/**
 * 图谱数据查询 Hook
 * 使用 React Query 实现数据缓存和自动更新
 */

import { useQuery } from '@tanstack/react-query';
import axios from 'axios';
import { GraphData, GraphStats } from '@/types/graph';

const API_BASE_URL = 'http://localhost:8000';

/**
 * 获取图谱数据
 */
export const useGraphData = (dimension: 'theory' | 'author' | 'entity') => {
  return useQuery({
    queryKey: ['graphData', dimension],
    queryFn: async (): Promise<GraphData> => {
      const response = await axios.get(`${API_BASE_URL}/api/v1/graph/data`, {
        params: { dimension }
      });
      
      if (response.data?.code === 200 && response.data?.data) {
        return response.data.data;
      }
      
      throw new Error('获取图谱数据失败');
    },
    staleTime: 5 * 60 * 1000,    // 5分钟内认为数据新鲜
    gcTime: 10 * 60 * 1000,       // 10分钟后清除缓存（原cacheTime）
    refetchOnWindowFocus: false,  // 窗口聚焦时不重新获取
    retry: 2,                     // 失败重试2次
    retryDelay: 1000,             // 重试延迟1秒
  });
};

/**
 * 获取图谱统计信息
 */
export const useGraphStats = () => {
  return useQuery({
    queryKey: ['graphStats'],
    queryFn: async (): Promise<GraphStats> => {
      const response = await axios.get(`${API_BASE_URL}/api/v1/graph/stats`);
      
      if (response.data?.code === 200 && response.data?.data) {
        return response.data.data;
      }
      
      throw new Error('获取图谱统计失败');
    },
    staleTime: 10 * 60 * 1000,    // 10分钟内认为数据新鲜
    gcTime: 30 * 60 * 1000,       // 30分钟后清除缓存
    refetchOnWindowFocus: false,
    retry: 2,
  });
};

/**
 * 获取节点详情
 */
export const useNodeDetail = (nodeId: string | null) => {
  return useQuery({
    queryKey: ['nodeDetail', nodeId],
    queryFn: async () => {
      if (!nodeId) return null;
      
      const response = await axios.get(`${API_BASE_URL}/api/v1/nodes/${nodeId}`);
      
      if (response.data?.code === 200 && response.data?.data) {
        return response.data.data;
      }
      
      throw new Error('获取节点详情失败');
    },
    enabled: !!nodeId,  // 只有nodeId存在时才执行查询
    staleTime: 5 * 60 * 1000,
    gcTime: 10 * 60 * 1000,
    retry: 1,
  });
};

/**
 * 预取图谱数据
 */
export const usePrefetchGraphData = () => {
  const queryClient = useQueryClient();
  
  const prefetchGraphData = (dimension: 'theory' | 'author' | 'entity') => {
    queryClient.prefetchQuery({
      queryKey: ['graphData', dimension],
      queryFn: async (): Promise<GraphData> => {
        const response = await axios.get(`${API_BASE_URL}/api/v1/graph/data`, {
          params: { dimension }
        });
        
        if (response.data?.code === 200 && response.data?.data) {
          return response.data.data;
        }
        
        throw new Error('获取图谱数据失败');
      },
      staleTime: 5 * 60 * 1000,
    });
  };
  
  return { prefetchGraphData };
};

import { useQueryClient } from '@tanstack/react-query';
