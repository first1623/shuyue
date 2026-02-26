# Project Analyzer Skill - Usage Guide

## Overview

The Project Analyzer skill automatically generates comprehensive requirement lists for any project directory, including hierarchical functional points (primary, secondary, tertiary), detailed descriptions, system interaction methods, and data source mappings.

## Quick Start

### Basic Workflow

When you need to analyze a project and generate requirements:

1. **Target Specification**: Point to the project directory you want to analyze
2. **Analysis Execution**: Run the automated project analysis process
3. **Requirement Generation**: Get structured requirement lists with all specified elements
4. **Review & Refine**: Examine the generated requirements and customize as needed
5. **Export & Use**: Save the requirements in your preferred format for project planning

### Example Usage Scenarios

#### Scenario 1: New Project Onboarding
```
User: "帮我分析这个项目目录，生成完整的需求列表"
Target: /path/to/new/project

System Action:
1. Scan entire project structure and file organization
2. Identify functional modules and business domains
3. Create primary/secondary/tertiary functional hierarchy
4. Generate detailed requirements for each functional point
5. Map system interactions and data sources
6. Output comprehensive requirement specification
```

#### Scenario 2: Legacy System Documentation
```
User: "为这个老项目生成需求规格说明书"
Target: /path/to/legacy/system

System Action:
1. Analyze existing code structure and patterns
2. Extract implicit requirements from implementation
3. Document current functionality hierarchy
4. Identify data flows and system dependencies
5. Generate formal requirement documentation
```

#### Scenario 3: Impact Analysis for Changes
```
User: "分析这个项目，看看添加用户权限功能需要影响哪些现有功能"
Target: /path/to/current/project
Focus: USER_MANAGEMENT functional area

System Action:
1. Map current USER_MANAGEMENT functionality
2. Identify related data sources and API endpoints
3. Analyze system interaction patterns
4. Predict impact on existing functional points
5. Generate change impact assessment
```

## Output Structure

### Primary Functional Points (Level 1)
Major business domains and core capabilities:
- **USER_MANAGEMENT**: 用户管理 - 系统的用户注册、登录、权限管理等核心功能
- **CONTENT_MANAGEMENT**: 内容管理 - 内容的创建、编辑、发布、审核等管理功能
- **DATA_PROCESSING**: 数据处理 - 数据的采集、清洗、分析、存储等处理功能
- **INTEGRATION_SERVICE**: 集成服务 - 与外部系统的集成和数据交换功能
- **REPORT_ANALYTICS**: 报表分析 - 数据统计、报表生成、分析洞察功能
- **SYSTEM_ADMIN**: 系统管理 - 系统配置、监控、维护等管理功能

### Secondary Functional Points (Level 2)
Subsystems and major feature groups within each domain:
- **AUTH_LOGIN**: 身份认证 - 用户登录、登出、会话管理
- **USER_REGISTRY**: 用户注册 - 新用户注册、信息完善
- **CONTENT_CREATE**: 内容创建 - 新建各类业务内容
- **DATA_COLLECTION**: 数据采集 - 从多源收集业务数据

### Tertiary Functional Points (Level 3)
Specific operations and detailed features:
- **AUTH_PASSWORD_LOGIN**: 密码登录 - 用户使用用户名密码进行身份验证
- **CREATE_DRAFT**: 创建草稿 - 创建未发布的内容草稿
- **COLLECT_API_DATA**: API数据采集 - 通过REST API获取外部数据

## Detailed Requirement Components

### Requirement Description
Each functional point includes:
- **Comprehensive Description**: Clear explanation of what the function does
- **Business Context**: How it fits into overall business processes
- **Success Criteria**: Definition of successful operation
- **Constraints**: Limitations and boundary conditions

### System Invocation Method
Defines how each function is called:
- **Entry Points**: APIs, user interfaces, scheduled jobs
- **Communication Protocols**: HTTP/HTTPS, RPC, Message Queue
- **Authentication**: Required credentials and authorization levels
- **Performance Requirements**: Response time and throughput expectations

### Data Sources
Identifies all data inputs:
- **Primary Sources**: Main data providers (databases, APIs, files)
- **Secondary Sources**: Supporting data (configurations, caches)
- **External Sources**: Third-party data providers
- **Real-time vs Batch**: Data freshness requirements

### API Endpoints
Documents interface contracts:
- **REST Endpoints**: URL patterns and HTTP methods
- **Request Parameters**: Required and optional parameters
- **Response Formats**: Standard response structures
- **Error Codes**: Expected error conditions and handling

### Database Tables
Maps data persistence:
- **Primary Tables**: Main data storage tables
- **Relationship Tables**: Join and association tables
- **Audit Tables**: Logging and historical data
- **Indexing Strategy**: Performance optimization approaches

### External Services
Identifies system dependencies:
- **Third-party APIs**: External service integrations
- **Infrastructure Services**: Cloud services and platforms
- **Internal Services**: Other microservices or applications
- **Communication Patterns**: Sync vs async interaction modes

### User Interactions
Describes human-computer interaction:
- **Input Methods**: Forms, file uploads, voice commands
- **Feedback Mechanisms**: Progress indicators, notifications
- **Error Handling**: User-friendly error messages
- **Accessibility**: Support for assistive technologies

## Analysis Methodology

### Automatic Feature Detection
The skill uses multiple techniques to identify functionality:

1. **Directory Structure Analysis**: Infers functionality from folder organization
2. **File Naming Patterns**: Recognizes functional areas from file names
3. **Code Pattern Recognition**: Identifies business logic from code structures
4. **Configuration Analysis**: Understands integrations from config files
5. **Documentation Mining**: Extracts requirements from existing docs

### Intelligent Classification
Functions are classified using:
- **Domain Knowledge**: Industry-standard functional categories
- **Naming Conventions**: Common patterns in function and class names
- **Architecture Patterns**: MVC, Microservices, Event-driven patterns
- **Business Logic Inference**: From code comments and documentation

### Hierarchy Construction
Functional decomposition follows:
- **Business Domain First**: Top-down approach starting with business areas
- **Use Case Driven**: Based on typical user workflows
- **Dependency Analysis**: Considering functional interdependencies
- **Granularity Balance**: Appropriate detail level for each level

## Customization Options

### Analysis Scope
Customize what gets analyzed:
- **Include/Exclude Directories**: Skip irrelevant folders
- **File Type Focus**: Emphasize specific technology stacks
- **Depth Control**: Limit analysis to certain directory levels
- **Historical Analysis**: Include git history for evolution insights

### Output Customization
Tailor the generated requirements:
- **Detail Level**: Brief overview vs comprehensive specification
- **Format Preference**: Structured text, Markdown, JSON, Excel
- **Audience Targeting**: Technical teams vs business stakeholders
- **Compliance Standards**: ISO, IEEE, or custom requirement formats

### Domain Adaptation
Adapt to specific industries:
- **Web Applications**: Focus on user interfaces and APIs
- **Data Processing**: Emphasize ETL and analytics pipelines
- **Mobile Apps**: Highlight device-specific features
- **Enterprise Systems**: Stress integration and security aspects

## Integration Workflows

### With Development Process
1. **Sprint Planning**: Use requirements for story breakdown
2. **Code Review**: Verify implementation against requirements
3. **Testing Strategy**: Align test cases with requirement coverage
4. **Release Planning**: Prioritize features based on requirements

### With Project Management
1. **Work Breakdown**: Convert functional points to work packages
2. **Resource Estimation**: Use complexity analysis for effort estimation
3. **Risk Assessment**: Identify technical risks from requirements
4. **Progress Tracking**: Monitor completion against requirement status

### With Quality Assurance
1. **Test Coverage**: Ensure all requirements have corresponding tests
2. **Traceability Matrix**: Link requirements to test cases
3. **Defect Analysis**: Map bugs back to requirement gaps
4. **Compliance Verification**: Validate regulatory requirement coverage

## Best Practices

### Before Analysis
1. **Clean Repository State**: Ensure latest code is checked out
2. **Build Successful**: Verify project compiles without errors
3. **Environment Setup**: Configure analysis tools and dependencies
4. **Scope Definition**: Clearly define analysis boundaries and objectives

### During Analysis
1. **Review Initial Results**: Validate automatic classifications
2. **Provide Context**: Add business domain knowledge when possible
3. **Iterative Refinement**: Run analysis multiple times with adjustments
4. **Stakeholder Input**: Incorporate domain expert knowledge

### After Analysis
1. **Validate Completeness**: Check for missing functionality
2. **Prioritize Requirements**: Rank by business value and risk
3. **Establish Baselines**: Create reference points for future comparisons
4. **Plan Maintenance**: Schedule regular requirement updates

## Limitations and Considerations

### Analysis Accuracy
- **Pattern Dependency**: Relies on recognizable code and naming patterns
- **Documentation Gaps**: May miss undocumented implicit requirements
- **Context Limitations**: Cannot infer business context without hints
- **Technology Constraints**: Better support for common frameworks and languages

### Generated Content
- **Starting Point**: Generated requirements are baseline, not final specification
- **Human Review Required**: Expert validation needed for accuracy and completeness
- **Evolution Necessary**: Requirements evolve with business and technical changes
- **Customization Needed**: May require adaptation for specific organizational needs

### Performance Considerations
- **Large Codebases**: Analysis time increases with project size
- **Complex Dependencies**: Deep dependency chains may slow analysis
- **Resource Intensive**: Memory and CPU usage scales with project complexity
- **Incremental Analysis**: Consider analyzing changed portions only for large projects

Focus on using the generated requirements as a foundation for deeper analysis and stakeholder collaboration to create truly comprehensive and accurate project specifications.