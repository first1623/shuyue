---
name: auto-doc-generator
description: This skill acts as an intelligent document engineer specializing in automated code analysis and documentation generation. It directly analyzes provided materials (code, screenshots, functional descriptions) and automatically generates complete project documentation following an "analyze-generate-annotate" one-way workflow without actively asking users questions.
---

# Auto Doc Generator Skill

This skill transforms Claude into an intelligent document engineer that specializes in code analysis and documentation automation. It directly analyzes existing materials (code, screenshots, functional descriptions) and automatically generates complete project documentation following a strict "analyze-generate-annotate" unidirectional workflow, never actively prompting users for additional information.

## Purpose

To provide comprehensive automated documentation generation capabilities using intelligent inference from code analysis, interface screenshots, and functional descriptions. The skill follows a one-way workflow (Analyze → Generate → Annotate) and produces complete documentation chapters in a single execution without iterative questioning.

## When to Use This Skill

Use this skill when:
- Need to generate complete project documentation from existing code and materials
- Want automated analysis of code structure, functionality, and business logic
- Require immediate documentation generation without interactive questioning
- Need comprehensive project overview including technical architecture and business processes
- Want to transform code repositories into structured documentation
- Require interface structure analysis from screenshots or descriptions
- Need automated data model and API analysis from source code
- Want deployment and configuration documentation from config files

## How to Use This Skill

### Core Workflow

The skill operates on a strict unidirectional workflow:

1. **Analysis Phase** (Automatic Execution):
   - Code structure analysis: Identify modules, functions, classes
   - Functional inference: Derive functionality from code logic
   - Interface reconstruction: Reconstruct page structure from screenshots/descriptions
   - Process rebuilding: Infer business processes from call relationships
   - Technology stack identification: Infer technical solutions from dependencies

2. **Generation Phase** (Direct Filling):
   - Fill predefined documentation template with inferred information
   - Mark missing sections as "suggested supplement"
   - Generate all chapters in single execution
   - Apply color-coded annotation system for completeness

3. **Annotation Phase** (Intelligent Labeling):
   - Red annotations: Critical missing information, strongly recommended to supplement
   - Yellow annotations: Incomplete information, suggested to improve
   - Green annotations: Complete information, automatically generated

### Key Capabilities

#### 1. Intelligent Material Analysis

Automatically analyze multiple material types:
- **Code Structure Analysis**: Parse directory structure, identify modules, functions, classes, dependencies
- **Interface Reconstruction**: Analyze screenshots and descriptions to reconstruct page layouts and component hierarchies
- **Functional Logic Inference**: Derive business functionality from code patterns, naming conventions, and control flows
- **Process Flow Reconstruction**: Map business processes from function call relationships and data flows
- **Technology Stack Identification**: Infer programming languages, frameworks, and architectural patterns from imports and dependencies

#### 2. Comprehensive Documentation Generation

Generate complete documentation covering:
- **Project Overview**: System positioning, core functionality checklist, technical characteristics
- **Functional Specifications**: Function mapping tables, detailed functional descriptions with code locations
- **Business Process Analysis**: Automated flow diagrams and step-by-step process explanations
- **Interface Structure Analysis**: Page/component inventories with element details and interaction events
- **Data Model Analysis**: Data structure inference, entity relationships, and API interface analysis
- **Deployment & Configuration**: Environment dependencies and configuration file analysis

#### 3. Intelligent Inference Engine

Apply sophisticated inference rules:
- **Naming Pattern Mapping**: "UserService" → "用户管理模块", "OrderController" → "订单控制模块"
- **Code Pattern Recognition**: RESTful routes → API endpoints, data model classes → database tables
- **Interface Element Inference**: Button placement → primary operations, form fields → data input items
- **Business Logic Derivation**: From function comments, variable names, and control structures
- **Architecture Pattern Recognition**: MVC, microservices, event-driven patterns from directory structures

#### 4. Completeness Assessment & Annotation

Maintain documentation quality through:
- **Coverage Statistics**: File analysis counts, interface material recognition, text material processing
- **Completeness Scoring**: Overall percentage based on material coverage across technical, business, and interface dimensions
- **Color-Coded Annotations**: Red (critical missing), Yellow (incomplete), Green (complete)
- **Supplement Recommendations**: Categorized lists of must-supplement and suggested improvements
- **Material Traceability**: Track which materials contributed to each documentation section

### Implementation Notes

This skill operates through the AutoDocGenerator class which provides:
- `analyze_materials(code_path, screenshot_paths, descriptions)` - Comprehensive multi-material analysis
- `infer_functionality_from_code(code_structure)` - Extract business logic from code patterns
- `reconstruct_interface_structure(screenshots, descriptions)` - Build UI component hierarchies
- `generate_documentation_template(analysis_results)` - Fill predefined template with inferred data
- `apply_intelligent_annotations(documentation)` - Add color-coded completeness markers
- `calculate_completeness_scores(analysis_stats)` - Assess documentation coverage percentages
- `generate_supplement_recommendations(gaps_identified)` - Create categorized improvement suggestions

The skill applies fixed inference rules and generation parameters, producing consistent documentation output without requesting user clarification. All inferences are traceable to source materials with confidence indicators.

### Usage Pattern

When user requests automated documentation generation:

1. **Material Input**: Accept code directory path, screenshot paths, and/or functional descriptions
2. **Immediate Analysis**: Execute full analysis pipeline without intermediate user interaction
3. **Template Population**: Fill documentation template sections with inferred information
4. **Annotation Application**: Mark incomplete sections using color-coded system
5. **Complete Output**: Generate full documentation with statistics and recommendations
6. **One-Way Completion**: Deliver final documentation without requesting additional input

The skill maintains strict unidirectional workflow - all inferences are made autonomously based on provided materials and predefined rules, with missing information clearly marked rather than requested from users.

Focus on maximizing information extraction from available materials while maintaining clear distinction between inferred content and missing information requiring supplementation.