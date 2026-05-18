"""Workflow template selector.

Maps (model_family, pipeline_type) → base template JSON file.
Falls back to sdxl_txt2img when no specific match.
"""

import json
from pathlib import Path
from typing import Optional

TEMPLATES_DIR = Path(__file__).resolve().parent.parent.parent / "templates" / "base"

TEMPLATE_MAP = {
    ("sd15", "txt2img"):       "sd15_txt2img.json",
    ("sd15", "img2img"):       "sd15_txt2img.json",
    ("sd15", "inpaint"):       "sd15_txt2img.json",
    ("sd15", "txt2vid"):       "sd15_txt2img.json",
    ("sdxl", "txt2img"):       "sdxl_txt2img.json",
    ("sdxl", "img2img"):       "sdxl_txt2img.json",
    ("sdxl", "inpaint"):       "sdxl_txt2img.json",
    ("sdxl_turbo", "txt2img"): "sdxl_txt2img.json",
    ("flux", "txt2img"):       "flux_txt2img.json",
    ("flux", "img2img"):       "flux_txt2img.json",
    ("flux", "inpaint"):       "flux_txt2img.json",
    ("sd3", "txt2img"):        "flux_txt2img.json",
    ("video", "txt2vid"):      "sd15_txt2img.json",
    ("video", "img2vid"):      "sd15_txt2img.json",
}

# Model families that require special handling beyond base template
REQUIRES_FLUX_GUIDANCE = {"flux", "sdxl_turbo"}
REQUIRES_16CH_LATENT = {"flux", "sd3"}
NO_NEGATIVE_PROMPT = {"flux", "sdxl_turbo"}
USES_DUAL_CLIP = {"sdxl", "sdxl_turbo"}
USES_TRIPLE_CLIP = {"sd3"}


def select_template(model_family: str, pipeline_type: str = "txt2img") -> str:
    """Return the template filename for the given model family and pipeline type."""
    key = (model_family.lower(), pipeline_type.lower())
    filename = TEMPLATE_MAP.get(key, "sdxl_txt2img.json")
    return str(TEMPLATES_DIR / filename)


def load_template(model_family: str, pipeline_type: str = "txt2img") -> dict:
    """Load and return the parsed template JSON."""
    path = select_template(model_family, pipeline_type)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def list_available_templates() -> list[str]:
    """List all available template filenames."""
    return sorted(p.name for p in TEMPLATES_DIR.glob("*.json"))


def has_template(model_family: str, pipeline_type: str = "txt2img") -> bool:
    """Check whether an exact template match exists."""
    key = (model_family.lower(), pipeline_type.lower())
    return key in TEMPLATE_MAP
