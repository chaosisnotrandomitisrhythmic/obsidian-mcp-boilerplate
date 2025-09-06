"""Navigation tools for Obsidian vault access."""

import os
from typing import Dict, Any, Annotated

import anyio
from fastmcp import FastMCP
from fastmcp.exceptions import ToolError

from ..config import VAULT_PATH, VAULT_CLAUDE_MD, TARGET_FOLDER_PATH, TARGET_CLAUDE_MD


def register_navigation_tools(mcp: FastMCP) -> None:
    """Register navigation-related tools with the MCP server.
    
    Args:
        mcp: The FastMCP server instance to register tools with
    """
    
    @mcp.tool(
        annotations={
            "title": "Load Top-Level Navigation Context",
            "description": "Load the main CLAUDE.md navigation file from Obsidian vault root",
            "readOnlyHint": True,
            "openWorldHint": False,
            "idempotentHint": True,
        }
    )
    async def load_navigation_context() -> Dict[str, Any]:
        """Load the top-level CLAUDE.md navigation file from Obsidian vault.

        Returns the content of the main navigation file that should be loaded
        into conversation context.
        """
        try:
            if not await anyio.Path(VAULT_CLAUDE_MD).exists():
                raise ToolError(f"Navigation file not found at {VAULT_CLAUDE_MD}")

            # Use anyio for async file operations (FastMCP uses anyio internally)
            content = await anyio.Path(VAULT_CLAUDE_MD).read_text(encoding="utf-8")

            return {
                "path": str(VAULT_CLAUDE_MD),
                "content": content,
                "loaded": True,
                "message": "Top-level navigation context loaded successfully",
            }

        except Exception as e:
            raise ToolError(f"Failed to load navigation context: {str(e)}")

    @mcp.tool(
        annotations={
            "title": "Load Target Folder Navigation",
            "description": "Load CLAUDE.md navigation file from the configured target folder",
            "readOnlyHint": True,
            "openWorldHint": False,
            "idempotentHint": True,
        }
    )
    async def load_target_folder_context() -> Dict[str, Any]:
        """Load the CLAUDE.md navigation file from the configured target folder.

        Returns the content of the target folder's navigation file for context.
        """
        try:
            if not await anyio.Path(TARGET_CLAUDE_MD).exists():
                return {
                    "path": str(TARGET_CLAUDE_MD),
                    "content": "",
                    "loaded": False,
                    "message": f"No CLAUDE.md found in target folder: {TARGET_FOLDER_PATH}",
                }

            # Use anyio for async file operations
            content = await anyio.Path(TARGET_CLAUDE_MD).read_text(encoding="utf-8")

            return {
                "path": str(TARGET_CLAUDE_MD),
                "content": content,
                "loaded": True,
                "message": f"Target folder navigation loaded successfully",
            }

        except Exception as e:
            raise ToolError(f"Failed to load target folder context: {str(e)}")

    @mcp.tool(
        annotations={
            "title": "Discover Subdirectory Navigation",
            "description": "Load CLAUDE.md navigation file from a specific subdirectory",
            "readOnlyHint": True,
            "openWorldHint": False,
            "idempotentHint": True,
        }
    )
    async def discover_subdirectory_navigation(
        subdirectory: Annotated[str, "Subdirectory path relative to vault root (e.g. 'Yoga', 'Literature')"]
    ) -> Dict[str, Any]:
        """Discover and load CLAUDE.md files in specific subdirectories.

        Returns:
            Content of the subdirectory's CLAUDE.md file if it exists.
        """
        try:
            subdir_path = VAULT_PATH / subdirectory
            claude_md_path = subdir_path / "CLAUDE.md"

            if not await anyio.Path(subdir_path).exists():
                raise ToolError(f"Subdirectory not found: {subdir_path}")

            if not await anyio.Path(claude_md_path).exists():
                return {
                    "path": str(claude_md_path),
                    "content": "",
                    "loaded": False,
                    "message": f"No CLAUDE.md found in {subdirectory}",
                }

            # Use anyio for async file operations
            content = await anyio.Path(claude_md_path).read_text(encoding="utf-8")

            return {
                "path": str(claude_md_path),
                "content": content,
                "loaded": True,
                "message": f"Subdirectory navigation for {subdirectory} loaded successfully",
            }

        except Exception as e:
            raise ToolError(f"Failed to discover subdirectory navigation: {str(e)}")

    @mcp.tool(
        annotations={
            "title": "List Available Navigation Files",
            "description": "Discover all CLAUDE.md files available in the vault",
            "readOnlyHint": True,
            "openWorldHint": False,
            "idempotentHint": True,
        }
    )
    async def list_navigation_files() -> Dict[str, Any]:
        """List all available CLAUDE.md files in the vault for discovery.

        Returns:
            Dictionary with lists of available navigation files.
        """
        try:
            navigation_files = []

            # Use anyio.to_thread for blocking os.walk operation
            def _walk_directory():
                files_list = []
                for root, _, files in os.walk(VAULT_PATH):
                    if "CLAUDE.md" in files:
                        rel_path = os.path.relpath(root, VAULT_PATH)
                        if rel_path == ".":
                            files_list.append("/ (root)")
                        else:
                            files_list.append(rel_path)
                return files_list
            
            navigation_files = await anyio.to_thread.run_sync(_walk_directory)

            return {
                "available_navigation": navigation_files,
                "total_count": len(navigation_files),
                "vault_path": str(VAULT_PATH),
                "target_folder": str(TARGET_FOLDER_PATH),
            }

        except Exception as e:
            raise ToolError(f"Failed to list navigation files: {str(e)}")