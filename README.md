# Obsidian MCP Server Boilerplate

A reusable FastMCP server template for creating Model Context Protocol servers that work with any Obsidian vault folder. This boilerplate provides core navigation and time tools while allowing easy customization for folder-specific workflows.

## Features

### Core Tools (Reusable)
- **Navigation Tools**: CLAUDE.md context loading, subdirectory discovery, navigation file listing
- **Time Tools**: Current timestamp with timezone information
- **Vault Integration**: Secure path validation and filesystem access

### Customizable Components
- **Folder-Specific Tools**: Template for adding custom analysis tools
- **Custom Prompts**: FastMCP prompt system for workflow orchestration
- **Configuration**: Easy setup for different vault structures

## Quick Start

1. **Clone and Configure**:
   ```bash
   cp -r obsidian-mcp-boilerplate my-vault-mcp
   cd my-vault-mcp
   ```

2. **Update Configuration**:
   - Edit `src/obsidian_mcp/config.py` with your vault path and server name
   - Modify custom tools in `src/obsidian_mcp/tools/custom.py`
   - Add prompts in `src/obsidian_mcp/prompts/custom.py`

3. **Install and Run**:
   ```bash
   uv sync
   uv run python main.py
   ```

4. **Test with MCP Inspector**:
   ```bash
   npx @modelcontextprotocol/inspector uv --directory . run python main.py
   ```

## Architecture

```
/
├── main.py                          # Clean entry point
├── pyproject.toml                   # uv dependency management
├── src/obsidian_mcp/
│   ├── __init__.py
│   ├── config.py                    # Vault path and server configuration
│   ├── server.py                    # FastMCP instance and tool registration
│   ├── tools/                       # Modular tool definitions
│   │   ├── __init__.py              # Tool registration exports
│   │   ├── time.py                  # Time-related tools (reusable)
│   │   ├── navigation.py            # Vault navigation tools (reusable)
│   │   └── custom.py                # Your folder-specific tools
│   └── prompts/                     # FastMCP prompts for workflows
│       ├── __init__.py
│       └── custom.py                # Your folder-specific prompts
└── llm_ctx/                        # LLM context documentation
    └── fastmcp_reference.md
```

## Customization Guide

### 1. Configure Your Vault

Edit `src/obsidian_mcp/config.py`:
```python
# Your vault configuration
VAULT_PATH = "/path/to/your/obsidian/vault"
TARGET_FOLDER = "Your Target Folder"  # Subfolder to focus on
SERVER_NAME = "your-vault-mcp"
SERVER_INSTRUCTIONS = "Description of your vault's purpose and tools"
```

### 2. Add Custom Tools

Edit `src/obsidian_mcp/tools/custom.py`:
```python
def register_custom_tools(mcp):
    """Register your folder-specific tools."""
    
    @mcp.tool
    async def your_custom_tool() -> Dict[str, Any]:
        """Your custom analysis tool."""
        # Implementation here
        pass
```

### 3. Add Custom Prompts

Edit `src/obsidian_mcp/prompts/custom.py`:
```python
def register_custom_prompts(mcp: FastMCP) -> None:
    """Register your folder-specific prompts."""
    
    @mcp.prompt(
        name="your_workflow",
        description="Your custom workflow description",
        tags={"your", "tags"}
    )
    def your_workflow() -> List[PromptMessage]:
        return [Message(role="user", content="Your workflow instructions")]
```

## Example Configurations

### Academic Research Vault
- Tools: Citation extraction, paper analysis, research timeline
- Prompts: Literature review, research planning, citation formatting

### Creative Writing Vault
- Tools: Character analysis, plot tracking, scene extraction
- Prompts: Story structure analysis, character development, writing prompts

### Project Management Vault
- Tools: Task extraction, deadline tracking, progress analysis
- Prompts: Project status reports, milestone planning, resource allocation

### Personal Knowledge Base
- Tools: Concept mapping, cross-reference analysis, learning progress
- Prompts: Knowledge synthesis, study planning, concept review

## FastMCP Best Practices

This boilerplate follows FastMCP best practices:

1. **Async I/O Operations**: All file operations use `anyio` for non-blocking access
2. **Proper Error Handling**: `ToolError` from `fastmcp.exceptions` for user-facing errors
3. **Type Safety**: Correct return type annotations (`Dict[str, Any]` vs `Dict[str, str]`)
4. **Tool Annotations**: Comprehensive metadata with `readOnlyHint` and `idempotentHint`
5. **Modular Organization**: Factory pattern for tool registration
6. **Clean Architecture**: `src/` layout with clear entry point

## Development Commands

```bash
# Run the server
uv run python main.py

# Test with MCP inspector
npx @modelcontextprotocol/inspector uv --directory . run python main.py

# Test server imports
PYTHONPATH=src uv run python -c "import obsidian_mcp.server; print('✅ Server working')"

# Add new dependencies
uv add package-name

# Code formatting
uv run black src/
uv run isort src/
```

## Based on Revenant MCP

This boilerplate extracts the proven patterns from the Revenant MCP server, which provides:
- Scanner Daybook daily log analysis
- Morning briefing workflows
- Energy pattern recognition
- FastMCP prompt orchestration

The Scanner Daybook implementation serves as a reference example for building domain-specific tools on top of this foundation.

## License

MIT License - Feel free to adapt for your specific Obsidian vault needs.