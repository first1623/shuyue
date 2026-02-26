import React, { useMemo, useCallback, useState, useRef, useEffect } from 'react';
import { Spin, Empty } from 'antd';
import { GraphNode, GraphEdge } from '@/types/graph';
import { LODController, LODLevel } from './LODController';
import './VirtualGraph.css';

interface VirtualGraphProps {
  nodes: GraphNode[];
  edges: GraphEdge[];
  width: number;
  height: number;
  onNodeClick?: (nodeId: string) => void;
  loading?: boolean;
}

interface NodePosition {
  x: number;
  y: number;
  vx: number;
  vy: number;
}

const VirtualGraph: React.FC<VirtualGraphProps> = ({
  nodes,
  edges,
  width,
  height,
  onNodeClick,
  loading = false
}) => {
  // 视口状态
  const [viewport, setViewport] = useState({
    x: 0,
    y: 0,
    zoom: 1
  });
  
  // 节点位置管理
  const nodePositions = useRef<Map<string, NodePosition>>(new Map());
  
  // LOD控制器
  const lodController = useRef(new LODController());
  
  // 拖拽状态
  const [isDragging, setIsDragging] = useState(false);
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 });
  const [selectedNode, setSelectedNode] = useState<string | null>(null);
  
  // 初始化节点位置
  useEffect(() => {
    if (nodes.length === 0) return;
    
    // 使用圆形布局初始化
    const centerX = width / 2;
    const centerY = height / 2;
    const radius = Math.min(width, height) / 3;
    
    nodes.forEach((node, index) => {
      const angle = (2 * Math.PI * index) / nodes.length;
      nodePositions.current.set(node.id, {
        x: centerX + radius * Math.cos(angle),
        y: centerY + radius * Math.sin(angle),
        vx: 0,
        vy: 0
      });
    });
    
    // 触发一次简单布局（后续会用Web Worker优化）
    applyForceLayout();
  }, [nodes, width, height]);
  
  // 简化的力导向布局
  const applyForceLayout = useCallback(() => {
    if (nodes.length === 0) return;
    
    const positions = nodePositions.current;
    
    // 简单的力导向算法
    for (let i = 0; i < 50; i++) {
      // 斥力
      nodes.forEach(nodeA => {
        nodes.forEach(nodeB => {
          if (nodeA.id === nodeB.id) return;
          
          const posA = positions.get(nodeA.id);
          const posB = positions.get(nodeB.id);
          if (!posA || !posB) return;
          
          const dx = posA.x - posB.x;
          const dy = posA.y - posB.y;
          const distance = Math.sqrt(dx * dx + dy * dy);
          
          if (distance < 1) return;
          
          const force = 300 / (distance * distance);
          posA.x += (dx / distance) * force * 0.1;
          posA.y += (dy / distance) * force * 0.1;
        });
      });
      
      // 引力
      edges.forEach(edge => {
        const sourcePos = positions.get(edge.source);
        const targetPos = positions.get(edge.target);
        if (!sourcePos || !targetPos) return;
        
        const dx = targetPos.x - sourcePos.x;
        const dy = targetPos.y - sourcePos.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        if (distance < 1) return;
        
        const force = distance * 0.01;
        sourcePos.x += (dx / distance) * force;
        sourcePos.y += (dy / distance) * force;
        targetPos.x -= (dx / distance) * force;
        targetPos.y -= (dy / distance) * force;
      });
    }
  }, [nodes, edges]);
  
  // 计算可视区域节点
  const visibleNodes = useMemo(() => {
    const { x: vpX, y: vpY, zoom } = viewport;
    const visibleWidth = width / zoom;
    const visibleHeight = height / zoom;
    const buffer = 200; // 缓冲区
    
    return nodes.filter(node => {
      const pos = nodePositions.current.get(node.id);
      if (!pos) return false;
      
      // 判断节点是否在可视区域内
      return (
        pos.x >= vpX - buffer &&
        pos.x <= vpX + visibleWidth + buffer &&
        pos.y >= vpY - buffer &&
        pos.y <= vpY + visibleHeight + buffer
      );
    });
  }, [nodes, viewport, width, height]);
  
  // 计算可视边
  const visibleEdges = useMemo(() => {
    const visibleNodeIds = new Set(visibleNodes.map(n => n.id));
    return edges.filter(edge => 
      visibleNodeIds.has(edge.source) && visibleNodeIds.has(edge.target)
    );
  }, [edges, visibleNodes]);
  
  // 获取LOD级别
  const lodLevel = lodController.current.getLODLevel(viewport.zoom);
  
  // 处理鼠标滚轮缩放
  const handleWheel = useCallback((e: React.WheelEvent) => {
    e.preventDefault();
    
    const delta = e.deltaY > 0 ? 0.9 : 1.1;
    const newZoom = Math.max(0.1, Math.min(3, viewport.zoom * delta));
    
    // 以鼠标位置为中心缩放
    const rect = e.currentTarget?.getBoundingClientRect?.();
    if (!rect) return;
    const mouseX = e.clientX - rect.left;
    const mouseY = e.clientY - rect.top;
    
    const zoomRatio = newZoom / viewport.zoom;
    const newViewportX = mouseX - (mouseX - viewport.x) * zoomRatio;
    const newViewportY = mouseY - (mouseY - viewport.y) * zoomRatio;
    
    setViewport({
      x: newViewportX,
      y: newViewportY,
      zoom: newZoom
    });
  }, [viewport]);
  
  // 处理拖拽
  const handleMouseDown = useCallback((e: React.MouseEvent) => {
    if (e.button === 0) { // 左键
      setIsDragging(true);
      setDragStart({ x: e.clientX, y: e.clientY });
    }
  }, []);
  
  const handleMouseMove = useCallback((e: React.MouseEvent) => {
    if (!isDragging) return;
    
    const dx = e.clientX - dragStart.x;
    const dy = e.clientY - dragStart.y;
    
    setViewport(prev => ({
      ...prev,
      x: prev.x - dx / prev.zoom,
      y: prev.y - dy / prev.zoom
    }));
    
    setDragStart({ x: e.clientX, y: e.clientY });
  }, [isDragging, dragStart]);
  
  const handleMouseUp = useCallback(() => {
    setIsDragging(false);
  }, []);
  
  // 处理节点点击
  const handleNodeClick = useCallback((nodeId: string) => {
    setSelectedNode(nodeId);
    onNodeClick?.(nodeId);
  }, [onNodeClick]);
  
  // 重置视图
  const resetView = useCallback(() => {
    setViewport({ x: 0, y: 0, zoom: 1 });
    applyForceLayout();
  }, [applyForceLayout]);
  
  if (loading) {
    return (
      <div className="virtual-graph-container" style={{ width, height }}>
        <Spin tip="加载图谱数据..." />
      </div>
    );
  }
  
  if (nodes.length === 0) {
    return (
      <div className="virtual-graph-container" style={{ width, height }}>
        <Empty description="暂无图谱数据" />
      </div>
    );
  }
  
  return (
    <div
      className="virtual-graph-container"
      style={{
        width,
        height,
        cursor: isDragging ? 'grabbing' : 'grab',
        overflow: 'hidden',
        position: 'relative',
        backgroundColor: '#fafafa',
        border: '1px solid #e8e8e8',
        borderRadius: '4px'
      }}
      onWheel={handleWheel}
      onMouseDown={handleMouseDown}
      onMouseMove={handleMouseMove}
      onMouseUp={handleMouseUp}
      onMouseLeave={handleMouseUp}
    >
      {/* 性能统计 */}
      <div className="graph-stats" style={{
        position: 'absolute',
        top: 10,
        left: 10,
        zIndex: 10,
        backgroundColor: 'rgba(255, 255, 255, 0.9)',
        padding: '8px 12px',
        borderRadius: '4px',
        fontSize: '12px',
        boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
      }}>
        <div>总节点: {nodes.length}</div>
        <div>渲染节点: {visibleNodes.length}</div>
        <div>缩放: {(viewport.zoom * 100).toFixed(0)}%</div>
        <div>LOD: {lodLevel}</div>
      </div>
      
      {/* SVG层 - 渲染边 */}
      <svg
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%',
          pointerEvents: 'none'
        }}
      >
        <g transform={`translate(${-viewport.x * viewport.zoom}, ${-viewport.y * viewport.zoom}) scale(${viewport.zoom})`}>
          {lodController.current.shouldShowEdge(viewport.zoom) && visibleEdges.map(edge => {
            const sourcePos = nodePositions.current.get(edge.source);
            const targetPos = nodePositions.current.get(edge.target);
            if (!sourcePos || !targetPos) return null;
            
            return (
              <line
                key={edge.id}
                x1={sourcePos.x}
                y1={sourcePos.y}
                x2={targetPos.x}
                y2={targetPos.y}
                stroke="#d9d9d9"
                strokeWidth={1.5 / viewport.zoom}
                opacity={0.5}
              />
            );
          })}
        </g>
      </svg>
      
      {/* Canvas层 - 渲染节点 */}
      <canvas
        ref={canvasRef => {
          if (canvasRef) {
            const ctx = canvasRef.getContext('2d');
            if (ctx) {
              // 设置canvas尺寸
              canvasRef.width = width;
              canvasRef.height = height;
              
              // 清空画布
              ctx.clearRect(0, 0, width, height);
              
              // 应用变换
              ctx.save();
              ctx.translate(-viewport.x * viewport.zoom, -viewport.y * viewport.zoom);
              ctx.scale(viewport.zoom, viewport.zoom);
              
              // 绘制节点
              visibleNodes.forEach(node => {
                const pos = nodePositions.current.get(node.id);
                if (!pos) return;
                
                const nodeSize = lodController.current.getNodeSize(node, viewport.zoom);
                const isSelected = selectedNode === node.id;
                
                // 绘制节点圆形
                ctx.beginPath();
                ctx.arc(pos.x, pos.y, nodeSize, 0, 2 * Math.PI);
                ctx.fillStyle = getNodeColor(node.type);
                ctx.fill();
                
                if (isSelected) {
                  ctx.strokeStyle = '#1890ff';
                  ctx.lineWidth = 3 / viewport.zoom;
                  ctx.stroke();
                }
                
                // 绘制标签
                if (lodController.current.shouldShowLabel(viewport.zoom)) {
                  ctx.fillStyle = '#262626';
                  ctx.font = `${11 / viewport.zoom}px Arial`;
                  ctx.textAlign = 'center';
                  ctx.textBaseline = 'top';
                  
                  const label = node.label.length > 10 
                    ? node.label.substring(0, 10) + '...' 
                    : node.label;
                  ctx.fillText(label, pos.x, pos.y + nodeSize + 5 / viewport.zoom);
                }
              });
              
              ctx.restore();
            }
          }
        }}
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          pointerEvents: 'none'
        }}
      />
      
      {/* 交互层 - 处理节点点击 */}
      <div
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%'
        }}
        onClick={(e) => {
          const rect = e.currentTarget?.getBoundingClientRect?.();
          if (!rect) return;
          const mouseX = (e.clientX - rect.left + viewport.x * viewport.zoom) / viewport.zoom;
          const mouseY = (e.clientY - rect.top + viewport.y * viewport.zoom) / viewport.zoom;
          
          // 查找点击的节点
          for (const node of visibleNodes) {
            const pos = nodePositions.current.get(node.id);
            if (!pos) continue;
            
            const distance = Math.sqrt(
              Math.pow(mouseX - pos.x, 2) + Math.pow(mouseY - pos.y, 2)
            );
            
            const nodeSize = lodController.current.getNodeSize(node, viewport.zoom);
            if (distance <= nodeSize) {
              handleNodeClick(node.id);
              break;
            }
          }
        }}
      />
    </div>
  );
};

// 辅助函数：获取节点颜色
function getNodeColor(type: string): string {
  const colors: Record<string, string> = {
    document: '#1890ff',
    theory: '#722ed1',
    author: '#13c2c2',
    entity: '#fa8c16',
  };
  return colors[type] || '#1890ff';
}

export default VirtualGraph;
