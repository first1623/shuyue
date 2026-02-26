import os
import re
import json
import ast
from typing import Dict, List, Any, Tuple, Optional
from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class FunctionalPoint:
    id: str
    level: int  # 1=primary, 2=secondary, 3=tertiary
    name: str
    description: str
    parent_id: Optional[str] = None
    children_ids: List[str] = None
    related_files: List[str] = None
    
    def __post_init__(self):
        if self.children_ids is None:
            self.children_ids = []
        if self.related_files is None:
            self.related_files = []

@dataclass
class RequirementDetail:
    functional_point_id: str
    requirement_description: str
    system_invocation_method: str
    data_sources: List[str]
    api_endpoints: List[str] = None
    database_tables: List[str] = None
    external_services: List[str] = None
    user_interactions: List[str] = None
    
    def __post_init__(self):
        if self.api_endpoints is None:
            self.api_endpoints = []
        if self.database_tables is None:
            self.database_tables = []
        if self.external_services is None:
            self.external_services = []
        if self.user_interactions is None:
            self.user_interactions = []

class ProjectAnalyzer:
    """项目分析器 - 自动生成需求列表"""
    
    def __init__(self, project_path: str = "."):
        self.project_path = Path(project_path)
        self.functional_points: Dict[str, FunctionalPoint] = {}
        self.requirements: Dict[str, RequirementDetail] = {}
        self.project_structure = {}
        self.code_analysis = {}
        self.config_analysis = {}
        
    async def analyze_project_structure(self) -> Dict:
        """分析项目结构"""
        print("🔍 分析项目结构...")
        
        structure = {
            'directories': [],
            'files_by_type': {},
            'entry_points': [],
            'config_files': [],
            'documentation': [],
            'tests': []
        }
        
        # 扫描目录结构
        for root, dirs, files in os.walk(self.project_path):
            # 跳过常见非业务目录
            dirs[:] = [d for d in dirs if d not in ['node_modules', '.git', '__pycache__', 'venv', '.venv', 'dist', 'build', '.pytest_cache']]
            
            rel_root = os.path.relpath(root, self.project_path)
            if rel_root != '.':
                structure['directories'].append(rel_root)
            
            for file in files:
                file_path = Path(root) / file
                rel_path = os.path.relpath(file_path, self.project_path)
                
                # 按文件类型分类
                suffix = file_path.suffix.lower()
                if suffix not in structure['files_by_type']:
                    structure['files_by_type'][suffix] = []
                structure['files_by_type'][suffix].append(rel_path)
                
                # 识别关键文件类型
                if file.lower() in ['main.py', 'app.py', 'index.js', 'server.js', 'manage.py']:
                    structure['entry_points'].append(rel_path)
                elif suffix in ['.json', '.yaml', '.yml', '.toml', '.ini', '.cfg']:
                    structure['config_files'].append(rel_path)
                elif 'readme' in file.lower() or file.endswith('.md'):
                    structure['documentation'].append(rel_path)
                elif 'test' in file.lower() or 'spec' in file.lower():
                    structure['tests'].append(rel_path)
        
        self.project_structure = structure
        return structure
    
    async def extract_functional_modules(self) -> Dict[str, List[str]]:
        """提取功能模块"""
        print("📊 提取功能模块...")
        
        functional_modules = {
            'core_business': [],
            'api_services': [],
            'data_processing': [],
            'user_interface': [],
            'integration': [],
            'utilities': [],
            'configuration': []
        }
        
        # 基于目录结构推断功能模块
        directories = self.project_structure['directories']
        
        for directory in directories:
            dir_lower = directory.lower()
            
            if any(keyword in dir_lower for keyword in ['api', 'service', 'endpoint']):
                functional_modules['api_services'].append(directory)
            elif any(keyword in dir_lower for keyword in ['model', 'entity', 'business', 'core']):
                functional_modules['core_business'].append(directory)
            elif any(keyword in dir_lower for keyword in ['view', 'template', 'static', 'frontend', 'ui']):
                functional_modules['user_interface'].append(directory)
            elif any(keyword in dir_lower for keyword in ['processor', 'handler', 'worker', 'job']):
                functional_modules['data_processing'].append(directory)
            elif any(keyword in dir_lower for keyword in ['integration', 'external', 'third', 'client']):
                functional_modules['integration'].append(directory)
            elif any(keyword in dir_lower for keyword in ['util', 'helper', 'common', 'shared']):
                functional_modules['utilities'].append(directory)
            elif any(keyword in dir_lower for keyword in ['config', 'setting', 'env']):
                functional_modules['configuration'].append(directory)
        
        # 基于文件命名模式进一步分析
        for file_type, files in self.project_structure['files_by_type'].items():
            if file_type in ['.py', '.js', '.java', '.cpp']:
                for file_path in files:
                    file_lower = file_path.lower()
                    
                    if any(pattern in file_lower for pattern in ['api', 'service', 'controller']):
                        functional_modules['api_services'].append(file_path)
                    elif any(pattern in file_lower for pattern in ['model', 'entity', 'business']):
                        functional_modules['core_business'].append(file_path)
                    elif any(pattern in file_lower for pattern in ['view', 'component', 'page']):
                        functional_modules['user_interface'].append(file_path)
                    elif any(pattern in file_lower for pattern in ['process', 'handle', 'transform']):
                        functional_modules['data_processing'].append(file_path)
        
        # 去重
        for key in functional_modules:
            functional_modules[key] = list(set(functional_modules[key]))
        
        self.code_analysis['functional_modules'] = functional_modules
        return functional_modules
    
    async def decompose_functional_hierarchy(self) -> Dict[str, FunctionalPoint]:
        """分解功能层级"""
        print("🏗️ 构建功能层级结构...")
        
        # 一级功能点（主要业务域）
        primary_functions = [
            ('USER_MANAGEMENT', '用户管理', '系统的用户注册、登录、权限管理等核心功能'),
            ('CONTENT_MANAGEMENT', '内容管理', '内容的创建、编辑、发布、审核等管理功能'),
            ('DATA_PROCESSING', '数据处理', '数据的采集、清洗、分析、存储等处理功能'),
            ('INTEGRATION_SERVICE', '集成服务', '与外部系统的集成和数据交换功能'),
            ('REPORT_ANALYTICS', '报表分析', '数据统计、报表生成、分析洞察功能'),
            ('SYSTEM_ADMIN', '系统管理', '系统配置、监控、维护等管理功能')
        ]
        
        primary_points = {}
        for func_id, name, desc in primary_functions:
            point = FunctionalPoint(
                id=func_id,
                level=1,
                name=name,
                description=desc,
                children_ids=[]
            )
            primary_points[func_id] = point
            self.functional_points[func_id] = point
        
        # 基于项目实际情况调整一级功能点
        modules = self.code_analysis.get('functional_modules', {})
        
        if modules.get('api_services'):
            if 'SERVICE_LAYER' not in primary_points:
                primary_points['SERVICE_LAYER'] = FunctionalPoint(
                    id='SERVICE_LAYER',
                    level=1,
                    name='服务层',
                    description='提供API服务和业务逻辑处理的核心服务层'
                )
                self.functional_points['SERVICE_LAYER'] = primary_points['SERVICE_LAYER']
        
        if modules.get('user_interface'):
            primary_points['USER_MANAGEMENT'].description += '，包括前端界面交互功能'
        
        # 二级功能点（子系统）- 根据项目特点动态生成
        secondary_mapping = {
            'USER_MANAGEMENT': [
                ('AUTH_LOGIN', '身份认证', '用户登录、登出、会话管理'),
                ('USER_REGISTRY', '用户注册', '新用户注册、信息完善'),
                ('PERMISSION_CTRL', '权限控制', '角色管理、权限分配'),
                ('PROFILE_MANAGE', '档案管理', '用户信息管理、偏好设置')
            ],
            'CONTENT_MANAGEMENT': [
                ('CONTENT_CREATE', '内容创建', '新建各类业务内容'),
                ('CONTENT_EDIT', '内容编辑', '修改和更新现有内容'),
                ('CONTENT_REVIEW', '内容审核', '内容质量检查和发布控制'),
                ('CONTENT_PUBLISH', '内容发布', '多渠道内容发布和推广')
            ],
            'DATA_PROCESSING': [
                ('DATA_COLLECTION', '数据采集', '从多源收集业务数据'),
                ('DATA_CLEANING', '数据清洗', '数据质量处理和标准化'),
                ('DATA_ANALYSIS', '数据分析', '业务数据分析和挖掘'),
                ('DATA_STORAGE', '数据存储', '数据持久化和备份管理')
            ],
            'SERVICE_LAYER': [
                ('API_GATEWAY', 'API网关', '统一API入口和路由管理'),
                ('BUSINESS_LOGIC', '业务逻辑', '核心业务规则和流程处理'),
                ('EXTERNAL_API', '外部API', '第三方服务集成和调用'),
                ('DATA_SERVICE', '数据服务', '数据访问和业务数据提供')
            ]
        }
        
        for primary_id, primary_point in primary_points.items():
            if primary_id in secondary_mapping:
                for sec_id, sec_name, sec_desc in secondary_mapping[primary_id]:
                    secondary_point = FunctionalPoint(
                        id=sec_id,
                        level=2,
                        name=sec_name,
                        description=sec_desc,
                        parent_id=primary_id,
                        children_ids=[]
                    )
                    primary_point.children_ids.append(sec_id)
                    self.functional_points[sec_id] = secondary_point
        
        # 三级功能点（具体操作）- 基于代码文件生成
        await self._generate_tertiary_functions()
        
        return self.functional_points
    
    async def _generate_tertiary_functions(self):
        """生成三级功能点"""
        # 基于发现的文件生成三级功能点
        files_by_category = self.code_analysis.get('functional_modules', {})
        
        # 为每个二级功能点生成对应的三级功能点
        for func_id, func_point in self.functional_points.items():
            if func_point.level == 2:
                tertiary_functions = await self._infer_tertiary_from_files(func_point, files_by_category)
                
                for tert_id, tert_name, tert_desc, related_files in tertiary_functions:
                    tertiary_point = FunctionalPoint(
                        id=tert_id,
                        level=3,
                        name=tert_name,
                        description=tert_desc,
                        parent_id=func_id,
                        related_files=related_files
                    )
                    func_point.children_ids.append(tert_id)
                    self.functional_points[tert_id] = tertiary_point
    
    async def _infer_tertiary_from_files(self, parent_func: FunctionalPoint, 
                                       files_by_category: Dict) -> List[Tuple]:
        """基于文件推断三级功能点"""
        tertiary_functions = []
        
        # 根据父功能点的名称推断相关的三级功能
        parent_name = parent_func.name.lower()
        
        if '认证' in parent_name or 'login' in parent_name:
            tertiary_functions.extend([
                ('AUTH_PASSWORD_LOGIN', '密码登录', '用户使用用户名密码进行身份验证', []),
                ('AUTH_TOKEN_VALIDATE', '令牌验证', '验证JWT或Session令牌的有效性', []),
                ('AUTH_LOGOUT', '用户登出', '清除用户会话和令牌信息', [])
            ])
        
        elif '内容创建' in parent_name or 'create' in parent_name:
            tertiary_functions.extend([
                ('CREATE_DRAFT', '创建草稿', '创建未发布的内容草稿', []),
                ('CREATE_TEMPLATE', '使用模板', '基于预设模板创建内容', []),
                ('CREATE_MEDIA_UPLOAD', '媒体上传', '上传图片、视频等媒体文件', [])
            ])
        
        elif '数据采集' in parent_name or 'collection' in parent_name:
            tertiary_functions.extend([
                ('COLLECT_API_DATA', 'API数据采集', '通过REST API获取外部数据', []),
                ('COLLECT_FILE_IMPORT', '文件导入', '从CSV、Excel等文件导入数据', []),
                ('COLLECT_USER_INPUT', '用户输入采集', '收集用户在界面的输入数据', [])
            ])
        
        elif 'api' in parent_name or 'API' in parent_name:
            tertiary_functions.extend([
                ('API_REQUEST_ROUTE', '请求路由', '根据URL路径路由到对应处理逻辑', []),
                ('API_PARAMETER_VALIDATE', '参数验证', '验证请求参数的格式和有效性', []),
                ('API_RESPONSE_FORMAT', '响应格式化', '统一API响应格式和数据结构', [])
            ])
        
        # 基于实际文件补充三级功能点
        related_files = []
        for category, files in files_by_category.items():
            if any(keyword in parent_name for keyword in category.lower().split('_')):
                related_files.extend(files[:3])  # 取前3个文件作为关联
        
        if related_files and not tertiary_functions:
            # 如果没有推断出特定功能，基于文件创建通用功能点
            for i, file_path in enumerate(related_files[:3]):
                file_name = Path(file_path).stem
                tertiary_functions.append((
                    f'{parent_func.id}_OP_{i+1}',
                    f'{file_name}操作',
                    f'处理{file_name}相关的业务逻辑',
                    [file_path]
                ))
        
        return tertiary_functions
    
    async def generate_requirement_descriptions(self) -> Dict[str, RequirementDetail]:
        """生成需求描述"""
        print("📝 生成需求描述...")
        
        for func_id, func_point in self.functional_points.items():
            requirement = RequirementDetail(
                functional_point_id=func_id,
                requirement_description=await self._generate_detailed_requirement(func_point),
                system_invocation_method=await self._define_system_invocation(func_point),
                data_sources=await self._identify_data_sources(func_point),
                api_endpoints=await self._identify_api_endpoints(func_point),
                database_tables=await self._identify_database_tables(func_point),
                external_services=await self._identify_external_services(func_point),
                user_interactions=await self._identify_user_interactions(func_point)
            )
            self.requirements[func_id] = requirement
        
        return self.requirements
    
    async def _generate_detailed_requirement(self, func_point: FunctionalPoint) -> str:
        """生成详细需求描述"""
        base_desc = func_point.description
        
        if func_point.level == 1:
            return f"作为系统的主要功能域，{base_desc}。该功能域应该提供完整的业务流程支持，具备高可用性、可扩展性和安全性保障，能够满足用户的核心业务需求。"
        
        elif func_point.level == 2:
            parent_desc = self.functional_points.get(func_point.parent_id, FunctionalPoint('','', '')).description
            return f"在{parent_desc}范围内，{base_desc}。该功能应该与同层级的其他功能协调工作，提供稳定可靠的服务接口，支持并发访问和错误处理。"
        
        else:  # level == 3
            parent_func = self.functional_points.get(func_point.parent_id)
            if parent_func:
                parent_parent = self.functional_points.get(parent_func.parent_id)
                context = f"在{parent_parent.name}的{parent_func.name}功能下" if parent_parent else f"在{parent_func.name}功能下"
                return f"{context}，{base_desc}。该操作应该是原子性的，提供明确的输入输出规范，具备完善的异常处理和日志记录机制。"
        
        return base_desc
    
    async def _define_system_invocation(self, func_point: FunctionalPoint) -> str:
        """定义系统调用方式"""
        if func_point.level == 1:
            return "通过统一的业务门面（Business Facade）或服务定位器（Service Locator）模式进行调用，支持同步和异步调用方式，提供负载均衡和故障转移机制。"
        
        elif func_point.level == 2:
            return "通过RESTful API或RPC接口调用，支持HTTP/HTTPS协议，提供标准化的请求/响应格式，包含认证授权、参数校验、限流控制等企业级特性。"
        
        else:
            related_files = func_point.related_files
            if related_files:
                file_refs = ', '.join([Path(f).stem for f in related_files[:2]])
                return f"通过调用{file_refs}模块中的具体函数或服务方法实现，采用面向对象或函数式编程范式，支持单元测试和Mock测试。"
            else:
                return "通过内部服务调用或消息队列异步处理，确保操作的幂等性和事务一致性，提供详细的执行状态反馈。"
    
    async def _identify_data_sources(self, func_point: FunctionalPoint) -> List[str]:
        """识别数据源"""
        data_sources = []
        func_name = func_point.name.lower()
        
        if '用户' in func_name or 'user' in func_name:
            data_sources.extend(['用户数据库表', 'LDAP/AD目录服务', 'OAuth第三方认证'])
        
        if '内容' in func_name or 'content' in func_name:
            data_sources.extend(['内容管理系统', '文件系统', 'CDN存储'])
        
        if '数据' in func_name or 'data' in func_name:
            data_sources.extend(['业务数据库', '日志文件', '消息队列', '缓存系统'])
        
        if 'api' in func_name or '接口' in func_name:
            data_sources.extend(['HTTP请求参数', '请求头信息', 'Cookie/Session'])
        
        if '文件' in func_name or 'file' in func_name:
            data_sources.extend(['本地文件系统', '云存储服务', '上传临时目录'])
        
        # 确保至少有一个数据源
        if not data_sources:
            data_sources = ['系统内存', '配置文件', '环境变量']
        
        return data_sources[:4]  # 限制数量
    
    async def _identify_api_endpoints(self, func_point: FunctionalPoint) -> List[str]:
        """识别API端点"""
        endpoints = []
        func_name = func_point.name.lower()
        
        if func_point.level == 2:
            # 为二级功能点生成典型的API端点
            if '认证' in func_name or 'login' in func_name:
                endpoints = ['POST /api/auth/login', 'POST /api/auth/logout', 'GET /api/auth/profile']
            elif '内容' in func_name or 'content' in func_name:
                endpoints = ['GET /api/content', 'POST /api/content', 'PUT /api/content/{id}', 'DELETE /api/content/{id}']
            elif '数据' in func_name or 'data' in func_name:
                endpoints = ['GET /api/data/query', 'POST /api/data/import', 'GET /api/data/report']
            else:
                endpoints = [f'/api/{func_name.replace(" ", "-")}']
        
        elif func_point.level == 3:
            # 为三级功能点生成具体端点
            parent_func = self.functional_points.get(func_point.parent_id)
            if parent_func:
                parent_endpoint = f'/api/{parent_func.name.replace(" ", "-").lower()}'
                endpoints = [f'{parent_endpoint}/{func_name.replace(" ", "-")}']
        
        return endpoints
    
    async def _identify_database_tables(self, func_point: FunctionalPoint) -> List[str]:
        """识别数据库表"""
        tables = []
        func_name = func_point.name.lower()
        
        if '用户' in func_name or 'user' in func_name:
            tables = ['users', 'user_profiles', 'user_roles', 'permissions']
        elif '内容' in func_name or 'content' in func_name:
            tables = ['contents', 'content_versions', 'content_categories', 'media_assets']
        elif '数据' in func_name or 'data' in func_name:
            tables = ['data_records', 'data_sources', 'processing_logs', 'analytics_results']
        elif func_point.level == 3:
            # 为具体操作生成表名
            table_name = func_name.replace(' ', '_').replace('-', '_')
            tables = [f'{table_name}_logs', f'{table_name}_history']
        
        return tables[:3]
    
    async def _identify_external_services(self, func_point: FunctionalPoint) -> List[str]:
        """识别外部服务"""
        services = []
        func_name = func_point.name.lower()
        
        if '认证' in func_name or 'login' in func_name:
            services = ['OAuth2.0 Provider', 'LDAP Server', 'SSO Service']
        elif '邮件' in func_name or 'email' in func_name:
            services = ['SMTP Service', 'Email Template Engine', 'Notification Service']
        elif '支付' in func_name or 'payment' in func_name:
            services = ['Payment Gateway', 'Bank API', 'Fraud Detection Service']
        elif '文件' in func_name or 'file' in func_name:
            services = ['Cloud Storage API', 'CDN Service', 'Virus Scanner']
        
        # 通用外部服务
        if not services and func_point.level <= 2:
            services = ['Logging Service', 'Monitoring API', 'Configuration Service']
        
        return services[:3]
    
    async def _identify_user_interactions(self, func_point: FunctionalPoint) -> List[str]:
        """识别用户交互"""
        interactions = []
        func_name = func_point.name.lower()
        
        if func_point.level == 3:
            if '登录' in func_name or 'login' in func_name:
                interactions = ['输入用户名密码', '点击登录按钮', '接收验证码']
            elif '创建' in func_name or 'create' in func_name:
                interactions = ['填写表单信息', '上传文件', '点击保存按钮']
            elif '查询' in func_name or 'search' in func_name:
                interactions = ['输入搜索条件', '选择筛选条件', '查看结果列表']
            else:
                interactions = ['界面操作', '数据输入', '结果确认']
        
        return interactions
    
    async def generate_requirement_report(self, format_type: str = 'structured') -> str:
        """生成需求报告"""
        print("📋 生成需求报告...")
        
        if format_type == 'structured':
            return await self._generate_structured_report()
        elif format_type == 'markdown':
            return await self._generate_markdown_report()
        elif format_type == 'json':
            return json.dumps({
                'project_structure': self.project_structure,
                'functional_points': {k: asdict(v) for k, v in self.functional_points.items()},
                'requirements': {k: asdict(v) for k, v in self.requirements.items()}
            }, ensure_ascii=False, indent=2)
        else:
            return await self._generate_text_report()
    
    async def _generate_structured_report(self) -> str:
        """生成结构化报告"""
        report_lines = [
            "=" * 80,
            "📊 项目需求分析报告",
            "=" * 80,
            f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"项目路径: {self.project_path}",
            ""
        ]
        
        # 项目概览
        report_lines.append("📁 项目概览")
        report_lines.append("-" * 40)
        structure = self.project_structure
        report_lines.append(f"目录数量: {len(structure['directories'])}")
        report_lines.append(f"文件类型: {len(structure['files_by_type'])}")
        report_lines.append(f"入口文件: {len(structure['entry_points'])}")
        report_lines.append(f"配置文件: {len(structure['config_files'])}")
        report_lines.append("")
        
        # 按层级显示功能点和需求
        for level in [1, 2, 3]:
            level_points = [fp for fp in self.functional_points.values() if fp.level == level]
            if not level_points:
                continue
                
            level_names = {1: '一级功能点（主要业务域）', 2: '二级功能点（子系统）', 3: '三级功能点（具体操作）'}
            report_lines.append(f"\n🎯 {level_names[level]}")
            report_lines.append("=" * 60)
            
            for fp in level_points:
                req = self.requirements.get(fp.id)
                
                report_lines.append(f"\n【{fp.id}】{fp.name}")
                report_lines.append(f"描述: {fp.description}")
                
                if req:
                    report_lines.append(f"需求描述: {req.requirement_description}")
                    report_lines.append(f"系统调用: {req.system_invocation_method}")
                    report_lines.append(f"数据源: {', '.join(req.data_sources)}")
                    
                    if req.api_endpoints:
                        report_lines.append(f"API端点: {', '.join(req.api_endpoints)}")
                    if req.database_tables:
                        report_lines.append(f"数据库表: {', '.join(req.database_tables)}")
                    if req.external_services:
                        report_lines.append(f"外部服务: {', '.join(req.external_services)}")
                    if req.user_interactions:
                        report_lines.append(f"用户交互: {', '.join(req.user_interactions)}")
                
                # 显示子功能点
                if fp.children_ids:
                    child_names = [self.functional_points[cid].name for cid in fp.children_ids]
                    report_lines.append(f"子功能: {', '.join(child_names)}")
        
        report_lines.append("\n" + "=" * 80)
        report_lines.append("✅ 分析完成")
        
        return "\n".join(report_lines)
    
    async def _generate_markdown_report(self) -> str:
        """生成Markdown格式报告"""
        md_lines = [
            "# 项目需求分析报告",
            f"\n**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"\n**项目路径**: {self.project_path}",
            "\n---"
        ]
        
        # 项目结构
        md_lines.append("## 📁 项目结构概览")
        structure = self.project_structure
        md_lines.append(f"- **目录数量**: {len(structure['directories'])}")
        md_lines.append(f"- **文件类型**: {len(structure['files_by_type'])}")
        md_lines.append(f"- **入口文件**: {len(structure['entry_points'])}")
        
        # 功能点层次
        for level in [1, 2, 3]:
            level_points = [fp for fp in self.functional_points.values() if fp.level == level]
            if not level_points:
                continue
                
            level_names = {1: '一级功能点（主要业务域）', 2: '二级功能点（子系统）', 3: '三级功能点（具体操作）'}
            md_lines.append(f"\n## {level_names[level]}")
            
            for fp in level_points:
                req = self.requirements.get(fp.id)
                md_lines.append(f"\n### 【{fp.id}】{fp.name}")
                md_lines.append(f"\n**描述**: {fp.description}")
                
                if req:
                    md_lines.append(f"\n**需求描述**: {req.requirement_description}")
                    md_lines.append(f"\n**系统调用方式**: {req.system_invocation_method}")
                    md_lines.append(f"\n**数据源**: {', '.join(req.data_sources)}")
                    
                    if req.api_endpoints:
                        md_lines.append(f"\n**API端点**: {', '.join(req.api_endpoints)}")
                    if req.database_tables:
                        md_lines.append(f"\n**数据库表**: {', '.join(req.database_tables)}")
        
        return "\n".join(md_lines)
    
    async def _generate_text_report(self) -> str:
        """生成文本格式报告"""
        return await self._generate_structured_report()
    
    async def analyze_project_requirements(self, format_type: str = 'structured') -> str:
        """完整的需求分析流程"""
        print("🚀 开始项目需求分析...")
        
        # 执行分析流程
        await self.analyze_project_structure()
        await self.extract_functional_modules()
        await self.decompose_functional_hierarchy()
        await self.generate_requirement_descriptions()
        
        # 生成报告
        report = await self.generate_requirement_report(format_type)
        
        print("✅ 需求分析完成")
        return report