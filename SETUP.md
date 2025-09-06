# Setup Guide - Obsidian MCP Server Boilerplate

This guide walks through customizing the boilerplate for your specific Obsidian vault and folder.

## Quick Setup (5 minutes)

### 1. Copy the Boilerplate
```bash
# Navigate to your MCP servers directory
cd /path/to/your/mcp-servers/

# Copy the boilerplate to a new folder
cp -r obsidian-mcp-boilerplate my-vault-mcp
cd my-vault-mcp
```

### 2. Configure for Your Vault
Edit `src/obsidian_mcp/config.py` with your vault details:

```python
# UPDATE THESE PATHS for your vault
VAULT_PATH = Path("/Users/your-username/Documents/obsidian/your-vault-name")
TARGET_FOLDER = "Your Target Folder"  # e.g., "Research", "Projects", "Daily Notes"
SERVER_NAME = "your-vault-mcp"  # e.g., "research-mcp", "writing-mcp"
```

### 3. Install Dependencies
```bash
uv sync
```

### 4. Test the Server
```bash
# Test server imports
PYTHONPATH=src uv run python -c "import obsidian_mcp.server; print('✅ Server working')"

# Run with MCP inspector
npx @modelcontextprotocol/inspector uv --directory . run python main.py
```

## Customization Guide

### Add Custom Tools

Edit `src/obsidian_mcp/tools/custom.py` to add your domain-specific tools:

```python
@mcp.tool(
    annotations={
        "title": "Your Custom Tool",
        "description": "Description of what your tool does",
        "readOnlyHint": True,
        "idempotentHint": True,
    }
)
async def your_custom_tool(
    parameter: Annotated[str, "Parameter description"]
) -> Dict[str, Any]:
    """Your custom analysis tool."""
    try:
        # Your implementation here
        result = await analyze_your_content()
        
        return {
            "analysis": result,
            "status": "success",
            "target_folder": TARGET_FOLDER
        }
    except Exception as e:
        raise ToolError(f"Analysis failed: {str(e)}")
```

### Add Custom Prompts

Edit `src/obsidian_mcp/prompts/custom.py` to orchestrate your tools:

```python
@mcp.prompt(
    name="your_workflow",
    description="Your custom workflow description",
    tags={"your", "domain", "tags"}
)
def your_workflow() -> List[PromptMessage]:
    return [
        Message(
            role="user",
            content=(
                "Execute your custom workflow:\\n\\n"
                "1. get_current_time() for context\\n"
                "2. your_custom_tool() for analysis\\n"
                "3. Provide insights based on your domain\\n"
            )
        )
    ]
```

## Example Configurations

### Academic Research Setup

```python
# config.py
VAULT_PATH = Path("/Users/researcher/Documents/obsidian/research-vault")
TARGET_FOLDER = "Literature Review"
SERVER_NAME = "research-literature-mcp"
SERVER_INSTRUCTIONS = """
Academic research MCP server for literature review and paper analysis.

Tools:
- Paper metadata extraction from PDFs
- Citation network analysis
- Research gap identification
- Literature synthesis workflows

Use this server to analyze research papers and identify connections in your literature.
"""
```

**Custom tools to add:**
- Extract citations and authors from papers
- Identify research methodologies  
- Track research themes and trends
- Generate literature review summaries

### Creative Writing Setup

```python
# config.py
VAULT_PATH = Path("/Users/writer/Documents/obsidian/creative-vault")
TARGET_FOLDER = "Current Novel"
SERVER_NAME = "novel-writing-mcp"
SERVER_INSTRUCTIONS = """
Creative writing MCP server for novel development and character tracking.

Tools:
- Character arc analysis across chapters
- Scene and chapter progression tracking
- Dialogue and voice consistency checking
- Plot development and pacing analysis

Use this server to maintain consistency and track development in your creative work.
"""
```

**Custom tools to add:**
- Extract character mentions and development
- Analyze dialogue patterns and voice consistency
- Track plot threads and story arcs
- Generate character and plot summaries

### Project Management Setup

```python
# config.py  
VAULT_PATH = Path("/Users/manager/Documents/obsidian/projects-vault")
TARGET_FOLDER = "Active Projects"
SERVER_NAME = "project-management-mcp"
SERVER_INSTRUCTIONS = """
Project management MCP server for task tracking and progress analysis.

Tools:
- Task completion status tracking
- Milestone and deadline analysis
- Resource allocation and workload assessment
- Project timeline and dependency mapping

Use this server to monitor project progress and identify bottlenecks.
"""
```

**Custom tools to add:**
- Parse task status and completion markers
- Extract deadline and milestone information
- Analyze team workload and resource allocation
- Generate project status reports

## Advanced Customization

### Date-Based File Processing

If your folder contains date-based files (like daily notes), uncomment and customize the date-based tools in `custom.py`:

```python
@mcp.tool()
async def load_recent_files_by_date(days_back: int = 7) -> Dict[str, Any]:
    """Load files matching date patterns: YYYY-MM-DD.md"""
    # Adjust the filename pattern for your date format
    filename = f"{current_date.strftime('%Y-%m-%d')}.md"
```

### Content Analysis Patterns

Add domain-specific pattern matching:

```python
@mcp.tool()
async def analyze_content_patterns() -> Dict[str, Any]:
    """Extract domain-specific patterns from files."""
    files = await list_all_files()
    patterns = {}
    
    for file_data in files:
        content = file_data["content"]
        
        # Example: Extract academic citations
        citations = re.findall(r'@\w+\{[^}]+\}', content)
        
        # Example: Extract task markers
        tasks = re.findall(r'- \[([ x])\] (.+)', content)
        
        # Example: Extract energy ratings
        energy = re.findall(r'Energy: (\d+)/5', content)
        
        patterns[file_data["filename"]] = {
            "citations": citations,
            "tasks": tasks, 
            "energy": energy
        }
    
    return {"patterns": patterns}
```

## Integration with Claude Desktop

Add your server to Claude Desktop's MCP configuration:

```json
{
  "mcpServers": {
    "your-vault-mcp": {
      "command": "uv",
      "args": [
        "--directory", 
        "/path/to/your/my-vault-mcp",
        "run",
        "python",
        "main.py"
      ]
    }
  }
}
```

## Development Workflow

### 1. Test Changes Locally
```bash
# Test server functionality
PYTHONPATH=src uv run python -c "
from obsidian_mcp.server import mcp
print(f'Tools: {len(mcp._tool_manager._tools)}')
print(f'Prompts: {len(mcp._prompt_manager._prompts)}')
"

# Run with inspector
npx @modelcontextprotocol/inspector uv --directory . run python main.py
```

### 2. Add New Dependencies
```bash
# Add new Python packages
uv add package-name

# Update for development
uv add --dev pytest black isort mypy
```

### 3. Code Formatting
```bash
uv run black src/
uv run isort src/
uv run mypy src/
```

## Troubleshooting

### Common Issues

**"ValidationError: X is not of type 'string'"**
- Solution: Use `Dict[str, Any]` return type, not `Dict[str, str]`

**"Tool not found in MCP Inspector"** 
- Solution: Ensure tool registration happens after `mcp = FastMCP(...)` creation
- Check that `register_custom_tools(mcp)` is called in `server.py`

**Server hangs or slow responses**
- Solution: Use `async`/`await` and `anyio` for all file operations
- Never use blocking I/O like `Path.read_text()` directly

**"File not found" errors**
- Solution: Check `VAULT_PATH` and `TARGET_FOLDER` in `config.py`
- Verify paths exist and are accessible

### Debug Your Configuration

```bash
# Verify configuration
PYTHONPATH=src uv run python -c "
from obsidian_mcp.config import VAULT_PATH, TARGET_FOLDER_PATH
print(f'Vault: {VAULT_PATH}')
print(f'Target: {TARGET_FOLDER_PATH}') 
print(f'Vault exists: {VAULT_PATH.exists()}')
print(f'Target exists: {TARGET_FOLDER_PATH.exists()}')
"
```

## Next Steps

1. **Start with the example tools** - Test `list_target_folder_files()` and `load_target_folder_file()`
2. **Add one custom tool** - Begin with simple file analysis specific to your domain
3. **Create a workflow prompt** - Combine multiple tools into a useful workflow
4. **Integrate with Claude Desktop** - Add to your MCP configuration and test
5. **Iterate and expand** - Add more sophisticated analysis as you understand your needs

The boilerplate provides a solid foundation - customize it incrementally to match your specific workflow and content analysis needs.