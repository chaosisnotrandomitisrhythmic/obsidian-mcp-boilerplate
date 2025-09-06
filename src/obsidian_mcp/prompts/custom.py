"""Custom prompts template for folder-specific workflows.

CUSTOMIZE THIS FILE to add FastMCP prompts that orchestrate your folder-specific tools.
Prompts combine multiple tool calls into coherent workflows for common use cases.
"""

from typing import List
from fastmcp import FastMCP
from fastmcp.prompts.prompt import Message, PromptMessage

from ..config import TARGET_FOLDER


def register_custom_prompts(mcp: FastMCP) -> None:
    """Register custom prompts specific to your folder's workflows.
    
    Args:
        mcp: The FastMCP server instance to register prompts with
    """

    # =============================================================================
    # EXAMPLE PROMPTS - CUSTOMIZE OR REPLACE THESE
    # =============================================================================

    @mcp.prompt(
        name="folder_overview",
        description=f"Generate a comprehensive overview of the {TARGET_FOLDER} folder",
        tags={"overview", "analysis", "folder"}
    )
    def folder_overview() -> List[PromptMessage]:
        """
        Creates a workflow to analyze and summarize the target folder's contents.
        This is a template - customize the analysis steps for your specific needs.
        """
        return [
            Message(
                role="user",
                content=(
                    f"Create a comprehensive overview of my {TARGET_FOLDER} folder.\\n\\n"
                    "Please execute this workflow:\\n"
                    "1. get_current_time() to establish current context\\n"
                    "2. load_navigation_context() for vault-level guidance\\n"
                    "3. load_target_folder_context() for folder-specific context\\n"
                    "4. list_target_folder_files() to see all available files\\n\\n"
                    "Then analyze the folder contents and provide:\\n"
                    "- Summary of file types and organization\\n"
                    "- Key themes or patterns in the content\\n"
                    "- Recent activity and changes\\n"
                    "- Suggestions for next actions or areas to explore\\n\\n"
                    f"Focus on insights specific to the {TARGET_FOLDER} domain and purpose."
                )
            )
        ]

    @mcp.prompt(
        name="recent_activity_analysis", 
        description=f"Analyze recent activity and changes in {TARGET_FOLDER}",
        tags={"recent", "activity", "analysis"}
    )
    def recent_activity_analysis() -> List[PromptMessage]:
        """
        Analyzes recent activity in the target folder.
        Customize the analysis criteria for your specific content type.
        """
        return [
            Message(
                role="user",
                content=(
                    f"Analyze recent activity in my {TARGET_FOLDER} folder.\\n\\n"
                    "Please execute this workflow:\\n"
                    "1. get_current_time() for temporal context\\n"
                    "2. list_target_folder_files() to get all files with timestamps\\n"
                    "3. For the most recently modified files, use load_target_folder_file() to examine content\\n\\n"
                    "Then provide analysis of:\\n"
                    "- Most recently active files and their content\\n"
                    "- Patterns in recent changes or additions\\n"
                    "- Trends or developments over time\\n"
                    "- Recommendations based on recent activity\\n\\n"
                    f"Tailor the analysis to {TARGET_FOLDER}'s specific domain and my workflows."
                )
            )
        ]

    # =============================================================================
    # WORKFLOW TEMPLATES FOR DIFFERENT USE CASES
    # =============================================================================
    
    # Academic Research Example
    # @mcp.prompt(
    #     name="literature_review",
    #     description="Conduct literature review analysis of research papers",
    #     tags={"academic", "research", "literature"}
    # )
    # def literature_review() -> List[PromptMessage]:
    #     return [
    #         Message(
    #             role="user", 
    #             content=(
    #                 "Conduct a literature review of papers in my research folder.\\n\\n"
    #                 "1. list_target_folder_files('pdf') for all PDF papers\\n"
    #                 "2. For each paper, extract key findings and methodologies\\n"
    #                 "3. Identify research gaps and connections between papers\\n"
    #                 "4. Suggest future research directions\\n"
    #             )
    #         )
    #     ]

    # Creative Writing Example  
    # @mcp.prompt(
    #     name="story_development",
    #     description="Analyze story development and character arcs",
    #     tags={"writing", "story", "character", "development"}
    # )
    # def story_development() -> List[PromptMessage]:
    #     return [
    #         Message(
    #             role="user",
    #             content=(
    #                 "Analyze my story development and character arcs.\\n\\n"
    #                 "1. list_target_folder_files('md') for all story files\\n"
    #                 "2. Extract character mentions and development\\n"
    #                 "3. Track plot progression and story arcs\\n"
    #                 "4. Identify inconsistencies or development opportunities\\n"
    #             )
    #         )
    #     ]

    # Project Management Example
    # @mcp.prompt(
    #     name="project_status_report", 
    #     description="Generate comprehensive project status report",
    #     tags={"project", "status", "management", "reporting"}
    # )
    # def project_status_report() -> List[PromptMessage]:
    #     return [
    #         Message(
    #             role="user",
    #             content=(
    #                 "Generate a comprehensive project status report.\\n\\n"
    #                 "1. list_target_folder_files() for all project files\\n"
    #                 "2. Analyze task completion and milestone progress\\n"
    #                 "3. Identify blockers and resource needs\\n"
    #                 "4. Provide timeline and next action recommendations\\n"
    #             )
    #         )
    #     ]

    # Learning/Knowledge Base Example
    # @mcp.prompt(
    #     name="knowledge_synthesis",
    #     description="Synthesize knowledge and identify learning connections",
    #     tags={"learning", "knowledge", "synthesis", "connections"}
    # )
    # def knowledge_synthesis() -> List[PromptMessage]:
    #     return [
    #         Message(
    #             role="user",
    #             content=(
    #                 "Synthesize knowledge and identify learning connections.\\n\\n"
    #                 "1. list_target_folder_files() for all learning materials\\n"
    #                 "2. Extract key concepts and learning points\\n"
    #                 "3. Identify connections between different topics\\n"
    #                 "4. Suggest areas for deeper exploration\\n"
    #             )
    #         )
    #     ]