"""Obsidian MCP Server - Main server module."""

from fastmcp import FastMCP

from .config import SERVER_NAME, SERVER_INSTRUCTIONS
from .tools import register_time_tools, register_navigation_tools, register_custom_tools
from .prompts import register_custom_prompts


# Create the FastMCP server instance
mcp = FastMCP(name=SERVER_NAME, instructions=SERVER_INSTRUCTIONS)

# Register all tools (must happen after mcp instance creation)
register_time_tools(mcp)
register_navigation_tools(mcp)
register_custom_tools(mcp)

# Register prompts (must happen after mcp instance creation)
register_custom_prompts(mcp)


def run_server() -> None:
    """Run the MCP server."""
    mcp.run()