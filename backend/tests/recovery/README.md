# 异常恢复测试套件

## 概述

本测试套件用于验证知识图谱系统的异常恢复能力，确保系统在各种故障场景下能够正确检测、处理和恢复。

## 测试模块

### 1. 数据库恢复测试 (`test_database_recovery.py`)
- PostgreSQL连接断开后重连
- 连接池耗尽场景处理
- 查询超时恢复
- 事务回滚验证
- Neo4j连接恢复
- 数据完整性检查

### 2. API恢复测试 (`test_api_recovery.py`)
- API超时重试机制
- 速率限制恢复
- 熔断器模式验证
- 服务降级处理
- 指数退避重试
- 舱壁隔离模式
- DeepSeek API故障恢复

### 3. 服务恢复测试 (`test_service_recovery.py`)
- 服务健康检查
- 内存使用监控
- 内存泄漏检测
- CPU使用监控
- 文件描述符泄漏检测
- 线程泄漏检测
- 优雅关闭处理
- 进程恢复

### 4. 网络恢复测试 (`test_network_recovery.py`)
- 连接被拒绝恢复
- DNS解析失败处理
- 网络超时恢复
- 连接重置恢复
- SSL证书错误处理
- 代理服务器故障恢复
- 重试策略验证
- 网络分区检测

### 5. 数据恢复测试 (`test_data_recovery.py`)
- 数据校验和验证
- 数据损坏检测
- 数据一致性检查
- 备份创建与恢复
- 增量备份
- 灾难恢复（RPO/RTO）
- 数据迁移

### 6. 集成测试 (`test_recovery_integration.py`)
- 完整恢复工作流
- 级联故障恢复
- 并发故障处理
- 优雅降级
- 自动恢复时机
- 恢复指标计算
- 事件报告与审计

## 运行方式

### 运行所有测试
```bash
python run_recovery_tests.py --mode all
```

### 快速测试（仅关键测试）
```bash
python run_recovery_tests.py --mode quick
```

### 运行特定模块测试
```bash
# 数据库恢复测试
python run_recovery_tests.py --mode database

# API恢复测试
python run_recovery_tests.py --mode api

# 网络恢复测试
python run_recovery_tests.py --mode network
```

### 使用pytest直接运行
```bash
# 运行所有恢复测试
pytest backend/tests/recovery/ -v -s

# 运行单个测试文件
pytest backend/tests/recovery/test_database_recovery.py -v -s

# 运行特定测试
pytest backend/tests/recovery/test_api_recovery.py::TestAPIRecovery::test_api_timeout_retry -v -s
```

## 验收标准

| 测试类别 | 验收标准 |
|---------|---------|
| 数据库恢复 | 故障后3次重试内恢复 |
| API恢复 | 熔断器正确切换，降级数据可用 |
| 服务恢复 | 内存增长<100MB/100请求，无资源泄漏 |
| 网络恢复 | 指数退避重试成功，代理切换正常 |
| 数据恢复 | RPO<1小时，RTO<30分钟 |
| 集成测试 | 完整工作流通过，可用性>99.9% |

## 关键指标

- **MTTR (Mean Time To Repair)**: 平均修复时间 < 5分钟
- **MTTF (Mean Time To Failure)**: 平均故障间隔 > 720小时
- **可用性**: > 99.9%
- **恢复成功率**: > 95%

## 故障场景覆盖

1. ✅ 数据库连接断开
2. ✅ 数据库查询超时
3. ✅ API请求超时
4. ✅ API速率限制
5. ✅ 外部服务不可用
6. ✅ 网络中断
7. ✅ DNS解析失败
8. ✅ 内存溢出
9. ✅ 连接池耗尽
10. ✅ 数据损坏

## 注意事项

1. 部分测试需要真实的数据库连接
2. 内存泄漏测试可能需要较长时间
3. 网络测试在离线环境可能需要模拟
4. 建议在CI/CD中定期运行完整测试套件
