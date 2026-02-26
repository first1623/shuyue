import os
import re
import json
import yaml
from typing import Dict, List, Any, Tuple, Optional
from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import datetime
import ast

@dataclass
class Prompt:
    id: str
    content: str
    source_file: str
    line_number: int
    purpose: str  # 'debugging', 'code_generation', 'review', 'testing', 'documentation', 'planning'
    domain: str  # 'frontend', 'backend', 'devops', 'data_science', 'general'
    complexity: str  # 'simple', 'intermediate', 'advanced'
    context_type: str  # 'project_specific', 'generic', 'reusable'
    tags: List[str]
    created_at: str
    usage_count: int = 0
    effectiveness_rating: float = 0.0

class PromptCollector:
    """提示词收集和整理工具"""
    
    def __init__(self, project_path: str = "."):
        self.project_path = Path(project_path)
        self.discovered_prompts: List[Prompt] = []
        self.prompt_library = {}
        self.pattern_config = self._load_pattern_config()
        
    def _load_pattern_config(self) -> Dict:
        """加载提示词识别模式配置"""
        return {
            'comment_patterns': {
                'python': [
                    r'#\s*[Pp]rompt:\s*(.+)$',
                    r'#\s*[Ii]nstruction:\s*(.+)$', 
                    r'#\s*[Gg]uide:\s*(.+)$',
                    r'#\s*[Tt]emplate:\s*(.+)$',
                    r'#\s*[Dd]ebug.*?:\s*(.+)$',
                    r'#\s*[Ff]ix.*?:\s*(.+)$'
                ],
                'javascript': [
                    r'//\s*[Pp]rompt:\s*(.+)$',
                    r'//\s*[Ii]nstruction:\s*(.+)$',
                    r'//\s*[Tt]odo.*?:\s*(.+)$',
                    r'/\*\s*[Pp]rompt:\s*(.+?)\*/',
                    r'/\*\s*[Gg]uide:\s*(.+?)\*/'
                ],
                'general': [
                    r'<!--\s*[Pp]rompt:\s*(.+?)-->',
                    r'<!--\s*[Ii]nstruction:\s*(.+?)-->',
                    r'\/\/\s*[Pp]rompt:\s*(.+)$',
                    r'%.*?[Pp]rompt:\s*(.+)$'
                ]
            },
            'doc_patterns': {
                'markdown': [
                    r'^##\s*[Pp]rompt[s]?\s*$\n(.*?)(?=\n##|\n#|$)',
                    r'^###\s*[Ii]nstruction[s]?\s*$\n(.*?)(?=\n###|\n##|\n#|$)',
                    r'\*\*[Pp]rompt\*\*:\s*(.+)$',
                    r'>\s*[Nn]ote[:\s]*(.+)$'
                ],
                'text': [
                    r'[Pp]rompt[:\s]*(.+)$',
                    r'[Ii]nstruction[:\s]*(.+)$',
                    r'[Gg]uide[:\s]*(.+)$',
                    r'[Tt]emplate[:\s]*(.+)$'
                ]
            },
            'config_patterns': {
                'json': [
                    r'"[Pp]rompt"\s*:\s*"([^"]+)"',
                    r'"[Ii]nstruction"\s*:\s*"([^"]+)"',
                    r'"[Gg]uide"\s*:\s*"([^"]+)"'
                ],
                'yaml': [
                    r'[Pp]rompt:\s*(.+)',
                    r'[Ii]nstruction:\s*(.+)',
                    r'[Gg]uide:\s*(.+)'
                ]
            }
        }
    
    async def scan_project_for_prompts(self, file_types: List[str] = None, 
                                     exclude_dirs: List[str] = None) -> List[Prompt]:
        """扫描项目中的提示词"""
        print("🔍 开始扫描项目中的提示词...")
        
        if file_types is None:
            file_types = ['py', 'js', 'ts', 'md', 'txt', 'json', 'yml', 'yaml', 'java', 'cpp', 'c']
        
        if exclude_dirs is None:
            exclude_dirs = ['node_modules', '.git', '__pycache__', 'venv', '.venv', 'dist', 'build']
        
        self.discovered_prompts = []
        
        for file_type in file_types:
            files = list(self.project_path.rglob(f"*.{file_type}"))
            
            for file_path in files:
                # 跳过排除的目录
                if any(excluded in str(file_path) for excluded in exclude_dirs):
                    continue
                    
                try:
                    prompts = await self.extract_prompts_from_file(file_path)
                    self.discovered_prompts.extend(prompts)
                except Exception as e:
                    print(f"扫描文件 {file_path} 时出错: {e}")
        
        print(f"✅ 发现 {len(self.discovered_prompts)} 个提示词")
        return self.discovered_prompts
    
    async def extract_prompts_from_file(self, file_path: Path) -> List[Prompt]:
        """从单个文件中提取提示词"""
        prompts = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')
                
            file_ext = file_path.suffix.lower()
            
            # 根据文件类型选择提取策略
            if file_ext in ['.py', '.js', '.ts', '.java', '.cpp', '.c']:
                prompts.extend(self._extract_from_code_comments(content, lines, file_path, file_ext))
            elif file_ext in ['.md', '.txt']:
                prompts.extend(self._extract_from_documentation(content, file_path, file_ext))
            elif file_ext in ['.json']:
                prompts.extend(self._extract_from_json(content, file_path))
            elif file_ext in ['.yml', '.yaml']:
                prompts.extend(self._extract_from_yaml(content, file_path))
            else:
                prompts.extend(self._extract_from_generic_text(content, lines, file_path))
                
        except Exception as e:
            print(f"读取文件 {file_path} 失败: {e}")
        
        return prompts
    
    def _extract_from_code_comments(self, content: str, lines: List[str], 
                                 file_path: Path, file_ext: str) -> List[Prompt]:
        """从代码注释中提取提示词"""
        prompts = []
        
        # 确定文件类型对应的模式
        if file_ext == '.py':
            patterns = self.pattern_config['comment_patterns']['python']
        elif file_ext in ['.js', '.ts']:
            patterns = self.pattern_config['comment_patterns']['javascript']
        else:
            patterns = self.pattern_config['comment_patterns']['general']
        
        for line_num, line in enumerate(lines, 1):
            for pattern in patterns:
                matches = re.finditer(pattern, line, re.MULTILINE | re.DOTALL)
                for match in matches:
                    prompt_content = match.group(1).strip()
                    if len(prompt_content) > 10:  # 过滤太短的内容
                        prompt = self._create_prompt_from_match(
                            prompt_content, file_path, line_num, 'code_comment'
                        )
                        prompts.append(prompt)
        
        return prompts
    
    def _extract_from_documentation(self, content: str, file_path: Path, 
                                   file_ext: str) -> List[Prompt]:
        """从文档中提取提示词"""
        prompts = []
        
        if file_ext == '.md':
            patterns = self.pattern_config['doc_patterns']['markdown']
        else:
            patterns = self.pattern_config['doc_patterns']['text']
        
        for pattern in patterns:
            matches = re.finditer(pattern, content, re.MULTILINE | re.DOTALL)
            for match in matches:
                prompt_content = match.group(1).strip()
                if len(prompt_content) > 10:
                    # 计算行号
                    line_num = content[:match.start()].count('\n') + 1
                    prompt = self._create_prompt_from_match(
                        prompt_content, file_path, line_num, 'documentation'
                    )
                    prompts.append(prompt)
        
        return prompts
    
    def _extract_from_json(self, content: str, file_path: Path) -> List[Prompt]:
        """从JSON配置中提取提示词"""
        prompts = []
        
        try:
            data = json.loads(content)
            prompts.extend(self._extract_from_dict_recursive(data, file_path, 'json'))
        except json.JSONDecodeError:
            pass
        
        return prompts
    
    def _extract_from_yaml(self, content: str, file_path: Path) -> List[Prompt]:
        """从YAML配置中提取提示词"""
        prompts = []
        
        try:
            data = yaml.safe_load(content)
            if data:
                prompts.extend(self._extract_from_dict_recursive(data, file_path, 'yaml'))
        except yaml.YAMLError:
            pass
        
        return prompts
    
    def _extract_from_dict_recursive(self, data: Dict, file_path: Path, 
                                   source_type: str, path: str = "") -> List[Prompt]:
        """递归从字典结构中提取提示词"""
        prompts = []
        
        for key, value in data.items():
            current_path = f"{path}.{key}" if path else key
            
            # 检查键名是否暗示这是提示词
            if any(indicator in key.lower() for indicator in ['prompt', 'instruction', 'guide', 'template']):
                if isinstance(value, str) and len(value) > 10:
                    line_num = 1  # JSON/YAML不便于精确定位行号
                    prompt = self._create_prompt_from_match(
                        value, file_path, line_num, source_type, current_path
                    )
                    prompts.append(prompt)
            
            # 递归处理嵌套结构
            if isinstance(value, dict):
                prompts.extend(self._extract_from_dict_recursive(value, file_path, source_type, current_path))
            elif isinstance(value, list):
                for i, item in enumerate(value):
                    if isinstance(item, dict):
                        prompts.extend(self._extract_from_dict_recursive(
                            item, file_path, source_type, f"{current_path}[{i}]"
                        ))
        
        return prompts
    
    def _extract_from_generic_text(self, content: str, lines: List[str], 
                                  file_path: Path) -> List[Prompt]:
        """从通用文本中提取提示词"""
        prompts = []
        
        # 简单的启发式规则：寻找包含特定关键词的行
        prompt_indicators = ['prompt', 'instruction', 'guide', 'template', 'todo', 'fix', 'debug']
        
        for line_num, line in enumerate(lines, 1):
            line_lower = line.lower()
            if any(indicator in line_lower for indicator in prompt_indicators):
                # 清理行内容
                cleaned_line = re.sub(r'^[#\s/*>-]+', '', line).strip()
                if len(cleaned_line) > 15:
                    prompt = self._create_prompt_from_match(
                        cleaned_line, file_path, line_num, 'generic_text'
                    )
                    prompts.append(prompt)
        
        return prompts
    
    def _create_prompt_from_match(self, content: str, file_path: Path, 
                                line_num: int, source_type: str, 
                                config_path: str = "") -> Prompt:
        """从匹配结果创建Prompt对象"""
        # 分析提示词的目的和领域
        purpose = self.analyze_prompt_purpose(content)
        domain = self.analyze_prompt_domain(content)
        complexity = self.analyze_prompt_complexity(content)
        context_type = self.analyze_context_type(content)
        tags = self.generate_tags(content, purpose, domain)
        
        prompt_id = f"{file_path.stem}_{source_type}_{line_num}_{hash(content) % 10000}"
        
        return Prompt(
            id=prompt_id,
            content=content,
            source_file=str(file_path),
            line_number=line_num,
            purpose=purpose,
            domain=domain,
            complexity=complexity,
            context_type=context_type,
            tags=tags,
            created_at=datetime.now().isoformat(),
            usage_count=0,
            effectiveness_rating=0.0
        )
    
    def analyze_prompt_purpose(self, content: str) -> str:
        """分析提示词的目的"""
        content_lower = content.lower()
        
        purpose_keywords = {
            'debugging': ['debug', 'fix', 'error', 'bug', 'issue', 'problem'],
            'code_generation': ['create', 'generate', 'build', 'implement', 'write', 'make'],
            'review': ['review', 'check', 'examine', 'analyze', 'evaluate'],
            'testing': ['test', 'verify', 'validate', 'assert', 'mock'],
            'documentation': ['document', 'explain', 'describe', 'readme', 'comment'],
            'planning': ['plan', 'design', 'architect', 'structure', 'organize']
        }
        
        for purpose, keywords in purpose_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                return purpose
        
        return 'general'
    
    def analyze_prompt_domain(self, content: str) -> str:
        """分析提示词的领域"""
        content_lower = content.lower()
        
        domain_keywords = {
            'frontend': ['react', 'vue', 'angular', 'css', 'html', 'frontend', 'ui', 'ux'],
            'backend': ['api', 'server', 'database', 'backend', 'endpoint', 'service'],
            'devops': ['deploy', 'docker', 'kubernetes', 'ci/cd', 'pipeline', 'infrastructure'],
            'data_science': ['model', 'data', 'ml', 'ai', 'analysis', 'algorithm', 'training'],
            'mobile': ['mobile', 'ios', 'android', 'flutter', 'react native'],
            'security': ['security', 'auth', 'encrypt', 'permission', 'vulnerability']
        }
        
        for domain, keywords in domain_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                return domain
        
        return 'general'
    
    def analyze_prompt_complexity(self, content: str) -> str:
        """分析提示词的复杂度"""
        word_count = len(content.split())
        
        if word_count < 15:
            return 'simple'
        elif word_count < 50:
            return 'intermediate'
        else:
            return 'advanced'
    
    def analyze_context_type(self, content: str) -> str:
        """分析上下文类型"""
        # 检查是否包含特定项目名称或路径
        if re.search(r'\b[A-Z][a-zA-Z]+Project\b|/[a-zA-Z_-]+/', content):
            return 'project_specific'
        elif any(word in content.lower() for word in ['generic', 'template', 'standard', 'common']):
            return 'generic'
        else:
            return 'reusable'
    
    def generate_tags(self, content: str, purpose: str, domain: str) -> List[str]:
        """生成标签"""
        tags = [purpose, domain]
        
        content_lower = content.lower()
        
        # 添加技术标签
        tech_keywords = ['python', 'javascript', 'react', 'api', 'database', 'testing', 'debug']
        for keyword in tech_keywords:
            if keyword in content_lower:
                tags.append(keyword)
        
        # 添加动作标签
        action_keywords = ['create', 'fix', 'optimize', 'refactor', 'implement']
        for keyword in action_keywords:
            if keyword in content_lower:
                tags.append(keyword)
        
        return list(set(tags))  # 去重
    
    async def create_prompt_library(self, organization_style: str = 'by_purpose') -> Dict:
        """创建结构化的提示词库"""
        print("📚 创建提示词库...")
        
        library = {
            'metadata': {
                'created_at': datetime.now().isoformat(),
                'total_prompts': len(self.discovered_prompts),
                'organization_style': organization_style
            },
            'categories': {},
            'prompts': [asdict(prompt) for prompt in self.discovered_prompts]
        }
        
        if organization_style == 'by_purpose':
            library['categories'] = self._organize_by_purpose()
        elif organization_style == 'by_domain':
            library['categories'] = self._organize_by_domain()
        elif organization_style == 'by_complexity':
            library['categories'] = self._organize_by_complexity()
        else:
            library['categories'] = self._organize_hierarchical()
        
        self.prompt_library = library
        return library
    
    def _organize_by_purpose(self) -> Dict:
        """按目的组织提示词"""
        categories = {}
        
        for prompt in self.discovered_prompts:
            purpose = prompt.purpose
            if purpose not in categories:
                categories[purpose] = []
            categories[purpose].append(asdict(prompt))
        
        return categories
    
    def _organize_by_domain(self) -> Dict:
        """按领域组织提示词"""
        categories = {}
        
        for prompt in self.discovered_prompts:
            domain = prompt.domain
            if domain not in categories:
                categories[domain] = []
            categories[domain].append(asdict(prompt))
        
        return categories
    
    def _organize_by_complexity(self) -> Dict:
        """按复杂度组织提示词"""
        categories = {}
        
        for prompt in self.discovered_prompts:
            complexity = prompt.complexity
            if complexity not in categories:
                categories[complexity] = []
            categories[complexity].append(asdict(prompt))
        
        return categories
    
    def _organize_hierarchical(self) -> Dict:
        """分层组织提示词"""
        categories = {
            'by_purpose': self._organize_by_purpose(),
            'by_domain': self._organize_by_domain(),
            'by_complexity': self._organize_by_complexity(),
            'by_context': self._organize_by_context_type()
        }
        return categories
    
    def _organize_by_context_type(self) -> Dict:
        """按上下文类型组织提示词"""
        categories = {}
        
        for prompt in self.discovered_prompts:
            context_type = prompt.context_type
            if context_type not in categories:
                categories[context_type] = []
            categories[context_type].append(asdict(prompt))
        
        return categories
    
    async def generate_reuse_templates(self, template_format: str = 'markdown') -> str:
        """生成可复用的提示词模板"""
        print("🛠️ 生成重用模板...")
        
        if not self.prompt_library:
            await self.create_prompt_library()
        
        if template_format == 'markdown':
            return self._generate_markdown_templates()
        elif template_format == 'json':
            return json.dumps(self.prompt_library, indent=2, ensure_ascii=False)
        elif template_format == 'yaml':
            return yaml.dump(self.prompt_library, default_flow_style=False, allow_unicode=True)
        else:
            return self._generate_text_templates()
    
    def _generate_markdown_templates(self) -> str:
        """生成Markdown格式的模板"""
        md_content = ["# 提示词库\n"]
        md_content.append(f"*生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
        md_content.append(f"*总计提示词: {len(self.discovered_prompts)}*\n\n")
        
        # 按目的分组显示
        by_purpose = self._organize_by_purpose()
        
        for purpose, prompts in by_purpose.items():
            md_content.append(f"## {purpose.title()} 相关提示词\n")
            
            for i, prompt_data in enumerate(prompts, 1):
                prompt = Prompt(**prompt_data)
                md_content.append(f"### {i}. {prompt.source_file}:{prompt.line_number}\n")
                md_content.append(f"**领域**: {prompt.domain} | **复杂度**: {prompt.complexity} | **上下文**: {prompt.context_type}\n")
                md_content.append(f"**标签**: {', '.join(prompt.tags)}\n")
                md_content.append(f"> {prompt.content}\n\n")
                
                # 生成可重用模板
                template = self._create_reusable_template(prompt)
                md_content.append(f"**可重用模板**:\n```\n{template}\n```\n\n")
        
        return '\n'.join(md_content)
    
    def _create_reusable_template(self, prompt: Prompt) -> str:
        """创建可重用的提示词模板"""
        template = prompt.content
        
        # 替换项目特定的路径和名称为占位符
        template = re.sub(r'/[a-zA-Z_-]+/', '/{PROJECT_PATH}/', template)
        template = re.sub(r'\b[A-Z][a-zA-Z]+Project\b', '{PROJECT_NAME}', template)
        template = re.sub(r'\b[a-z]+@[a-z]+\.[a-z]+\b', '{EMAIL}', template)
        template = re.sub(r'\b\d{4}-\d{2}-\d{2}\b', '{DATE}', template)
        template = re.sub(r'\b\d+\b(?=\s*(?:days?|hours?|minutes?))', '{TIME_VALUE}', template)
        
        # 添加使用说明
        template += "\n\n---\n*使用方法: 将 {} 中的占位符替换为实际值*"
        
        return template
    
    def _generate_text_templates(self) -> str:
        """生成纯文本模板"""
        text_content = ["提示词库\n"]
        text_content.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        text_content.append(f"总计提示词: {len(self.discovered_prompts)}\n\n")
        
        for i, prompt in enumerate(self.discovered_prompts, 1):
            text_content.append(f"{i}. [{prompt.purpose}] {prompt.source_file}:{prompt.line_number}")
            text_content.append(f"   内容: {prompt.content}")
            text_content.append(f"   模板: {self._create_reusable_template(prompt)}")
            text_content.append("")
        
        return '\n'.join(text_content)
    
    async def search_prompts(self, criteria: Dict[str, Any]) -> List[Prompt]:
        """搜索提示词"""
        filtered_prompts = self.discovered_prompts.copy()
        
        # 按目的筛选
        if 'purpose' in criteria:
            filtered_prompts = [p for p in filtered_prompts if p.purpose == criteria['purpose']]
        
        # 按领域筛选
        if 'domain' in criteria:
            filtered_prompts = [p for p in filtered_prompts if p.domain == criteria['domain']]
        
        # 按复杂度筛选
        if 'complexity' in criteria:
            filtered_prompts = [p for p in filtered_prompts if p.complexity == criteria['complexity']]
        
        # 按标签筛选
        if 'tags' in criteria:
            required_tags = set(criteria['tags'])
            filtered_prompts = [p for p in filtered_prompts if required_tags.intersection(set(p.tags))]
        
        # 按关键词搜索内容
        if 'keyword' in criteria:
            keyword = criteria['keyword'].lower()
            filtered_prompts = [p for p in filtered_prompts if keyword in p.content.lower()]
        
        return filtered_prompts
    
    async def export_prompt_library(self, export_path: str, format_type: str = 'markdown') -> str:
        """导出提示词库"""
        print(f"💾 导出提示词库到 {export_path}...")
        
        if format_type == 'markdown':
            content = await self.generate_reuse_templates('markdown')
        elif format_type == 'json':
            content = json.dumps(self.prompt_library, indent=2, ensure_ascii=False)
        elif format_type == 'yaml':
            content = yaml.dump(self.prompt_library, default_flow_style=False, allow_unicode=True)
        else:
            content = await self.generate_reuse_templates('text')
        
        # 确保导出目录存在
        export_file = Path(export_path)
        export_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(export_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return export_path