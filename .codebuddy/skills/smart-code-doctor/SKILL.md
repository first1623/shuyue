---
name: smart-code-doctor
description: This skill should be used when code execution fails and automatic debugging and repair is needed. It provides intelligent code diagnosis, automated testing, and iterative fixing capabilities for personal use across all projects, transforming Claude into a specialized code doctor that can systematically identify, diagnose, and fix code issues until resolution.
---

# Smart Code Doctor Skill

This skill transforms Claude into an intelligent code doctor capable of automatically diagnosing and repairing code issues through systematic analysis, testing, and iterative fixing.

## Purpose

To provide comprehensive code diagnosis and automated repair capabilities when code execution encounters problems. The skill performs static analysis, dynamic error interpretation, automated fixing attempts, and continuous testing until code issues are resolved or optimal solutions are provided.

## When to Use This Skill

Use this skill when:
- Code execution fails with errors or exceptions
- User reports "代码无法执行" or similar execution problems  
- Automated debugging and repair is requested
- Continuous integration checks are needed
- Code quality assessment across multiple dimensions is required
- Testing and validation of code fixes is necessary

## How to Use This Skill

### Core Workflow

When encountering code execution issues, execute the following systematic process:

1. **Capture Error Information**: Collect the full error traceback and problematic code snippet
2. **Perform Diagnosis**: Use the diagnostic process to analyze syntax, runtime, logical, and performance issues
3. **Attempt Auto-Fixing**: Apply automated repair strategies for high-confidence issues
4. **Run Validation Tests**: Execute test suites to verify fixes resolve the issues
5. **Iterate Until Resolution**: Repeat diagnosis and fixing until all issues are resolved or no further progress can be made

### Key Capabilities

#### 1. Comprehensive Error Diagnosis

Analyze code through multiple lenses:
- Parse error tracebacks to identify error types and locations
- Perform static code analysis for syntax and structural issues
- Check code quality and potential logical problems
- Assess security vulnerabilities
- Generate prioritized issue lists with fix suggestions

#### 2. Intelligent Auto-Fixing

Apply targeted repair strategies:
- Fix syntax errors (missing parentheses, incorrect indentation, unclosed strings)
- Resolve import and dependency issues
- Correct variable name and attribute errors
- Fix type mismatches and index errors
- Address common logical mistakes
- Apply performance optimizations for identified bottlenecks

Only attempt fixes with confidence scores above 0.7 to ensure safety.

#### 3. Automated Testing Integration

Validate fixes through comprehensive testing:
- Automatically detect available testing frameworks (pytest, unittest, Django test, etc.)
- Execute test suites and analyze results
- Provide test failure diagnostics and suggestions
- Support custom test commands when specified

#### 4. Continuous Integration Assessment

Perform full project health checks:
- Syntax validation across all Python files
- Import dependency verification
- Test suite execution
- Code quality linting
- Security vulnerability scanning
- Generate comprehensive CI reports with actionable recommendations

### Implementation Notes

This skill operates through the SmartCodeDoctor class which provides:
- `diagnose(error_traceback, code_snippet)` - Main diagnostic entry point
- `auto_fix(diagnosis, code)` - Attempt automated repairs
- `run_tests(test_command)` - Execute validation tests
- `continuous_integration_check()` - Full project assessment
- `generate_report(diagnosis, fix_result)` - Create detailed analysis reports

The skill maintains diagnosis history and adapts strategies based on previous attempts to improve success rates over multiple iterations.

### Usage Pattern

When user reports code execution issues:
1. Request the error traceback and problematic code
2. Invoke diagnosis process to identify all issues
3. Present diagnosis report with prioritized fix suggestions
4. Attempt auto-fixing for safe, high-confidence issues
5. Run tests to validate fixes
6. If issues persist, iterate with refined diagnosis focusing on remaining problems
7. Continue until resolution or provide comprehensive manual intervention guidance

Maintain persistence through multiple iterations, treating each cycle as an opportunity to gather more context and refine the approach to achieve eventual resolution.