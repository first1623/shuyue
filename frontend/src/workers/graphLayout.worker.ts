/**
 * 图谱布局计算 Web Worker
 * 在后台线程中进行力导向布局计算，避免阻塞主线程
 */

import { GraphNode, GraphEdge } from '../types/graph';

interface NodePosition {
  x: number;
  y: number;
  vx: number;
  vy: number;
}

interface LayoutMessage {
  nodes: GraphNode[];
  edges: GraphEdge[];
  width: number;
  height: number;
  iterations?: number;
}

/**
 * 力导向布局算法
 */
function forceLayout(
  nodes: GraphNode[],
  edges: GraphEdge[],
  width: number,
  height: number,
  iterations: number = 300
): Map<string, NodePosition> {
  const positions = new Map<string, NodePosition>();
  
  // 1. 初始化节点位置（圆形布局）
  const centerX = width / 2;
  const centerY = height / 2;
  const radius = Math.min(width, height) / 3;
  
  nodes.forEach((node, index) => {
    const angle = (2 * Math.PI * index) / nodes.length;
    positions.set(node.id, {
      x: centerX + radius * Math.cos(angle),
      y: centerY + radius * Math.sin(angle),
      vx: 0,
      vy: 0
    });
  });
  
  // 2. 力导向迭代
  for (let i = 0; i < iterations; i++) {
    // 计算节点间斥力
    nodes.forEach(nodeA => {
      nodes.forEach(nodeB => {
        if (nodeA.id === nodeB.id) return;
        
        const posA = positions.get(nodeA.id)!;
        const posB = positions.get(nodeB.id)!;
        
        const dx = posA.x - posB.x;
        const dy = posA.y - posB.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        if (distance < 1) return;
        
        // 斥力公式：F = k / d²
        const k = 300;
        const force = k / (distance * distance);
        
        // 应用斥力
        posA.x += (dx / distance) * force;
        posA.y += (dy / distance) * force;
      });
    });
    
    // 计算边引力
    edges.forEach(edge => {
      const sourcePos = positions.get(edge.source);
      const targetPos = positions.get(edge.target);
      
      if (!sourcePos || !targetPos) return;
      
      const dx = targetPos.x - sourcePos.x;
      const dy = targetPos.y - sourcePos.y;
      const distance = Math.sqrt(dx * dx + dy * dy);
      
      if (distance < 1) return;
      
      // 引力公式：F = k * d
      const k = 0.1;
      const force = distance * k;
      
      // 应用引力
      sourcePos.x += (dx / distance) * force;
      sourcePos.y += (dy / distance) * force;
      targetPos.x -= (dx / distance) * force;
      targetPos.y -= (dy / distance) * force;
    });
    
    // 边界约束
    const padding = 50;
    positions.forEach(pos => {
      pos.x = Math.max(padding, Math.min(width - padding, pos.x));
      pos.y = Math.max(padding, Math.min(height - padding, pos.y));
    });
    
    // 每50次迭代发送一次进度更新
    if (i % 50 === 0) {
      self.postMessage({
        type: 'progress',
        iteration: i,
        total: iterations,
        positions: serializePositions(positions)
      });
    }
  }
  
  return positions;
}

/**
 * 序列化位置数据（转换为可传输格式）
 */
function serializePositions(positions: Map<string, NodePosition>): Record<string, { x: number; y: number }> {
  const result: Record<string, { x: number; y: number }> = {};
  positions.forEach((pos, id) => {
    result[id] = { x: pos.x, y: pos.y };
  });
  return result;
}

// 监听主线程消息
self.onmessage = (event: MessageEvent<LayoutMessage>) => {
  const { nodes, edges, width, height, iterations = 300 } = event.data;
  
  console.log(`Web Worker: 开始布局计算，节点数: ${nodes.length}, 边数: ${edges.length}`);
  
  const startTime = Date.now();
  
  // 计算布局
  const positions = forceLayout(nodes, edges, width, height, iterations);
  
  const duration = Date.now() - startTime;
  console.log(`Web Worker: 布局计算完成，耗时: ${duration}ms`);
  
  // 返回结果
  self.postMessage({
    type: 'complete',
    positions: serializePositions(positions),
    duration
  });
};

export {};
