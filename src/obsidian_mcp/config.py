"""Configuration for Obsidian MCP Server.

CUSTOMIZE THIS FILE for your specific Obsidian vault and folder structure.
This is the main configuration point for adapting the boilerplate to your needs.
"""

from pathlib import Path

# =============================================================================
# VAULT CONFIGURATION - CUSTOMIZE THESE FOR YOUR VAULT
# =============================================================================

# Primary vault path - UPDATE THIS to your Obsidian vault location  
VAULT_PATH = Path("/Users/chaosisnotrandomitisrythmic/Documents/obsedian/chaos_isrhythmic")

# Target folder within vault - UPDATE THIS to your specific folder
TARGET_FOLDER = "Scanner Daybook"  # Using Scanner Daybook as test example

# Full path to your target folder
TARGET_FOLDER_PATH = VAULT_PATH / TARGET_FOLDER

# CLAUDE.md files for navigation context
VAULT_CLAUDE_MD = VAULT_PATH / "CLAUDE.md"
TARGET_CLAUDE_MD = TARGET_FOLDER_PATH / "CLAUDE.md"

# =============================================================================
# SERVER CONFIGURATION - CUSTOMIZE THESE FOR YOUR USE CASE  
# =============================================================================

# Server name - will appear in Claude Desktop MCP configuration
SERVER_NAME = "boilerplate-test-mcp"  # Test configuration

# Server instructions - describe your vault's purpose and available tools
SERVER_INSTRUCTIONS = f"""
This MCP server provides navigation and analysis tools for the {TARGET_FOLDER} folder 
in an Obsidian vault. It offers:

Core Tools:
- Vault navigation through CLAUDE.md files  
- Time and temporal context
- File discovery and content access

Custom Tools:
- [Describe your folder-specific tools here]
- [Add analysis capabilities specific to your content]
- [List workflow automation features]

Usage:
- Use navigation tools to explore vault structure
- Load context files for guidance on folder organization
- Apply custom tools for folder-specific analysis and insights

The server follows FastMCP best practices with async I/O operations and proper error handling.
""".strip()

# =============================================================================
# EXAMPLE CONFIGURATIONS
# =============================================================================

# Uncomment one of these examples or create your own:

# # Academic Research Vault
# VAULT_PATH = Path("/Users/researcher/Documents/obsidian/research-vault")
# TARGET_FOLDER = "Literature Review"
# SERVER_NAME = "research-literature-mcp"

# # Creative Writing Vault  
# VAULT_PATH = Path("/Users/writer/Documents/obsidian/creative-vault")
# TARGET_FOLDER = "Current Novel"
# SERVER_NAME = "novel-writing-mcp"

# # Project Management Vault
# VAULT_PATH = Path("/Users/manager/Documents/obsidian/projects-vault") 
# TARGET_FOLDER = "Active Projects"
# SERVER_NAME = "project-management-mcp"

# # Personal Knowledge Base
# VAULT_PATH = Path("/Users/learner/Documents/obsidian/knowledge-vault")
# TARGET_FOLDER = "Learning"
# SERVER_NAME = "knowledge-learning-mcp"