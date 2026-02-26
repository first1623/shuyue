#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
学习平台知识图谱系统 - FastAPI 应用
"""
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Optional

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.core.config import settings
from app.core.database import SessionLocal
from app.models.data_overview import DataOverview, DataBookDetail
from app.utils.document_parser import DocumentParser

# 创建 FastAPI 应用
app = FastAPI(
    title="学习平台知识图谱系统 API",
    description="基于 DeepSeek AI 的智能文档解析与知识图谱系统",
    version="1.0.0"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化文档解析器
parser = DocumentParser()


# ==================== Pydantic 模型 ====================

class DocumentParseRequest(BaseModel):
    """文档解析请求"""
    file_path: str
    file_id: int


class DocumentResponse(BaseModel):
    """文档响应"""
    id: int
    file_name: str
    file_path: str
    file_type: str
    file_size: Optional[int] = None
    parse_status: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class DocumentDetailResponse(BaseModel):
    """文档详情响应"""
    id: int
    file_id: int
    abstract: Optional[str] = None
    keywords: Optional[List[str]] = None
    theories: Optional[List[str]] = None
    experiment_flow: Optional[str] = None
    statistical_methods: Optional[List[str]] = None
    conclusion: Optional[str] = None
    parse_status: Optional[str] = None
    parse_time: Optional[datetime] = None
    confidence_score: Optional[float] = None


class FolderScanRequest(BaseModel):
    """文件夹扫描请求"""
    folder_path: str
    recursive: bool = True


class ScanResult(BaseModel):
    """扫描结果"""
    total_files: int
    scanned_files: int
    parsed_files: int
    errors: List[str]


# ==================== API 接口 ====================

@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "学习平台知识图谱系统 API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "database": "connected"
    }


@app.post("/api/v1/documents/parse")
async def parse_document(request: DocumentParseRequest, background_tasks: BackgroundTasks):
    """
    解析单个文档
    
    - **file_path**: 文档的完整路径
    - **file_id**: 文件 ID（用于数据库关联）
    """
    try:
        file_path = Path(request.file_path)
        if not file_path.exists():
            raise HTTPException(status_code=404, detail=f"文件不存在: {request.file_path}")
        
        # 同步解析（快速返回）
        result = parser.parse_document(str(file_path), request.file_id)
        
        return {
            "status": "success",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"解析失败: {str(e)}")


@app.post("/api/v1/folders/scan", response_model=ScanResult)
async def scan_folder(request: FolderScanRequest, background_tasks: BackgroundTasks):
    """
    扫描文件夹并解析所有文档
    
    - **folder_path**: 要扫描的文件夹路径
    - **recursive**: 是否递归扫描子文件夹
    """
    try:
        folder_path = Path(request.folder_path)
        if not folder_path.exists():
            raise HTTPException(status_code=404, detail=f"文件夹不存在: {request.folder_path}")
        
        db = SessionLocal()
        results = ScanResult(total_files=0, scanned_files=0, parsed_files=0, errors=[])
        
        try:
            # 扫描文件
            if request.recursive:
                files = list(folder_path.rglob("*"))
            else:
                files = list(folder_path.glob("*"))
            
            # 过滤支持的格式
            supported_extensions = {'.pdf', '.docx', '.txt', '.md'}
            document_files = [f for f in files if f.is_file() and f.suffix.lower() in supported_extensions]
            
            results.total_files = len(document_files)
            
            # 解析每个文件
            for idx, file_path in enumerate(document_files):
                try:
                    # 创建或更新文件记录
                    existing = db.query(DataOverview).filter(
                        DataOverview.file_path == str(file_path)
                    ).first()
                    
                    if existing:
                        file_record = existing
                    else:
                        file_record = DataOverview(
                            file_name=file_path.name,
                            file_path=str(file_path),
                            file_type="file",
                            file_size=file_path.stat().st_size,
                            file_extension=file_path.suffix.lower()
                        )
                        db.add(file_record)
                        db.commit()
                        db.refresh(file_record)
                    
                    # 解析文档
                    parser.parse_document(str(file_path), file_record.id)
                    
                    results.scanned_files += 1
                    results.parsed_files += 1
                    
                except Exception as e:
                    results.errors.append(f"{file_path.name}: {str(e)}")
            
            return results
            
        finally:
            db.close()
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"扫描失败: {str(e)}")


@app.get("/api/v1/documents", response_model=List[DocumentResponse])
async def list_documents(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    file_type: Optional[str] = None
):
    """
    获取文档列表
    
    - **skip**: 跳过的记录数
    - **limit**: 返回的最大记录数
    - **file_type**: 按文件类型过滤（folder/file）
    """
    db = SessionLocal()
    try:
        query = db.query(DataOverview)
        
        if file_type:
            query = query.filter(DataOverview.file_type == file_type)
        
        documents = query.offset(skip).limit(limit).all()
        
        return [
            DocumentResponse(
                id=doc.id,
                file_name=doc.file_name,
                file_path=doc.file_path,
                file_type=doc.file_type,
                file_size=doc.file_size,
                parse_status=db.query(DataBookDetail).filter(
                    DataBookDetail.file_id == doc.id
                ).first().parse_status if db.query(DataBookDetail).filter(
                    DataBookDetail.file_id == doc.id
                ).first() else None,
                created_at=doc.created_at,
                updated_at=doc.updated_at
            )
            for doc in documents
        ]
    finally:
        db.close()


@app.get("/api/v1/documents/{document_id}", response_model=DocumentDetailResponse)
async def get_document_detail(document_id: int):
    """
    获取文档详情
    
    - **document_id**: 文档 ID
    """
    db = SessionLocal()
    try:
        # 查询文档详情
        detail = db.query(DataBookDetail).filter(
            DataBookDetail.file_id == document_id
        ).first()
        
        if not detail:
            raise HTTPException(status_code=404, detail="文档详情不存在")
        
        # 提取置信度
        confidence_score = None
        if detail.deepseek_response:
            confidence_score = detail.deepseek_response.get('confidence_score')
        
        return DocumentDetailResponse(
            id=detail.id,
            file_id=detail.file_id,
            abstract=detail.abstract,
            keywords=detail.keywords,
            theories=detail.theories,
            experiment_flow=detail.experiment_flow,
            statistical_methods=detail.statistical_methods,
            conclusion=detail.conclusion,
            parse_status=detail.parse_status,
            parse_time=detail.parse_time,
            confidence_score=confidence_score
        )
    finally:
        db.close()


@app.get("/api/v1/search")
async def search_documents(
    q: str = Query(..., min_length=1),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100)
):
    """
    搜索文档
    
    - **q**: 搜索关键词
    - **skip**: 跳过的记录数
    - **limit**: 返回的最大记录数
    """
    db = SessionLocal()
    try:
        # 搜索摘要、关键词、结论
        results = db.query(DataBookDetail).filter(
            (DataBookDetail.abstract.contains(q)) |
            (DataBookDetail.conclusion.contains(q)) |
            (DataBookDetail.keywords.contains(q))
        ).offset(skip).limit(limit).all()
        
        return {
            "query": q,
            "total": len(results),
            "results": [
                {
                    "file_id": r.file_id,
                    "abstract": r.abstract,
                    "keywords": r.keywords,
                    "conclusion": r.conclusion,
                    "parse_time": r.parse_time.isoformat() if r.parse_time else None
                }
                for r in results
            ]
        }
    finally:
        db.close()


@app.get("/api/v1/system/stats")
async def get_system_stats():
    """
    获取系统统计信息
    """
    db = SessionLocal()
    try:
        total_files = db.query(DataOverview).filter(
            DataOverview.file_type == "file"
        ).count()
        
        parsed_files = db.query(DataBookDetail).filter(
            DataBookDetail.parse_status == "completed"
        ).count()
        
        failed_files = db.query(DataBookDetail).filter(
            DataBookDetail.parse_status == "failed"
        ).count()
        
        return {
            "total_files": total_files,
            "parsed_files": parsed_files,
            "failed_files": failed_files,
            "parse_rate": round(parsed_files / total_files * 100, 2) if total_files > 0 else 0
        }
    finally:
        db.close()


# ==================== 三维度图谱API ====================

@app.get("/api/v1/graph/dimension/{dimension}")
async def get_graph_by_dimension(dimension: str):
    """
    获取三维度图谱数据
    
    - **dimension**: 维度类型 (theory/author/entity)
    - 返回对应维度的图谱数据（节点+边）
    """
    if dimension not in ['theory', 'author', 'entity']:
        raise HTTPException(status_code=400, detail="维度必须是 theory/author/entity 之一")
    
    db = SessionLocal()
    try:
        # 获取所有已解析的文档
        documents = db.query(DataBookDetail).filter(
            DataBookDetail.parse_status == "completed"
        ).all()
        
        nodes = []
        edges = []
        node_id_counter = 1
        edge_id_counter = 1
        
        # 用于去重的集合
        seen_nodes = {}
        doc_nodes = {}
        
        # 先创建文档节点
        for doc in documents:
            file_info = db.query(DataOverview).filter(DataOverview.id == doc.file_id).first()
            if file_info:
                doc_node_id = f"doc_{doc.file_id}"
                doc_nodes[doc.file_id] = doc_node_id
                nodes.append({
                    "id": doc_node_id,
                    "type": "document",
                    "label": file_info.file_name[:30],
                    "size": 20,
                    "properties": {
                        "file_id": doc.file_id,
                        "file_name": file_info.file_name,
                        "abstract": doc.abstract[:100] if doc.abstract else ""
                    }
                })
        
        if dimension == 'theory':
            # 按理论维度构建图谱
            for doc in documents:
                theories = doc.theories_used or []
                if isinstance(theories, str):
                    try:
                        theories = eval(theories)
                    except:
                        theories = []
                
                for theory in theories:
                    if isinstance(theory, dict):
                        theory_name = theory.get('name', '')
                        theory_desc = theory.get('description', '')
                    else:
                        theory_name = str(theory)
                        theory_desc = ''
                    
                    if theory_name:
                        # 创建或获取理论节点
                        if theory_name not in seen_nodes:
                            theory_node_id = f"theory_{node_id_counter}"
                            seen_nodes[theory_name] = theory_node_id
                            node_id_counter += 1
                            nodes.append({
                                "id": theory_node_id,
                                "type": "theory",
                                "label": theory_name,
                                "size": 30,
                                "properties": {
                                    "name": theory_name,
                                    "description": theory_desc
                                }
                            })
                        else:
                            theory_node_id = seen_nodes[theory_name]
                        
                        # 创建文档-理论关系
                        if doc.file_id in doc_nodes:
                            edges.append({
                                "id": f"edge_{edge_id_counter}",
                                "source": doc_nodes[doc.file_id],
                                "target": theory_node_id,
                                "type": "USES_THEORY",
                                "label": "使用"
                            })
                            edge_id_counter += 1
        
        elif dimension == 'author':
            # 按作者维度构建图谱
            author_docs = {}  # 作者名 -> 文档列表
            
            for doc in documents:
                authors = doc.authors or []
                if isinstance(authors, str):
                    try:
                        authors = eval(authors)
                    except:
                        authors = []
                
                for author_name in authors:
                    if author_name:
                        if author_name not in author_docs:
                            author_docs[author_name] = []
                        author_docs[author_name].append(doc.file_id)
            
            # 创建作者节点和关系
            for author_name, doc_ids in author_docs.items():
                if author_name not in seen_nodes:
                    author_node_id = f"author_{node_id_counter}"
                    seen_nodes[author_name] = author_node_id
                    node_id_counter += 1
                    nodes.append({
                        "id": author_node_id,
                        "type": "author",
                        "label": author_name,
                        "size": 25 + len(doc_ids) * 5,
                        "properties": {
                            "name": author_name,
                            "doc_count": len(doc_ids)
                        }
                    })
                else:
                    author_node_id = seen_nodes[author_name]
                
                # 创建作者-文档关系
                for doc_id in doc_ids:
                    if doc_id in doc_nodes:
                        edges.append({
                            "id": f"edge_{edge_id_counter}",
                            "source": author_node_id,
                            "target": doc_nodes[doc_id],
                            "type": "AUTHORED",
                            "label": "撰写"
                        })
                        edge_id_counter += 1
        
        elif dimension == 'entity':
            # 按实体词维度构建图谱
            entity_docs = {}  # 实体名 -> 文档列表
            
            for doc in documents:
                entities = doc.entities or []
                if isinstance(entities, str):
                    try:
                        entities = eval(entities)
                    except:
                        entities = []
                
                for entity in entities:
                    if isinstance(entity, dict):
                        entity_name = entity.get('name', '')
                        entity_type = entity.get('type', '术语')
                        entity_freq = entity.get('frequency', 1)
                    else:
                        entity_name = str(entity)
                        entity_type = '术语'
                        entity_freq = 1
                    
                    if entity_name:
                        key = f"{entity_name}_{entity_type}"
                        if key not in entity_docs:
                            entity_docs[key] = {
                                'name': entity_name,
                                'type': entity_type,
                                'frequency': entity_freq,
                                'doc_ids': []
                            }
                        entity_docs[key]['doc_ids'].append(doc.file_id)
                        entity_docs[key]['frequency'] += entity_freq
            
            # 创建实体节点和关系
            for key, entity_data in entity_docs.items():
                entity_name = entity_data['name']
                entity_type = entity_data['type']
                
                if entity_name not in seen_nodes:
                    entity_node_id = f"entity_{node_id_counter}"
                    seen_nodes[entity_name] = entity_node_id
                    node_id_counter += 1
                    nodes.append({
                        "id": entity_node_id,
                        "type": "entity",
                        "label": entity_name,
                        "size": 15 + entity_data['frequency'] * 2,
                        "properties": {
                            "name": entity_name,
                            "entity_type": entity_type,
                            "frequency": entity_data['frequency'],
                            "doc_count": len(entity_data['doc_ids'])
                        }
                    })
                else:
                    entity_node_id = seen_nodes[entity_name]
                
                # 创建实体-文档关系
                for doc_id in entity_data['doc_ids']:
                    if doc_id in doc_nodes:
                        edges.append({
                            "id": f"edge_{edge_id_counter}",
                            "source": entity_node_id,
                            "target": doc_nodes[doc_id],
                            "type": "APPEARS_IN",
                            "label": "出现于"
                        })
                        edge_id_counter += 1
        
        return {
            "dimension": dimension,
            "nodes": nodes,
            "edges": edges,
            "stats": {
                "node_count": len(nodes),
                "edge_count": len(edges),
                "doc_count": len(doc_nodes)
            }
        }
    
    finally:
        db.close()


@app.get("/api/v1/graph/node/{node_id}/detail")
async def get_node_detail(node_id: str):
    """
    获取节点详情
    
    - **node_id**: 节点ID（如 doc_1, theory_1, author_1, entity_1）
    - 返回节点详细信息和关联文档列表
    """
    db = SessionLocal()
    try:
        node_type, record_id = node_id.split('_', 1)
        
        result = {
            "node_id": node_id,
            "node_type": node_type,
            "info": {},
            "related_documents": []
        }
        
        if node_type == 'doc':
            # 文档节点详情
            doc_id = int(record_id)
            doc = db.query(DataBookDetail).filter(DataBookDetail.file_id == doc_id).first()
            file_info = db.query(DataOverview).filter(DataOverview.id == doc_id).first()
            
            if doc and file_info:
                result["info"] = {
                    "file_name": file_info.file_name,
                    "file_path": file_info.file_path,
                    "abstract": doc.abstract,
                    "keywords": doc.keywords,
                    "authors": doc.authors,
                    "theories_used": doc.theories_used,
                    "entities": doc.entities,
                    "parse_status": doc.parse_status,
                    "parse_time": doc.parse_time.isoformat() if doc.parse_time else None
                }
        
        elif node_type in ['theory', 'author', 'entity']:
            # 查找所有包含该节点的文档
            documents = db.query(DataBookDetail).filter(
                DataBookDetail.parse_status == "completed"
            ).all()
            
            for doc in documents:
                file_info = db.query(DataOverview).filter(DataOverview.id == doc.file_id).first()
                if not file_info:
                    continue
                
                is_related = False
                
                if node_type == 'theory':
                    theories = doc.theories_used or []
                    if isinstance(theories, str):
                        try:
                            theories = eval(theories)
                        except:
                            theories = []
                    for t in theories:
                        if isinstance(t, dict) and t.get('name') == record_id:
                            is_related = True
                            break
                        elif str(t) == record_id:
                            is_related = True
                            break
                
                elif node_type == 'author':
                    authors = doc.authors or []
                    if isinstance(authors, str):
                        try:
                            authors = eval(authors)
                        except:
                            authors = []
                    if record_id in authors:
                        is_related = True
                
                elif node_type == 'entity':
                    entities = doc.entities or []
                    if isinstance(entities, str):
                        try:
                            entities = eval(entities)
                        except:
                            entities = []
                    for e in entities:
                        if isinstance(e, dict) and e.get('name') == record_id:
                            is_related = True
                            break
                
                if is_related:
                    result["related_documents"].append({
                        "file_id": doc.file_id,
                        "file_name": file_info.file_name,
                        "abstract": doc.abstract[:100] if doc.abstract else "",
                        "keywords": doc.keywords[:5] if doc.keywords else []
                    })
            
            # 设置节点信息
            if node_type == 'theory':
                result["info"] = {
                    "name": record_id,
                    "doc_count": len(result["related_documents"])
                }
            elif node_type == 'author':
                result["info"] = {
                    "name": record_id,
                    "doc_count": len(result["related_documents"])
                }
            elif node_type == 'entity':
                result["info"] = {
                    "name": record_id,
                    "doc_count": len(result["related_documents"])
                }
        
        return result
    
    finally:
        db.close()


@app.get("/api/v1/graph/stats")
async def get_graph_stats():
    """
    获取图谱统计信息
    """
    db = SessionLocal()
    try:
        documents = db.query(DataBookDetail).filter(
            DataBookDetail.parse_status == "completed"
        ).all()
        
        # 统计各维度数据
        theory_count = 0
        author_count = 0
        entity_count = 0
        
        theory_set = set()
        author_set = set()
        entity_set = set()
        
        for doc in documents:
            # 理论统计
            theories = doc.theories_used or []
            if isinstance(theories, str):
                try:
                    theories = eval(theories)
                except:
                    theories = []
            for t in theories:
                if isinstance(t, dict):
                    theory_set.add(t.get('name', ''))
                else:
                    theory_set.add(str(t))
            
            # 作者统计
            authors = doc.authors or []
            if isinstance(authors, str):
                try:
                    authors = eval(authors)
                except:
                    authors = []
            author_set.update(authors)
            
            # 实体统计
            entities = doc.entities or []
            if isinstance(entities, str):
                try:
                    entities = eval(entities)
                except:
                    entities = []
            for e in entities:
                if isinstance(e, dict):
                    entity_set.add(e.get('name', ''))
                else:
                    entity_set.add(str(e))
        
        return {
            "total_documents": len(documents),
            "theory_count": len(theory_set),
            "author_count": len(author_set),
            "entity_count": len(entity_set),
            "dimension_stats": {
                "theory": {
                    "name": "按理论",
                    "count": len(theory_set),
                    "description": "文档引用的理论和框架"
                },
                "author": {
                    "name": "按作者",
                    "count": len(author_set),
                    "description": "文档作者分布"
                },
                "entity": {
                    "name": "按实体词",
                    "count": len(entity_set),
                    "description": "提取的术语和概念"
                }
            }
        }
    
    finally:
        db.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
