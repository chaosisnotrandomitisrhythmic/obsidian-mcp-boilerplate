# CLAUDE.md - Obsidian MCP Server Boilerplate

This file provides guidance to Claude Code (claude.ai/code) when working with this boilerplate repository.

## Overview

This is a **reusable FastMCP server boilerplate** for creating Model Context Protocol servers that integrate with any Obsidian vault folder. It extracts proven patterns from the Revenant MCP server (Scanner Daybook implementation) and makes them adaptable for any domain.

**Core Purpose**: Provide a 5-minute setup foundation for domain-specific Obsidian MCP servers while following FastMCP best practices.

## Architecture & Structure

```
obsidian-mcp-boilerplate/
├── main.py                          # Entry point - DO NOT modify
├── pyproject.toml                   # uv package management
├── src/obsidian_mcp/
│   ├── config.py                    # PRIMARY CUSTOMIZATION POINT
│   ├── server.py                    # FastMCP instance - rarely modified
│   ├── tools/
│   │   ├── time.py                  # Reusable - DO NOT modify
│   │   ├── navigation.py            # Reusable - DO NOT modify  
│   │   └── custom.py                # CUSTOMIZE THIS for domain tools
│   └── prompts/
│       └── custom.py                # CUSTOMIZE THIS for workflows
└── llm_ctx/
    └── fastmcp_reference.md         # Framework patterns reference
```

## Customization Workflow

When adapting this boilerplate for a new Obsidian folder:

### 1. Configuration (REQUIRED)
```python
# src/obsidian_mcp/config.py
VAULT_PATH = Path("/path/to/obsidian/vault")  # UPDATE THIS
TARGET_FOLDER = "Folder Name"                  # UPDATE THIS
SERVER_NAME = "descriptive-name-mcp"           # UPDATE THIS
SERVER_INSTRUCTIONS = "Description..."          # UPDATE THIS
```

### 2. Custom Tools (src/obsidian_mcp/tools/custom.py)
```python
@mcp.tool()
async def analyze_domain_content() -> Dict[str, Any]:
    """Add domain-specific analysis tools."""
    # Use TARGET_FOLDER_PATH for file access
    # Always use anyio for async I/O
    # Return Dict[str, Any] for mixed types
    # Raise ToolError for user-facing errors
```

### 3. Custom Prompts (src/obsidian_mcp/prompts/custom.py)
```python
@mcp.prompt(name="domain_workflow", tags={"domain", "analysis"})
def domain_workflow() -> List[PromptMessage]:
    return [Message(role="user", content="Workflow steps...")]
```

## Critical FastMCP Patterns

### ✅ ALWAYS DO THESE

1. **Async I/O Operations**:
```python
# CORRECT
content = await anyio.Path(file_path).read_text()

# WRONG - Blocks event loop
content = Path(file_path).read_text()
```

2. **Return Type Annotations**:
```python
# CORRECT for mixed types
def my_tool() -> Dict[str, Any]:
    return {"text": "string", "count": 42, "success": True}

# WRONG - Will cause validation errors
def my_tool() -> Dict[str, str]:
    return {"count": 42}  # 42 is not a string!
```

3. **Error Handling**:
```python
from fastmcp.exceptions import ToolError

# CORRECT
raise ToolError("User-friendly error message")

# WRONG
raise Exception("Raw exception")
```

4. **Tool Registration Timing**:
```python
# Tools MUST be registered AFTER mcp instance creation
mcp = FastMCP(...)  # First create instance
register_custom_tools(mcp)  # Then register tools
```

## Common Customization Patterns

### Academic Research Vault
```python
# Tools to add:
- extract_citations_from_papers()
- analyze_research_methodology()
- identify_research_gaps()
- generate_literature_matrix()

# Prompts to add:
- literature_review_synthesis
- research_timeline_analysis
- citation_network_mapping
```

### Creative Writing Vault
```python
# Tools to add:
- track_character_development()
- analyze_plot_structure()
- check_scene_consistency()
- extract_dialogue_patterns()

# Prompts to add:
- story_arc_analysis
- character_relationship_mapping
- writing_style_consistency
```

### Project Management Vault
```python
# Tools to add:
- extract_task_status()
- calculate_project_progress()
- identify_blockers()
- analyze_resource_allocation()

# Prompts to add:
- project_status_report
- milestone_tracking
- risk_assessment
```

### Personal Knowledge Base
```python
# Tools to add:
- map_concept_relationships()
- track_learning_progress()
- identify_knowledge_gaps()
- generate_study_guides()

# Prompts to add:
- knowledge_synthesis
- learning_path_optimization
- concept_review
```

## Testing & Validation

### Quick Tests
```bash
# Test imports
PYTHONPATH=src uv run python -c "import obsidian_mcp.server; print('✅ Server imports successfully')"

# Test tool registration
PYTHONPATH=src uv run python -c "
from obsidian_mcp.server import mcp
print(f'✅ {len(mcp._tool_manager._tools)} tools registered')
for name in mcp._tool_manager._tools:
    print(f'  - {name}')
"

# Test configuration
PYTHONPATH=src uv run python -c "
from obsidian_mcp.config import VAULT_PATH, TARGET_FOLDER_PATH
print(f'Vault: {VAULT_PATH}')
print(f'Target: {TARGET_FOLDER_PATH}')
print(f'Vault exists: {VAULT_PATH.exists()}')
print(f'Target exists: {TARGET_FOLDER_PATH.exists()}')
"

# Full MCP Inspector test
npx @modelcontextprotocol/inspector uv --directory . run python main.py
```

## Common Issues & Solutions

### "ValidationError: X is not of type 'string'"
**Cause**: Tool returns non-string values with `Dict[str, str]` annotation
**Fix**: Change return type to `Dict[str, Any]`

### "Tool not found" in MCP Inspector
**Cause**: Tool registration timing issue
**Fix**: Ensure `@mcp.tool` decorators execute AFTER `mcp = FastMCP()` creation

### Server hangs or slow responses
**Cause**: Synchronous I/O operations blocking event loop
**Fix**: Use `anyio` for ALL file operations

### "PromptMessage role validation error"
**Cause**: Using `role="system"` in prompts
**Fix**: Only use `role="user"` or `role="assistant"`

## Development Commands

```bash
# Install/update dependencies
uv sync
uv add package-name

# Run server
uv run python main.py

# Code formatting
uv run black src/
uv run isort src/

# Type checking
uv run mypy src/
```

## Adding New Features

### Step 1: Understand Your Domain
- What files will you be analyzing?
- What patterns or information need extraction?
- What workflows do users typically follow?

### Step 2: Create Domain Tools
```python
# In custom.py
@mcp.tool()
async def your_analysis_tool(
    param: Annotated[str, "Parameter description"]
) -> Dict[str, Any]:
    """Tool description."""
    try:
        # 1. Load files using anyio
        # 2. Process/analyze content
        # 3. Return structured results
        pass
    except Exception as e:
        raise ToolError(f"Analysis failed: {str(e)}")
```

### Step 3: Create Workflow Prompts
```python
# In prompts/custom.py
@mcp.prompt(name="workflow_name")
def workflow_name() -> List[PromptMessage]:
    return [Message(
        role="user",
        content="1. Use tool_one()\\n2. Use tool_two()\\n3. Analyze results"
    )]
```

### Step 4: Test Thoroughly
- Test each tool individually
- Test prompts with real data
- Validate with MCP Inspector
- Check performance with large datasets

## Origin Story

This boilerplate was extracted from the **Revenant MCP server**, which provides:
- Scanner Daybook daily log analysis
- Energy pattern recognition
- Morning briefing workflows
- Zeigarnik Effect management through documentation

The Scanner implementation demonstrated FastMCP best practices that are now generalized in this boilerplate for any Obsidian vault use case.

## Key Design Decisions

1. **Separation of Reusable vs Custom**: Navigation and time tools are reusable, domain-specific tools go in custom.py
2. **Configuration Centralization**: All customization starts in config.py
3. **Factory Pattern**: Tool registration uses factory functions to avoid timing issues
4. **Async-First**: All I/O operations are async using anyio
5. **Error Handling Philosophy**: User-friendly errors via ToolError, never raw exceptions
6. **Return Type Safety**: Dict[str, Any] for flexibility, avoid strict typing that causes validation errors

## Future Enhancement Ideas

When extending this boilerplate:

1. **Add Caching**: For frequently accessed files or expensive computations
2. **Batch Processing**: Process multiple files concurrently
3. **Progressive Loading**: Return summaries first, details on demand
4. **Search Optimization**: Add indexing for large vaults
5. **Template Library**: Pre-built tool templates for common domains
6. **Testing Framework**: Automated test templates for custom tools

## Important Reminders

- **NEVER** modify `time.py` or `navigation.py` - these are proven reusable components
- **ALWAYS** use `anyio` for file operations - synchronous I/O will block FastMCP
- **ALWAYS** test with real vault data before deploying
- **PREFER** simple, focused tools over complex multi-purpose ones
- **REMEMBER** prompts orchestrate tools, tools don't orchestrate other tools

## Success Criteria

A successful customization will:
1. ✅ Import without errors
2. ✅ Register all tools correctly
3. ✅ Handle missing files gracefully
4. ✅ Return structured, useful data
5. ✅ Complete operations quickly (async I/O)
6. ✅ Provide clear error messages
7. ✅ Follow domain conventions

## Getting Help

- **FastMCP Documentation**: See `llm_ctx/fastmcp_reference.md`
- **Example Implementation**: Revenant MCP (Scanner Daybook)
- **Common Patterns**: Check this file's customization examples
- **Testing Issues**: Use MCP Inspector for debugging

---

**Remember**: This boilerplate provides the foundation. Your domain expertise shapes the implementation. Start simple, test often, iterate based on actual usage.