"""Custom tools template for folder-specific functionality.

CUSTOMIZE THIS FILE to add tools specific to your Obsidian folder's content and workflow.
This template provides examples and patterns for common folder analysis tasks.
"""

import anyio
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Annotated

from fastmcp import FastMCP
from fastmcp.exceptions import ToolError

from ..config import TARGET_FOLDER_PATH, TARGET_FOLDER


def register_custom_tools(mcp: FastMCP) -> None:
    """Register custom tools specific to your folder's content and workflows.
    
    Args:
        mcp: The FastMCP server instance to register tools with
    """

    # =============================================================================
    # EXAMPLE TOOLS - CUSTOMIZE OR REPLACE THESE
    # =============================================================================

    @mcp.tool(
        annotations={
            "title": f"List Files in {TARGET_FOLDER}",
            "description": f"List all files in the {TARGET_FOLDER} folder",
            "readOnlyHint": True,
            "openWorldHint": False,
            "idempotentHint": True,
        }
    )
    async def list_target_folder_files(
        file_extension: Annotated[str, "File extension to filter by (e.g., 'md', 'txt'). Leave empty for all files."] = ""
    ) -> Dict[str, Any]:
        """List all files in the target folder, optionally filtered by extension.
        
        Args:
            file_extension: Optional file extension to filter by (without the dot)
        
        Returns:
            Dictionary with file listing and metadata
        """
        try:
            if not await anyio.Path(TARGET_FOLDER_PATH).exists():
                raise ToolError(f"Target folder not found: {TARGET_FOLDER_PATH}")

            files = []
            async def _list_files():
                folder_files = []
                for item in await anyio.Path(TARGET_FOLDER_PATH).iterdir():
                    if await item.is_file():
                        if not file_extension or item.suffix.lower() == f".{file_extension.lower()}":
                            stat_info = await item.stat()
                            folder_files.append({
                                "name": item.name,
                                "path": str(item),
                                "size": stat_info.st_size,
                                "modified": datetime.fromtimestamp(stat_info.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                                "extension": item.suffix,
                            })
                return sorted(folder_files, key=lambda x: x["modified"], reverse=True)

            files = await _list_files()

            return {
                "target_folder": TARGET_FOLDER,
                "folder_path": str(TARGET_FOLDER_PATH),
                "files": files,
                "total_count": len(files),
                "filter": file_extension or "all files",
            }

        except Exception as e:
            raise ToolError(f"Failed to list target folder files: {str(e)}")

    @mcp.tool(
        annotations={
            "title": f"Load File from {TARGET_FOLDER}",
            "description": f"Load the content of a specific file from {TARGET_FOLDER}",
            "readOnlyHint": True,
            "openWorldHint": False,
            "idempotentHint": True,
        }
    )
    async def load_target_folder_file(
        filename: Annotated[str, "Name of the file to load (e.g., 'document.md')"]
    ) -> Dict[str, Any]:
        """Load the content of a specific file from the target folder.
        
        Args:
            filename: The name of the file to load
            
        Returns:
            Dictionary with file content and metadata
        """
        try:
            file_path = TARGET_FOLDER_PATH / filename
            
            if not await anyio.Path(file_path).exists():
                raise ToolError(f"File not found: {filename} in {TARGET_FOLDER}")

            content = await anyio.Path(file_path).read_text(encoding="utf-8")
            stat_info = await anyio.Path(file_path).stat()

            return {
                "filename": filename,
                "path": str(file_path),
                "content": content,
                "size": stat_info.st_size,
                "modified": datetime.fromtimestamp(stat_info.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                "target_folder": TARGET_FOLDER,
                "loaded": True,
            }

        except Exception as e:
            raise ToolError(f"Failed to load file {filename}: {str(e)}")

    # =============================================================================
    # DATE-BASED TOOLS TEMPLATE
    # =============================================================================
    # Uncomment and customize if your folder contains date-based files (like daily notes)
    
    # @mcp.tool(
    #     annotations={
    #         "title": "Load Recent Files by Date",
    #         "description": f"Load recent files from {TARGET_FOLDER} based on date patterns",
    #         "readOnlyHint": True,
    #         "openWorldHint": False,
    #         "idempotentHint": True,
    #     }
    # )
    # async def load_recent_files_by_date(days_back: int = 7) -> Dict[str, Any]:
    #     """Load recent files based on date patterns in filenames.
    #     
    #     Useful for folders with date-based naming like: 2025-01-15.md, 2025-01-16.md
    #     
    #     Args:
    #         days_back: Number of days to look back from today
    #         
    #     Returns:
    #         Dictionary with recent files and their content
    #     """
    #     try:
    #         if days_back < 1 or days_back > 365:
    #             raise ToolError("days_back must be between 1 and 365")
    #         
    #         end_date = datetime.now().date()
    #         start_date = end_date - timedelta(days=days_back - 1)
    #         
    #         current_date = start_date
    #         found_files = []
    #         
    #         while current_date <= end_date:
    #             # Adjust this pattern for your date format
    #             filename = f"{current_date.strftime('%Y-%m-%d')}.md"
    #             file_path = TARGET_FOLDER_PATH / filename
    #             
    #             if await anyio.Path(file_path).exists():
    #                 content = await anyio.Path(file_path).read_text(encoding="utf-8")
    #                 found_files.append({
    #                     "date": current_date.strftime("%Y-%m-%d"),
    #                     "filename": filename,
    #                     "content": content,
    #                     "path": str(file_path),
    #                 })
    #             
    #             current_date += timedelta(days=1)
    #         
    #         return {
    #             "date_range": {
    #                 "start_date": start_date.strftime("%Y-%m-%d"),
    #                 "end_date": end_date.strftime("%Y-%m-%d"),
    #                 "days_requested": days_back,
    #             },
    #             "files": found_files,
    #             "total_found": len(found_files),
    #             "target_folder": TARGET_FOLDER,
    #         }
    #     
    #     except Exception as e:
    #         raise ToolError(f"Failed to load recent files: {str(e)}")

    # =============================================================================
    # CONTENT ANALYSIS TEMPLATE  
    # =============================================================================
    # Add domain-specific analysis tools here
    
    # Example: Search for specific patterns in files
    # @mcp.tool()
    # async def analyze_content_patterns() -> Dict[str, Any]:
    #     """Analyze content for domain-specific patterns."""
    #     # Your analysis logic here
    #     pass

    # Example: Extract metadata from files
    # @mcp.tool()
    # async def extract_file_metadata() -> Dict[str, Any]:
    #     """Extract metadata from files in the target folder."""
    #     # Your metadata extraction logic here
    #     pass