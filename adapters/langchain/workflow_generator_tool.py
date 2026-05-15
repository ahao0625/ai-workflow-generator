"""
LangChain Tool Adapter / LangChain工具适配器
Wraps AI Workflow Generator as a BaseTool for LangChain agents.
包装为LangChain BaseTool，供LangChain Agent调用。
"""

import json
from typing import Optional, Type

from langchain_core.tools import BaseTool
from langchain_core.callbacks import CallbackManagerForToolRun
from pydantic import BaseModel, Field


class WorkflowGeneratorInput(BaseModel):
    description: str = Field(
        description="Natural language description of desired workflow. Include target platform, model, and features."
    )
    target_platform: Optional[str] = Field(
        default=None,
        description="Target platform: comfyui, a1111, diffusers, replicate, stability, midjourney, dalle, ideogram"
    )
    model_family: Optional[str] = Field(
        default=None,
        description="Model family: sd15, sdxl, sdxl_turbo, flux, sd3, video"
    )


class WorkflowGeneratorTool(BaseTool):
    name: str = "ai_workflow_generator"
    description: str = """
Generate AI image/video generation workflow files for various platforms.

Input: Natural language description (target platform, model, feature requirements)
Output: Platform-native workflow file (JSON/Python/YAML/prompt text) + dependency list + usage notes.

Supported platforms: ComfyUI (node graph JSON), A1111/Forge (params.json),
HuggingFace Diffusers (pipeline.py), Replicate API (request.json),
Stability AI (API request), Midjourney (/imagine prompt), DALL·E, Ideogram.

Example inputs:
- "Generate an SDXL txt2img workflow with 2 LoRAs for ComfyUI"
- "Flux.1-dev + ControlNet depth for A1111 Forge"
- "Convert this ComfyUI JSON to Diffusers Python"
"""
    args_schema: Type[BaseModel] = WorkflowGeneratorInput

    skill_content: str = ""
    knowledge_base: dict = {}

    def _run(
        self,
        description: str,
        target_platform: Optional[str] = None,
        model_family: Optional[str] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        prompt = self._build_llm_prompt(description, target_platform, model_family)
        return prompt

    def _build_llm_prompt(
        self,
        description: str,
        target_platform: Optional[str] = None,
        model_family: Optional[str] = None,
    ) -> str:
        parts = [self.skill_content]

        if target_platform:
            parts.append(f"\n\n## Target Platform\n{target_platform}")
        if model_family:
            parts.append(f"\n## Model Family\n{model_family}")

        parts.append(f"\n\n## User Request\n{description}")
        parts.append("\n\nGenerate the complete workflow with all 3 artifacts (workflow file + dependencies.md + usage notes).")

        return "\n".join(parts)


def create_workflow_generator_tool(
    skill_md_path: str,
    knowledge_dir: str,
) -> WorkflowGeneratorTool:
    """Factory to create WorkflowGeneratorTool with loaded knowledge."""
    with open(skill_md_path, "r", encoding="utf-8") as f:
        skill_content = f.read()

    return WorkflowGeneratorTool(
        skill_content=skill_content,
        knowledge_base={},
    )
