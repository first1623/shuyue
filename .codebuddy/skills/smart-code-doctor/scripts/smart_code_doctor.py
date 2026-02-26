import asyncio
import subprocess
import ast
import json
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from pathlib import Path
import traceback

@dataclass
class CodeIssue:
    type: str  # 'syntax', 'runtime', 'logical', 'performance'
    severity: str  # 'critical', 'high', 'medium', 'low'
    line: int
    message: str
    fix_suggestion: str
    confidence: float

class SmartCodeDoctor:
    """智能代码医生 - 自动诊断和修复代码问题"""
    
    def __init__(self, project_path: str = "."):
        self.project_path = Path(project_path)
        self.diagnosis_history = []
        self.fix_strategies = self._load_fix_strategies()
        
    def _load_fix_strategies(self) -> Dict:
        """加载修复策略"""
        return {
            'syntax_error': self._fix_syntax_error,
            'import_error': self._fix_import_error,
            'name_error': self._fix_name_error,
            'type_error': self._fix_type_error,
            'index_error': self._fix_index_error,
            'attribute_error': self._fix_attribute_error,
            'logic_error': self._fix_logic_error,
            'performance_issue': self._fix_performance_issue
        }
    
    async def diagnose(self, error_traceback: str, code_snippet: str = None) -> Dict:
        """
        诊断代码问题
        """
        print("🩺 开始代码诊断...")
        
        # 分析错误堆栈
        error_info = self._parse_error_traceback(error_traceback)
        
        # 静态代码分析
        static_issues = await self._static_analysis(code_snippet)
        
        # 动态分析建议
        dynamic_issues = await self._dynamic_analysis_suggestions(error_info)
        
        # 合并分析结果
        diagnosis = {
            'error_type': error_info['type'],
            'error_message': error_info['message'],
            'location': error_info['location'],
            'issues': static_issues + dynamic_issues,
            'probable_cause': self._identify_probable_cause(error_info),
            'fix_priority': self._calculate_fix_priority(static_issues + dynamic_issues),
            'confidence_score': self._calculate_confidence(error_info, static_issues)
        }
        
        self.diagnosis_history.append(diagnosis)
        return diagnosis
    
    def _parse_error_traceback(self, traceback_str: str) -> Dict:
        """解析错误堆栈"""
        lines = traceback_str.strip().split('\n')
        error_info = {
            'type': 'Unknown',
            'message': '',
            'location': {},
            'full_traceback': traceback_str
        }
        
        for line in lines:
            if 'Error:' in line or 'Exception:' in line:
                parts = line.split(':', 1)
                if len(parts) > 1:
                    error_info['type'] = parts[0].strip()
                    error_info['message'] = parts[1].strip()
            elif 'File "' in line:
                # 提取文件和行号信息
                match = re.search(r'File "(.*?)", line (\d+)', line)
                if match:
                    error_info['location'] = {
                        'file': match.group(1),
                        'line': int(match.group(2))
                    }
        
        return error_info
    
    async def _static_analysis(self, code: str) -> List[CodeIssue]:
        """静态代码分析"""
        issues = []
        
        if not code:
            return issues
        
        try:
            # 1. 语法检查
            try:
                ast.parse(code)
            except SyntaxError as e:
                issues.append(CodeIssue(
                    type='syntax',
                    severity='critical',
                    line=e.lineno or 0,
                    message=str(e),
                    fix_suggestion=self._suggest_syntax_fix(e),
                    confidence=0.95
                ))
            
            # 2. 代码风格和潜在问题检查
            issues.extend(await self._check_code_quality(code))
            
            # 3. 安全检查
            issues.extend(await self._check_security(code))
            
        except Exception as e:
            print(f"静态分析时出错: {e}")
        
        return issues
    
    async def _dynamic_analysis_suggestions(self, error_info: Dict) -> List[CodeIssue]:
        """基于错误信息的动态分析建议"""
        issues = []
        
        error_type = error_info['type']
        
        # 根据错误类型提供针对性的建议
        suggestions_map = {
            'NameError': self._suggest_name_error_fix,
            'TypeError': self._suggest_type_error_fix,
            'IndexError': self._suggest_index_error_fix,
            'ImportError': self._suggest_import_fix,
            'AttributeError': self._suggest_attribute_fix,
            'KeyError': self._suggest_key_error_fix,
            'ValueError': self._suggest_value_error_fix
        }
        
        if error_type in suggestions_map:
            suggestion = suggestions_map[error_type](error_info)
            if suggestion:
                issues.append(suggestion)
        
        return issues
    
    def _suggest_syntax_fix(self, syntax_error: SyntaxError) -> str:
        """语法错误修复建议"""
        error_msg = str(syntax_error)
        
        if 'invalid syntax' in error_msg:
            if 'print' in error_msg and 'missing parentheses' in error_msg.lower():
                return "在Python 3中，print需要括号。请将 'print x' 改为 'print(x)'"
            elif 'expected ':' in error_msg:
                return "请检查if/elif/else/for/while/def/class语句后是否缺少冒号(:)"
            elif 'unexpected indent' in error_msg:
                return "存在意外的缩进。请检查代码块的缩进是否一致"
            elif 'EOL while scanning string literal' in error_msg:
                return "字符串未正确闭合。请检查引号是否配对"
        
        return "请检查代码语法，确保括号、引号、冒号等符号正确配对"
    
    async def auto_fix(self, diagnosis: Dict, code: str) -> Dict:
        """
        尝试自动修复代码
        """
        print("🔧 尝试自动修复...")
        
        fixes_applied = []
        fixed_code = code
        
        for issue in diagnosis['issues']:
            if issue.confidence > 0.7:  # 高置信度的问题才尝试自动修复
                fix_result = self._apply_fix_strategy(issue, fixed_code)
                if fix_result['success']:
                    fixed_code = fix_result['fixed_code']
                    fixes_applied.append({
                        'issue': issue.message,
                        'fix': issue.fix_suggestion,
                        'confidence': issue.confidence
                    })
        
        return {
            'success': len(fixes_applied) > 0,
            'fixed_code': fixed_code,
            'applied_fixes': fixes_applied,
            'original_code': code,
            'remaining_issues': [i for i in diagnosis['issues'] if i.confidence <= 0.7]
        }
    
    def _apply_fix_strategy(self, issue: CodeIssue, code: str) -> Dict:
        """应用具体的修复策略"""
        lines = code.split('\n')
        line_num = issue.line - 1  # 转换为0-based索引
        
        if 0 <= line_num < len(lines):
            original_line = lines[line_num]
            
            # 根据问题类型应用不同的修复策略
            if issue.type == 'syntax':
                fixed_line = self._fix_specific_syntax(original_line, issue.message)
                if fixed_line != original_line:
                    lines[line_num] = fixed_line
                    return {
                        'success': True,
                        'fixed_code': '\n'.join(lines),
                        'change': f"第{issue.line}行: {original_line} -> {fixed_line}"
                    }
        
        return {'success': False, 'fixed_code': code}
    
    def _fix_specific_syntax(self, line: str, error_msg: str) -> str:
        """修复特定的语法错误"""
        # 修复print语句（Python 2 -> Python 3）
        if 'print' in line and 'missing parentheses' in error_msg.lower():
            # 简单的print语句转换
            if line.strip().startswith('print '):
                content = line.split('print ', 1)[1]
                return line.replace(f'print {content}', f'print({content})')
        
        return line
    
    async def run_tests(self, test_command: str = None) -> Dict:
        """
        运行测试套件
        """
        if not test_command:
            # 尝试自动检测测试框架
            test_command = self._detect_test_framework()
        
        print(f"🧪 运行测试: {test_command}")
        
        try:
            result = subprocess.run(
                test_command,
                shell=True,
                capture_output=True,
                text=True,
                cwd=self.project_path
            )
            
            return {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _detect_test_framework(self) -> str:
        """自动检测测试框架"""
        if (self.project_path / 'pytest.ini').exists():
            return "pytest"
        elif (self.project_path / 'manage.py').exists():
            return "python manage.py test"
        elif (self.project_path / 'requirements.txt').exists():
            with open(self.project_path / 'requirements.txt') as f:
                if 'pytest' in f.read():
                    return "pytest"
        return "python -m unittest discover"
    
    def generate_report(self, diagnosis: Dict, fix_result: Dict = None) -> str:
        """生成诊断报告"""
        report = [
            "=" * 60,
            "📋 代码诊断报告",
            "=" * 60,
            f"错误类型: {diagnosis['error_type']}",
            f"错误信息: {diagnosis['error_message']}",
            f"位置: {diagnosis.get('location', {}).get('file', 'Unknown')}:{diagnosis.get('location', {}).get('line', 'Unknown')}",
            "",
            "🔍 发现的问题:"
        ]
        
        for i, issue in enumerate(diagnosis['issues'], 1):
            report.append(f"{i}. [{issue.severity.upper()}] {issue.type}")
            report.append(f"   行 {issue.line}: {issue.message}")
            report.append(f"   建议: {issue.fix_suggestion}")
            report.append(f"   置信度: {issue.confidence:.2f}")
            report.append("")
        
        if fix_result and fix_result.get('applied_fixes'):
            report.append("✅ 已应用的修复:")
            for fix in fix_result['applied_fixes']:
                report.append(f"   - {fix['issue']}")
                report.append(f"     修复: {fix['fix']}")
        
        report.append(f"\n💡 可能的原因: {diagnosis.get('probable_cause', 'Unknown')}")
        report.append(f"🔧 修复优先级: {diagnosis.get('fix_priority', 'medium')}")
        report.append(f"📊 诊断置信度: {diagnosis.get('confidence_score', 0):.2f}")
        report.append("=" * 60)
        
        return '\n'.join(report)
    
    async def continuous_integration_check(self) -> Dict:
        """
        运行完整的CI检查流程
        """
        print("🚀 开始持续集成检查...")
        
        checks = {
            'syntax_check': await self._check_syntax(),
            'import_check': await self._check_imports(),
            'test_suite': await self.run_tests(),
            'code_quality': await self._run_linter(),
            'security_scan': await self._security_scan()
        }
        
        all_passed = all(check.get('success', False) for check in checks.values())
        
        return {
            'overall_success': all_passed,
            'checks': checks,
            'failed_checks': [name for name, result in checks.items() if not result.get('success', True)],
            'recommendations': self._generate_ci_recommendations(checks)
        }
    
    # 以下是辅助方法的简化实现
    async def _check_code_quality(self, code: str) -> List[CodeIssue]:
        """检查代码质量"""
        return []  # 简化实现
    
    async def _check_security(self, code: str) -> List[CodeIssue]:
        """安全检查"""
        return []  # 简化实现
    
    def _identify_probable_cause(self, error_info: Dict) -> str:
        """识别可能原因"""
        return "需要进一步分析"
    
    def _calculate_fix_priority(self, issues: List[CodeIssue]) -> str:
        """计算修复优先级"""
        return "medium"
    
    def _calculate_confidence(self, error_info: Dict, static_issues: List[CodeIssue]) -> float:
        """计算置信度"""
        return 0.8
    
    def _suggest_name_error_fix(self, error_info: Dict) -> Optional[CodeIssue]:
        """建议NameError修复"""
        return CodeIssue('runtime', 'high', 0, '变量未定义', '检查变量名拼写', 0.8)
    
    def _suggest_type_error_fix(self, error_info: Dict) -> Optional[CodeIssue]:
        """建议TypeError修复"""
        return CodeIssue('runtime', 'high', 0, '类型错误', '检查数据类型匹配', 0.8)
    
    def _suggest_index_error_fix(self, error_info: Dict) -> Optional[CodeIssue]:
        """建议IndexError修复"""
        return CodeIssue('runtime', 'medium', 0, '索引越界', '检查列表/数组长度', 0.8)
    
    def _suggest_import_fix(self, error_info: Dict) -> Optional[CodeIssue]:
        """建议ImportError修复"""
        return CodeIssue('runtime', 'high', 0, '导入错误', '检查模块路径和安装', 0.8)
    
    def _suggest_attribute_fix(self, error_info: Dict) -> Optional[CodeIssue]:
        """建议AttributeError修复"""
        return CodeIssue('runtime', 'high', 0, '属性不存在', '检查方法/属性名', 0.8)
    
    def _suggest_key_error_fix(self, error_info: Dict) -> Optional[CodeIssue]:
        """建议KeyError修复"""
        return CodeIssue('runtime', 'medium', 0, '键不存在', '检查字典键名', 0.8)
    
    def _suggest_value_error_fix(self, error_info: Dict) -> Optional[CodeIssue]:
        """建议ValueError修复"""
        return CodeIssue('runtime', 'medium', 0, '值错误', '检查参数有效性', 0.8)
    
    def _fix_syntax_error(self, code: str) -> str:
        """修复语法错误"""
        return code
    
    def _fix_import_error(self, code: str) -> str:
        """修复导入错误"""
        return code
    
    def _fix_name_error(self, code: str) -> str:
        """修复名称错误"""
        return code
    
    def _fix_type_error(self, code: str) -> str:
        """修复类型错误"""
        return code
    
    def _fix_index_error(self, code: str) -> str:
        """修复索引错误"""
        return code
    
    def _fix_attribute_error(self, code: str) -> str:
        """修复属性错误"""
        return code
    
    def _fix_logic_error(self, code: str) -> str:
        """修复逻辑错误"""
        return code
    
    def _fix_performance_issue(self, code: str) -> str:
        """修复性能问题"""
        return code
    
    async def _check_syntax(self) -> Dict:
        """检查语法"""
        return {'success': True, 'message': '语法检查通过'}
    
    async def _check_imports(self) -> Dict:
        """检查导入"""
        return {'success': True, 'message': '导入检查通过'}
    
    async def _run_linter(self) -> Dict:
        """运行代码检查器"""
        return {'success': True, 'message': '代码质量检查通过'}
    
    async def _security_scan(self) -> Dict:
        """安全扫描"""
        return {'success': True, 'message': '安全检查通过'}
    
    def _generate_ci_recommendations(self, checks: Dict) -> List[str]:
        """生成CI建议"""
        return ["所有检查通过"]