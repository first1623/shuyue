# Prompt Collector Skill - Usage Guide

## Quick Start

### Basic Workflow

When you need to collect and organize prompts across projects:

1. **Specify Target Project**: Point to the project directory you want to scan
2. **Define Scope**: Choose file types and areas to include/exclude
3. **Execute Collection**: Run the prompt discovery process
4. **Review Results**: Examine discovered prompts and their classifications
5. **Organize Library**: Create structured prompt library with desired organization
6. **Generate Templates**: Convert prompts to reusable templates
7. **Export & Reuse**: Save library in preferred format for future use

### Example Usage Scenarios

#### Scenario 1: New Project Setup
```
User: "帮我为新项目收集之前用过的调试相关的提示词"

System Action:
1. Scan current and previous projects for debugging prompts
2. Filter by purpose='debugging'
3. Create organized library with debugging templates
4. Export ready-to-use prompt templates
```

#### Scenario 2: Code Review Process Improvement
```
User: "我想整理项目中所有的代码审查提示词"

System Action:
1. Scan project documentation and code comments
2. Extract prompts with purpose='review'
3. Categorize by domain (frontend/backend/devops)
4. Generate standardized review prompt templates
```

#### Scenario 3: Team Knowledge Consolidation
```
User: "帮我把团队所有项目中的API开发提示词收集起来"

System Action:
1. Scan multiple project directories
2. Filter by domain='backend' and keywords=['api']
3. Create comprehensive API development prompt library
4. Export in team-shareable format
```

## Advanced Features

### Multi-Level Pattern Recognition

The skill recognizes prompts in various contexts:

#### Code Comments
- `# Prompt: Fix memory leak in data processing`
- `// Instruction: Implement caching strategy for API responses`
- `/* Guide: Set up Docker container for development */`

#### Documentation
- `## Prompt\nDebug authentication issues by checking...`
- `**Instruction**: Review code for security vulnerabilities`
- `> Note: Use consistent naming conventions throughout`

#### Configuration Files
- JSON: `{"prompt": "Generate unit tests for new features"}`
- YAML: `instruction: Validate input data before processing`

#### Generic Text Files
- TODO comments with detailed instructions
- Meeting notes with action items
- Issue descriptions with solution guidance

### Intelligent Classification

Prompts are automatically analyzed and tagged:

#### Purpose Categories
- **debugging**: Fix errors, troubleshoot issues, bug resolution
- **code_generation**: Create new code, implement features, build components
- **review**: Code examination, quality checks, security audits
- **testing**: Test creation, validation, mock setup
- **documentation**: Explain code, write docs, create comments
- **planning**: Design systems, architecture decisions, project organization

#### Domain Classifications
- **frontend**: React, Vue, CSS, UI/UX related prompts
- **backend**: API, database, server, service prompts
- **devops**: Deployment, Docker, CI/CD, infrastructure prompts
- **data_science**: ML models, data analysis, algorithm prompts
- **mobile**: iOS, Android, cross-platform development prompts
- **security**: Authentication, encryption, vulnerability prompts

#### Complexity Levels
- **simple**: Under 15 words, basic instructions
- **intermediate**: 15-50 words, moderate complexity
- **advanced**: Over 50 words, complex multi-step processes

## Search and Filter Capabilities

### Search Criteria
```python
# Search by purpose
criteria = {'purpose': 'debugging'}

# Search by domain and complexity
criteria = {'domain': 'frontend', 'complexity': 'intermediate'}

# Search by tags
criteria = {'tags': ['react', 'testing']}

# Keyword search
criteria = {'keyword': 'authentication'}

# Combined criteria
criteria = {
    'purpose': 'review',
    'domain': 'backend',
    'tags': ['api', 'security']
}
```

### Organization Styles

1. **by_purpose**: Group prompts by their intended use (default)
2. **by_domain**: Group by technical domain (frontend, backend, etc.)
3. **by_complexity**: Group by difficulty level
4. **hierarchical**: Multi-dimensional organization for comprehensive access

## Export Formats

### Markdown Format (Recommended)
- Human-readable with formatting
- Includes metadata and categorization
- Ready for documentation systems
- Supports template placeholders

### JSON Format
- Machine-readable structured data
- Easy integration with other tools
- Preserves all metadata and relationships
- Suitable for API consumption

### YAML Format
- Clean hierarchical structure
- Good for configuration management
- Easy to edit manually
- Compatible with DevOps workflows

### Text Format
- Simple plain text output
- Universal compatibility
- Minimal formatting overhead
- Good for quick reference

## Best Practices

### Effective Prompt Discovery
1. **Comprehensive Scanning**: Include all relevant file types (.py, .js, .md, .json, etc.)
2. **Context Awareness**: Consider project-specific vs. generic prompts
3. **Regular Updates**: Re-scan projects periodically to capture new prompts
4. **Quality Filtering**: Focus on substantial prompts (>10 characters)

### Library Organization
1. **Purpose-First**: Organize by intended use for easier discovery
2. **Cross-Reference**: Use tags for multi-dimensional categorization
3. **Version Tracking**: Note prompt evolution over time
4. **Usage Analytics**: Track which prompts are most frequently used

### Template Creation
1. **Placeholder Strategy**: Use consistent placeholders ({PROJECT_NAME}, {DATE}, etc.)
2. **Context Separation**: Clearly separate reusable parts from project-specific elements
3. **Usage Instructions**: Include guidance on template customization
4. **Validation**: Test templates in different contexts before widespread use

## Integration Workflows

### With Existing Projects
1. Scan current project for embedded prompts
2. Identify improvement opportunities
3. Create standardized prompt templates
4. Integrate templates into development workflow
5. Train team on new prompt standards

### Cross-Project Knowledge Transfer
1. Scan multiple legacy projects
2. Extract successful prompt patterns
3. Create unified prompt library
4. Establish prompt governance guidelines
5. Implement prompt usage monitoring

### Continuous Improvement
1. Regular prompt library maintenance
2. Effectiveness rating updates
3. Prompt consolidation opportunities
4. New pattern identification
5. Team feedback incorporation

## Limitations and Considerations

- **Pattern Recognition**: May miss creatively formatted prompts
- **Context Understanding**: Cannot infer intent from incomplete information
- **False Positives**: May identify non-prompt content as prompts
- **Project Specificity**: Highly project-specific prompts may have limited reuse value
- **Maintenance Overhead**: Large prompt libraries require ongoing organization

Focus on capturing explicit prompts and well-structured implicit guidance that represents valuable knowledge worth preserving and sharing across projects.