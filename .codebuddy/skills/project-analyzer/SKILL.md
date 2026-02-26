---
name: project-analyzer
description: This skill should be used when users need to analyze project directories and automatically generate comprehensive requirement lists with hierarchical functional points, detailed descriptions, system interaction methods, and data source mappings for each project.
allowed-tools: 
disable: false
---

# Project Analyzer Skill

This skill transforms Claude into an intelligent project analyst capable of automatically scanning project structures, analyzing code patterns, extracting business logic, and generating detailed requirement specifications with multi-level functional decomposition.

## Purpose

To provide comprehensive project analysis and automated requirement generation capabilities across all projects. The skill examines project directories, analyzes file structures, code implementations, configuration files, and documentation to produce structured requirement lists with primary, secondary, and tertiary functional points, detailed descriptions, system invocation methods, and data source mappings.

## When to Use This Skill

Use this skill when:
- Starting analysis of a new project and needing comprehensive requirement documentation
- Creating requirement specifications for existing projects without formal documentation
- Auditing project functionality and identifying gaps in requirement coverage
- Generating requirement traceability matrices for project planning
- Onboarding new team members who need project overview and requirements
- Comparing actual implementation against intended requirements
- Preparing project documentation for stakeholders or clients
- Conducting impact analysis for proposed feature changes

## How to Use This Skill

### Core Workflow

When tasked with project requirement analysis:

1. **Project Structure Scan**: Analyze the complete directory tree and file organization
2. **Code Pattern Analysis**: Examine source code to identify functional modules and business logic
3. **Configuration Mapping**: Parse configuration files to understand system integrations and settings
4. **Documentation Extraction**: Extract requirements and specifications from existing docs
5. **Functional Decomposition**: Break down identified functionalities into hierarchical levels
6. **Requirement Synthesis**: Generate detailed requirement descriptions for each functional point
7. **System Interaction Mapping**: Define how each function interacts with external systems and APIs
8. **Data Source Identification**: Map data inputs, outputs, and storage mechanisms
9. **Report Generation**: Create comprehensive requirement documentation with all specified elements

### Key Capabilities

#### 1. Multi-Level Functional Analysis

Decompose project functionality hierarchically:
- **Primary Functions**: Major business domains and core capabilities (Level 1)
- **Secondary Functions**: Subsystems and major feature groups within each domain (Level 2)
- **Tertiary Functions**: Specific operations and detailed features within subsystems (Level 3)
- **Implementation Mapping**: Link functional points to actual code files and modules

#### 2. Intelligent Requirement Extraction

Automatically derive requirements from:
- Code comments and docstrings containing requirement indicators
- Function and class names suggesting business functionality
- API endpoint definitions and routing configurations
- Database schema and migration files
- Configuration files indicating external system integrations
- Test cases demonstrating expected system behavior
- Error handling patterns revealing business rules and constraints

#### 3. System Interaction Modeling

Document how functions interact with:
- External APIs and third-party services
- Database systems and data stores
- File systems and local storage
- Network services and communication protocols
- User interfaces and presentation layers
- Background job processors and schedulers
- Authentication and authorization systems

#### 4. Data Flow Analysis

Map complete data lifecycle for each function:
- **Input Sources**: User input, API calls, database queries, file uploads, sensor data
- **Processing Logic**: Business rules, calculations, transformations, validations
- **Output Destinations**: Database storage, API responses, file generation, UI updates
- **Data Transformations**: Format conversions, aggregations, filters, enrichments
- **Storage Mechanisms**: Database tables, cache layers, file systems, external services

### Implementation Notes

This skill operates through the ProjectAnalyzer class which provides:
- `analyze_project_structure(project_path)` - Scan and map complete project architecture
- `extract_functional_modules(files_analysis)` - Identify distinct functional areas and modules
- `decompose_functional_hierarchy(functional_map)` - Create primary/secondary/tertiary breakdown
- `generate_requirement_descriptions(functional_points)` - Synthesize detailed requirement specs
- `map_system_interactions(functional_analysis)` - Document external system communications
- `identify_data_sources(functional_points, code_analysis)` - Trace data flow and storage
- `generate_requirement_report(analysis_results, format_type)` - Create comprehensive documentation
- `validate_requirement_coverage(requirements, codebase)` - Ensure completeness and accuracy

The skill maintains analysis history and learns from project patterns to improve requirement extraction accuracy over time, particularly for common architectural patterns and industry domains.

### Usage Pattern

When user requests project requirement analysis:

1. **Scope Definition**: Clarify target project directory and analysis depth
2. **Structure Analysis**: Scan project files, directories, and architectural patterns
3. **Function Identification**: Extract functional modules from code structure and naming patterns
4. **Hierarchy Creation**: Decompose functions into primary, secondary, and tertiary levels
5. **Requirement Documentation**: Generate detailed descriptions for each functional point
6. **Interaction Mapping**: Define system calls, API interactions, and external dependencies
7. **Data Flow Analysis**: Identify data sources, transformations, and storage mechanisms
8. **Report Compilation**: Assemble all elements into structured requirement documentation
9. **Validation Review**: Check requirement completeness and suggest additional analysis areas

For ongoing project management:
- Schedule regular requirement analysis for active development projects
- Track requirement evolution as code changes occur
- Compare intended vs. implemented functionality
- Generate requirement traceability reports for compliance
- Support impact analysis for proposed modifications

Focus on identifying implicit requirements in code patterns, configuration settings, and architectural decisions that represent business logic and user needs not explicitly documented but critical for system understanding.