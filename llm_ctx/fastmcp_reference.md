# FastMCP Framework Reference

This document provides essential FastMCP patterns and best practices for extending the Obsidian MCP Server boilerplate.

## Key FastMCP Concepts

### Tool Registration Pattern
```python
from fastmcp import FastMCP
from fastmcp.exceptions import ToolError

# Create server instance first
mcp = FastMCP(name="server-name", instructions="Server description")

# Register tools AFTER instance creation
@mcp.tool(
    annotations={
        "title": "Tool Display Name",
        "description": "Tool description for clients", 
        "readOnlyHint": True,  # Tool doesn't modify state
        "idempotentHint": True,  # Same input = same output
        "openWorldHint": False,  # Tool has limited scope
    }
)
async def my_tool(param: str) -> Dict[str, Any]:
    """Tool implementation with proper async/await."""
    try:
        # Use anyio for file operations
        content = await anyio.Path(file_path).read_text()
        return {"result": content}
    except Exception as e:
        raise ToolError(f"User-friendly error: {str(e)}")
```

### Prompt Registration Pattern  
```python
from fastmcp.prompts.prompt import Message, PromptMessage
from typing import List

@mcp.prompt(
    name="prompt_name",
    description="Prompt description", 
    tags={"tag1", "tag2"}
)
def my_prompt(param: int = 7) -> List[PromptMessage]:
    """Prompt that orchestrates multiple tools."""
    return [
        Message(
            role="user",  # Only 'user' and 'assistant' roles allowed
            content=(
                "Execute this workflow:\\n"
                "1. tool_one() for data\\n"
                "2. tool_two() for analysis\\n"
                "3. Provide insights based on results"
            )
        )
    ]
```

## Critical Best Practices

### Return Types & Validation
```python
# CORRECT: Use Dict[str, Any] for mixed data types
def mixed_tool() -> Dict[str, Any]:
    return {
        "text": "string",
        "count": 42,  # int
        "success": True,  # bool
        "items": ["list", "data"]  # list
    }

# INCORRECT: Dict[str, str] with non-string values will fail validation
def broken_tool() -> Dict[str, str]:
    return {"count": 42}  # ❌ ValidationError: 42 is not of type 'string'
```

### Async I/O Operations
```python
import anyio

# CORRECT: Use anyio for all I/O operations
async def read_file_async(path: Path) -> str:
    return await anyio.Path(path).read_text(encoding="utf-8")

# CORRECT: Wrap blocking operations with anyio.to_thread
async def walk_directory_async(path: Path) -> List[str]:
    def _blocking_walk():
        return [str(p) for p in path.rglob("*.md")]
    
    return await anyio.to_thread.run_sync(_blocking_walk)

# INCORRECT: Synchronous I/O blocks the event loop
def read_file_sync(path: Path) -> str:
    return path.read_text()  # ❌ Blocks FastMCP async event loop
```

### Error Handling
```python
from fastmcp.exceptions import ToolError

# CORRECT: Use ToolError for user-facing errors
async def my_tool() -> Dict[str, Any]:
    try:
        # Tool logic here
        pass
    except FileNotFoundError:
        raise ToolError("File not found - please check the path")
    except Exception as e:
        raise ToolError(f"Failed to process: {str(e)}")

# INCORRECT: Raw exceptions don't provide good UX
async def bad_tool() -> Dict[str, Any]:
    return open("missing_file.txt").read()  # ❌ Raw FileNotFoundError
```

## Tool Organization Patterns

### Factory Pattern (Recommended)
```python
def register_my_tools(mcp: FastMCP) -> None:
    """Register tools with the MCP server."""
    
    @mcp.tool()
    async def tool_one() -> Dict[str, Any]:
        """Tool implementation."""
        pass
    
    @mcp.tool() 
    async def tool_two() -> Dict[str, Any]:
        """Tool implementation."""
        pass

# In server.py:
register_my_tools(mcp)
```

### Parameter Annotations
```python
from typing import Annotated

@mcp.tool()
async def my_tool(
    days_back: Annotated[int, "Number of days to look back (1-365)"] = 7,
    file_type: Annotated[str, "File extension without dot (e.g., 'md', 'txt')"] = "md"
) -> Dict[str, Any]:
    """Tool with well-documented parameters."""
    pass
```

## Common Patterns

### File Loading with Safety
```python
async def load_file_safely(file_path: Path) -> Dict[str, Any]:
    """Load file with proper error handling."""
    try:
        if not await anyio.Path(file_path).exists():
            return {
                "path": str(file_path),
                "loaded": False,
                "error": "File not found",
                "content": ""
            }
        
        content = await anyio.Path(file_path).read_text(encoding="utf-8")
        stat_info = await anyio.Path(file_path).stat()
        
        return {
            "path": str(file_path),
            "loaded": True,
            "content": content,
            "size": stat_info.st_size,
            "modified": datetime.fromtimestamp(stat_info.st_mtime).isoformat()
        }
    
    except Exception as e:
        raise ToolError(f"Failed to load {file_path.name}: {str(e)}")
```

### Directory Walking
```python
async def walk_directory_async(root_path: Path) -> List[Dict[str, Any]]:
    """Walk directory tree asynchronously."""
    def _walk():
        files = []
        for item in root_path.rglob("*.md"):
            if item.is_file():
                files.append({
                    "name": item.name,
                    "path": str(item),
                    "relative_path": str(item.relative_to(root_path))
                })
        return files
    
    return await anyio.to_thread.run_sync(_walk)
```

### Date Range Processing
```python
from datetime import datetime, timedelta

async def load_date_range_files(folder: Path, days_back: int) -> Dict[str, Any]:
    """Load files based on date patterns."""
    if days_back < 1 or days_back > 365:
        raise ToolError("days_back must be between 1 and 365")
    
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days_back - 1)
    
    current_date = start_date
    found_files = []
    
    while current_date <= end_date:
        filename = f"{current_date.strftime('%Y-%m-%d')}.md"
        file_path = folder / filename
        
        if await anyio.Path(file_path).exists():
            content = await anyio.Path(file_path).read_text()
            found_files.append({
                "date": current_date.isoformat(),
                "filename": filename,
                "content": content
            })
        
        current_date += timedelta(days=1)
    
    return {
        "date_range": {
            "start": start_date.isoformat(),
            "end": end_date.isoformat(), 
            "days_requested": days_back
        },
        "files": found_files,
        "total_found": len(found_files)
    }
```

## Testing Your Implementation

### Import Test
```bash
PYTHONPATH=src uv run python -c "import obsidian_mcp.server; print('✅ Server imports successfully')"
```

### MCP Inspector Test  
```bash
npx @modelcontextprotocol/inspector uv --directory . run python main.py
```

### Tool Validation Test
```bash
# Test individual tool registration
PYTHONPATH=src uv run python -c "
from obsidian_mcp.server import mcp
print(f'✅ {len(mcp._tool_manager._tools)} tools registered')
for name in mcp._tool_manager._tools:
    print(f'  - {name}')
"
```

## Common Pitfalls & Solutions

| Problem | Symptom | Solution |
|---------|---------|----------|
| "ValidationError: X is not of type 'string'" | Tool returns mixed types | Use `Dict[str, Any]` not `Dict[str, str]` |
| "Tool not found" in MCP Inspector | Tool defined but not registered | Ensure `@mcp.tool` decorators run after `mcp` instance creation |
| Server hangs/slow response | Blocking I/O operations | Use `anyio` for all file operations |
| "PromptMessage role validation error" | Invalid role in prompts | Use only `role="user"` or `role="assistant"` |
| Tool registration timing issues | Tools in separate modules not found | Use factory pattern with explicit registration calls |

## Performance Considerations

1. **Batch I/O Operations**: Load multiple files concurrently when possible
2. **Use anyio Consistently**: All I/O should be async to avoid blocking
3. **Implement Caching**: For frequently accessed files or expensive computations
4. **Limit Data Size**: Return summaries for large datasets, full content for small files
5. **Validate Input Early**: Check parameters before doing expensive operations

This reference provides the foundation for extending your Obsidian MCP server with domain-specific functionality while following FastMCP best practices.