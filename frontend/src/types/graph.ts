/**
 * 图谱数据类型定义
 */

export interface GraphNode {
  id: string;
  type: string;
  label: string;
  size: number;
  properties: Record<string, any>;
}

export interface GraphEdge {
  id: string;
  source: string;
  target: string;
  type: string;
  label: string;
}

export interface GraphData {
  dimension: string;
  nodes: GraphNode[];
  edges: GraphEdge[];
  stats: {
    node_count: number;
    edge_count: number;
    doc_count: number;
  };
}

export interface NodeDetail {
  node_id: string;
  node_type: string;
  info: Record<string, any>;
  related_documents: Array<{
    file_id: number;
    file_name: string;
    abstract: string;
    keywords: string[];
  }>;
}

export interface GraphStats {
  total_documents: number;
  theory_count: number;
  author_count: number;
  entity_count: number;
  dimension_stats: Record<string, { name: string; count: number; description: string }>;
}
