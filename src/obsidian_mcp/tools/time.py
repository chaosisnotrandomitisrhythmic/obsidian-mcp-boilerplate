"""Time-related tools for Obsidian MCP Server."""

import time
from datetime import datetime
from typing import Dict

from fastmcp import FastMCP
from fastmcp.exceptions import ToolError


def register_time_tools(mcp: FastMCP) -> None:
    """Register time-related tools with the MCP server.
    
    Args:
        mcp: The FastMCP server instance to register tools with
    """
    
    @mcp.tool(
        annotations={
            "title": "Get Current Time with Timezone",
            "readOnlyHint": True,
            "openWorldHint": False,
            "idempotentHint": False,
        }
    )
    def get_current_time() -> Dict[str, str]:
        """Get the current date and time with timezone information."""
        try:
            now = datetime.now()
            timezone_name = time.tzname[time.daylight]

            return {"time": now.strftime("%Y-%m-%d %H:%M:%S"), "timezone": timezone_name}
        except Exception as e:
            raise ToolError(f"Failed to get current time: {str(e)}")