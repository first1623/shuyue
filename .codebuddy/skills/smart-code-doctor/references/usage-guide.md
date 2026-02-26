# Smart Code Doctor Skill - Usage Guide

## Quick Start

When code execution fails, follow this systematic approach:

### 1. Capture Error Information
```
User Input Needed:
- Full error traceback (copy from console/output)
- Problematic code snippet or file content
- Context about what the code is supposed to do
```

### 2. Execute Diagnosis
```python
from scripts.smart_code_doctor import SmartCodeDoctor

# Initialize the code doctor
doctor = SmartCodeDoctor()

# Run diagnosis
diagnosis = await doctor.diagnose(error_traceback, code_snippet)

# Display report
print(doctor.generate_report(diagnosis))
```

### 3. Attempt Auto-Fixing
```python
# Try automatic fixes
fix_result = await doctor.auto_fix(diagnosis, code_snippet)

if fix_result['success']:
    print("修复成功!")
    print(fix_result['fixed_code'])
else:
    print("无法自动修复，需要手动干预")
```

### 4. Validate with Testing
```python
# Run tests to verify fixes
test_result = await doctor.run_tests()

if test_result['success']:
    print("✅ 测试通过，问题解决")
else:
    print("❌ 测试失败，需要进一步调试")
```

### 5. Iterate Until Resolution
Repeat steps 2-4 until:
- All tests pass
- No more high-confidence fixes available
- Manual intervention required

## Common Error Patterns

### Syntax Errors
- Missing parentheses in print statements
- Incorrect indentation
- Unclosed strings or brackets
- Missing colons after control structures

### Runtime Errors
- **NameError**: Undefined variables
- **TypeError**: Data type mismatches  
- **IndexError**: Out-of-bounds list access
- **ImportError**: Missing modules
- **AttributeError**: Invalid method/property access
- **KeyError**: Missing dictionary keys
- **ValueError**: Invalid parameter values

### Logic Errors
- Infinite loops
- Off-by-one errors
- Incorrect algorithm implementation
- Wrong variable assignments

## Best Practices

1. **Always capture full traceback** - Partial errors lose context
2. **Provide code context** - More code helps identify root causes
3. **Test incrementally** - Fix one issue at a time when possible
4. **Review auto-fixes** - High confidence ≠ always correct
5. **Persist through iterations** - Multiple rounds often needed

## Integration with Claude Workflow

When user says "代码无法执行" or reports execution errors:

1. **Immediate Response**: Acknowledge the issue and request error details
2. **Information Gathering**: Collect traceback and problematic code
3. **Skill Activation**: Load SmartCodeDoctor and execute diagnosis
4. **Solution Presentation**: Show diagnosis report with fix suggestions
5. **Automated Repair**: Attempt safe auto-fixes
6. **Validation**: Run tests to verify resolution
7. **Iteration**: Continue until problem solved or manual guidance needed

## Limitations

- Auto-fixes only attempted for confidence > 0.7
- Complex logical errors may require manual intervention
- External dependencies and environment issues need manual resolution
- Some syntax errors require contextual understanding beyond static analysis