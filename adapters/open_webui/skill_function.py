"""
Open WebUI Tools — AI Workflow Generator Skill
Put this file in ~/.open-webui/tools/ or load via Admin → Tools → Add Tool.

Open WebUI工具模块 — AI工作流生成器技能
将此文件放入 ~/.open-webui/tools/ 或在Admin→Tools→Add Tool中加载。

Usage: The skill function is called when the LLM decides to use it.
The function receives parameters and returns a structured prompt that
includes all SKILL.md knowledge for the LLM to process.
"""

import os
import json


class Tools:
    """
    AI Workflow Generator — Open WebUI Tools format.
    This class is auto-discovered by Open WebUI's tool system.
    """

    class Valves:
        """
        Configuration values for this tool.
        Adjust in Open WebUI Admin → Tools → Valves tab.
        """
        skill_content: str = ""
        knowledge_dir: str = ""

    # Load SKILL.md and knowledge on startup
    try:
        _skill_path = os.path.join(os.path.dirname(__file__), "..", "..", "SKILL.md")
        if os.path.exists(_skill_path):
            with open(_skill_path, "r", encoding="utf-8") as f:
                skill_content = f.read()
        else:
            skill_content = "SKILL.md not found. Load manually."
    except Exception:
        skill_content = "SKILL.md not found. Load manually."

    def generate_workflow(
        self,
        description: str,
        target_platform: str = "comfyui",
        model_family: str = "sdxl",
    ) -> str:
        """
        Generate an AI image/video workflow file for the specified platform.

        :param description: Natural language description of the workflow.
            Example: "SDXL txt2img with 2 LoRAs and ControlNet depth for ComfyUI"
        :param target_platform: Target platform. One of: comfyui, a1111, diffusers,
            replicate, stability, midjourney, dalle, ideogram. Default: comfyui.
        :param model_family: Model family. One of: sd15, sdxl, sdxl_turbo, flux,
            sd3, video. Default: sdxl.
        :return: Generated workflow (JSON, Python code, or prompt text) with dependencies
            and usage instructions.
        """
        prompt = f"""You are an AI workflow generator.

{self.skill_content}

## User Request
{description}

## Target Platform
{target_platform}

## Model Family
{model_family}

Follow the 5-step process in SKILL.md:
1. Confirm target platform: {target_platform}
2. Build IR from description
3. Validate against rules
4. Render to {target_platform} format
5. Output workflow file + dependencies.md + usage notes

Generate the complete workflow now. Output all 3 artifacts."""
        return prompt

    def validate_workflow(self, workflow_json: str, target_platform: str = "comfyui") -> str:
        """
        Validate an existing workflow against known rules.

        :param workflow_json: The workflow content to validate (JSON for ComfyUI/A1111,
            Python code for Diffusers).
        :param target_platform: The platform this workflow targets.
        :return: Validation report with any issues found.
        """
        prompt = f"""You are an AI workflow validator.

{self.skill_content}

## Validation Target
Platform: {target_platform}

## Workflow to Validate
```json
{workflow_json}
```

Apply all validation rules from rules.yaml. Report:
- CRITICAL issues (must fix)
- ADVISORY warnings (recommended fixes)
- Any missing dependencies

Output a structured validation report. Highlight failures first, then warnings."""
        return prompt

    def convert_workflow(
        self,
        source_workflow: str,
        source_platform: str,
        target_platform: str,
    ) -> str:
        """
        Convert a workflow from one platform format to another.

        :param source_workflow: The existing workflow content (JSON, Python, prompt).
        :param source_platform: Source platform (comfyui/a1111/diffusers/midjourney).
        :param target_platform: Target platform to convert to.
        :return: Converted workflow in target platform format.
        """
        prompt = f"""You are an AI workflow converter.

{self.skill_content}

## Conversion Task
Convert from {source_platform} to {target_platform}.

## Source Workflow
```json
{source_workflow}
```

Parse the source workflow → extract IR fields → validate → render to {target_platform}.
Note any conversion losses (e.g., LoRA embedded in prompt → separate nodes).
Output the converted workflow + updated dependencies.md + usage notes."""
        return prompt
