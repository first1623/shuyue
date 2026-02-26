---
name: prompt-collector
description: This skill should be used when users need to collect, organize, and reuse prompts across projects. It automatically scans project files, extracts embedded prompts, categorizes them by purpose, and creates a centralized prompt library for easy discovery and reuse in future projects.
---

# Prompt Collector Skill

This skill transforms Claude into an intelligent prompt curator capable of automatically discovering, organizing, and managing prompts scattered across project files for maximum reusability.

## Purpose

To provide comprehensive prompt discovery and organization capabilities across projects. The skill scans various file types, extracts embedded prompts, analyzes their purposes, categorizes them intelligently, and builds a searchable prompt library that can be easily reused in new projects or contexts.

## When to Use This Skill

Use this skill when:
- Starting a new project and wanting to leverage existing prompts from previous work
- Need to audit and organize prompts scattered across multiple project files
- Want to create a centralized prompt library for team or personal use
- Refactoring projects and need to consolidate prompts in dedicated locations
- Onboarding new projects and want to quickly identify available prompt patterns
- Searching for specific types of prompts used in past projects (e.g., "debugging prompts", "code review prompts")
- Building prompt templates for common workflows

## How to Use This Skill

### Core Workflow

When tasked with prompt collection and organization:

1. **Scan Project Structure**: Analyze the project directory to identify all relevant files and directories
2. **Extract Embedded Prompts**: Scan files for common prompt patterns and embedded instructions
3. **Classify and Categorize**: Analyze prompt content and purpose to assign categories and tags
4. **Create Centralized Library**: Organize collected prompts into a structured, searchable format
5. **Generate Reuse Templates**: Create ready-to-use prompt templates with proper context placeholders
6. **Update Project Metadata**: Optionally embed prompt references back into project files for traceability

### Key Capabilities

#### 1. Multi-Format Prompt Discovery

Scan and extract prompts from various sources:
- Code comments containing prompt-like instructions
- Documentation files (README.md, docs/, wikis)
- Configuration files with embedded instructions
- Script headers and inline documentation
- Issue descriptions and PR templates
- Meeting notes and project documentation
- Chat logs and collaboration files

#### 2. Intelligent Content Analysis

Understand and classify prompts by:
- Purpose (debugging, code generation, review, testing, documentation)
- Domain (frontend, backend, DevOps, data science, etc.)
- Complexity level (simple, intermediate, advanced)
- Context requirements (project-specific, generic, reusable)
- Usage frequency patterns

#### 3. Automated Organization

Create structured prompt libraries:
- Hierarchical categorization by purpose and domain
- Tag-based indexing for flexible searching
- Version tracking for prompt evolution
- Usage statistics and popularity metrics
- Cross-project prompt relationship mapping

#### 4. Smart Reuse Generation

Transform discovered prompts into reusable assets:
- Template generation with placeholder substitution
- Context-aware prompt adaptation
- Parameterized prompt variants for different scenarios
- Integration with project-specific configurations
- Export in multiple formats (markdown, JSON, YAML)

### Implementation Notes

This skill operates through the PromptCollector class which provides:
- `scan_project_for_prompts(project_path, file_types)` - Discover prompts across project files
- `extract_prompts_from_file(file_path)` - Extract prompts from individual files
- `analyze_prompt_purpose(prompt_content)` - Classify prompts by purpose and domain
- `create_prompt_library(prompts, organization_style)` - Build organized prompt library
- `generate_reuse_templates(library, template_format)` - Create ready-to-use templates
- `search_prompts(library, criteria)` - Search and filter prompts by various criteria
- `export_prompt_library(library, export_path, format)` - Export library in specified format

The skill maintains prompt discovery history and learns from usage patterns to improve classification accuracy over time.

### Usage Pattern

When user requests prompt collection or organization:

1. **Scope Definition**: Clarify project scope and file types to include in scan
2. **Discovery Phase**: Scan project files and extract all potential prompts
3. **Analysis Phase**: Analyze and categorize each discovered prompt
4. **Organization Phase**: Create structured library with intelligent categorization
5. **Template Generation**: Convert prompts to reusable templates with proper context handling
6. **Library Presentation**: Display organized prompt library with search and filtering options
7. **Export Options**: Provide multiple export formats and integration options

For ongoing prompt management:
- Schedule regular scans for active projects
- Track prompt usage and effectiveness
- Suggest prompt improvements and consolidations
- Maintain prompt version history and evolution tracking

Focus on identifying implicit prompts in code comments, documentation patterns, and workflow instructions that represent valuable knowledge that should be systematically captured and made reusable.