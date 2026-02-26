/**
 * LOD (Level of Detail) 控制器
 * 根据缩放级别自动调整渲染细节，优化性能
 */

import { GraphNode } from '@/types/graph';

export enum LODLevel {
  FULL = 'full',        // 显示所有细节
  MEDIUM = 'medium',    // 显示节点和关键标签
  LOW = 'low',          // 仅显示节点
  CLUSTERED = 'clustered' // 聚类显示
}

export class LODController {
  private zoom: number = 1;
  
  /**
   * 根据缩放级别获取LOD等级
   */
  getLODLevel(zoom: number): LODLevel {
    if (zoom > 0.7) return LODLevel.FULL;
    if (zoom > 0.4) return LODLevel.MEDIUM;
    if (zoom > 0.2) return LODLevel.LOW;
    return LODLevel.CLUSTERED;
  }
  
  /**
   * 判断是否应该显示标签
   */
  shouldShowLabel(zoom: number): boolean {
    return this.getLODLevel(zoom) !== LODLevel.CLUSTERED;
  }
  
  /**
   * 判断是否应该显示边
   */
  shouldShowEdge(zoom: number): boolean {
    return this.getLODLevel(zoom) !== LODLevel.CLUSTERED;
  }
  
  /**
   * 获取节点显示大小
   */
  getNodeSize(node: GraphNode, zoom: number): number {
    const baseSize = Math.min(Math.max(node.size, 15), 50);
    const level = this.getLODLevel(zoom);
    
    switch (level) {
      case LODLevel.FULL:
        return baseSize;
      case LODLevel.MEDIUM:
        return baseSize * 0.8;
      case LODLevel.LOW:
        return baseSize * 0.6;
      case LODLevel.CLUSTERED:
        return baseSize * 0.4;
      default:
        return baseSize;
    }
  }
  
  /**
   * 获取边显示宽度
   */
  getEdgeWidth(zoom: number): number {
    const level = this.getLODLevel(zoom);
    
    switch (level) {
      case LODLevel.FULL:
        return 1.5;
      case LODLevel.MEDIUM:
        return 1.2;
      case LODLevel.LOW:
        return 0.8;
      case LODLevel.CLUSTERED:
        return 0.5;
      default:
        return 1;
    }
  }
  
  /**
   * 获取标签字体大小
   */
  getLabelFontSize(zoom: number): number {
    const level = this.getLODLevel(zoom);
    
    switch (level) {
      case LODLevel.FULL:
        return 11;
      case LODLevel.MEDIUM:
        return 10;
      case LODLevel.LOW:
        return 9;
      case LODLevel.CLUSTERED:
        return 8;
      default:
        return 11;
    }
  }
  
  /**
   * 判断节点是否需要聚类
   */
  shouldCluster(zoom: number, nodeCount: number): boolean {
    const level = this.getLODLevel(zoom);
    return level === LODLevel.CLUSTERED && nodeCount > 50;
  }
  
  /**
   * 获取聚类半径
   */
  getClusterRadius(zoom: number): number {
    return 50 / zoom;
  }
}
