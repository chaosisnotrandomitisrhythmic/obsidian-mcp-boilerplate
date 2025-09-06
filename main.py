#!/usr/bin/env python3
"""
Obsidian MCP Server Boilerplate - Entry Point

A reusable FastMCP server template for Obsidian vault integration.
Customize the configuration in src/obsidian_mcp/config.py to adapt
for your specific vault and folder structure.
"""

from src.obsidian_mcp.server import run_server

if __name__ == "__main__":
    run_server()