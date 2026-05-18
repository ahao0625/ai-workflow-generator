"""Workflow parameter injector.

Replaces ``{{placeholder}}`` markers in a template workflow with actual
parameter values from a dict.  Uses the schema registry for safe, typed
injection instead of brittle positional-index access.
"""

import copy
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

METADATA_DIR = Path(__file__).resolve().parent.parent.parent / "metadata"

# Regex for template placeholders: {{variable_name}}
_PLACEHOLDER_RE = re.compile(r"\{\{(\w+)\}\}")

# Node types that carry a text prompt
_PROMPT_NODE_TYPES = {"CLIPTextEncode", "CLIPTextEncodeSDXL", "CLIPTextEncodeFlux", "CLIPTextEncodeSD3"}

# Widget index maps for known node types (used when schema metadata is unavailable)
_WIDGET_INDEX = {
    "KSampler": {"seed": 0, "control_after_generate": 1, "steps": 2, "cfg": 3,
                 "sampler_name": 4, "scheduler": 5, "denoise": 6},
    "KSamplerAdvanced": {"seed": 0, "control_after_generate": 1, "steps": 2, "cfg": 3,
                         "sampler_name": 4, "scheduler": 5, "denoise": 6,
                         "start_at_step": 7, "end_at_step": 8, "return_with_leftover_noise": 9},
    "EmptyLatentImage": {"width": 0, "height": 1, "batch_size": 2},
    "EmptySD3LatentImage": {"width": 0, "height": 1, "batch_size": 2},
    "CheckpointLoaderSimple": {"ckpt_name": 0},
    "UNETLoader": {"unet_name": 0, "weight_dtype": 1},
    "DualCLIPLoader": {"clip_name1": 0, "clip_name2": 1, "type": 2},
    "VAELoader": {"vae_name": 0},
    "LoraLoader": {"lora_name": 0, "strength_model": 1, "strength_clip": 2},
    "FluxGuidance": {"guidance": 0},
    "SaveImage": {"filename_prefix": 0},
    "PreviewImage": {"filename_prefix": 0},
}


def _load_widget_schema() -> dict:
    """Load node widget schema from metadata JSON."""
    path = METADATA_DIR / "node_widgets_schema.json"
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def _resolve_widget_index(node_type: str, param_name: str) -> Optional[int]:
    """Resolve a parameter name to its widget index for a given node type.

    Checks metadata JSON first, then falls back to the hardcoded index map.
    """
    schema = _load_widget_schema()
    if node_type in schema:
        for version_key, fields in schema[node_type].items():
            try:
                return fields.index(param_name)
            except ValueError:
                continue
    return _WIDGET_INDEX.get(node_type, {}).get(param_name)


def _replace_placeholders(values: list, params: Dict[str, Any], node_type: str) -> list:
    """Replace ``{{placeholder}}`` strings in widget values with actual params.

    Falls back to index-based injection for nodes without placeholder markers.
    """
    result = []
    for i, val in enumerate(values):
        if isinstance(val, str):
            match = _PLACEHOLDER_RE.fullmatch(val)
            if match:
                key = match.group(1)
                if key in params:
                    result.append(params[key])
                else:
                    result.append(val)
            else:
                # Partial placeholder replacement within a string
                result.append(_PLACEHOLDER_RE.sub(
                    lambda m: str(params.get(m.group(1), m.group(0))), val))
        else:
            result.append(val)
    return result


def _inject_by_schema(widgets: list, params: Dict[str, Any], node_type: str) -> list:
    """Schema-aware injection: replace placeholders AND apply index-based overrides."""
    widgets = _replace_placeholders(widgets, params, node_type)

    # Also apply direct index-based injection for params without placeholders
    for key, value in params.items():
        idx = _resolve_widget_index(node_type, key)
        if idx is not None and idx < len(widgets):
            if widgets[idx] == value:
                continue  # already injected via placeholder
            # Only override if the current value is still a placeholder or default
            if isinstance(widgets[idx], str) and _PLACEHOLDER_RE.match(str(widgets[idx])):
                widgets[idx] = value

    return widgets


def inject_parameters(workflow: dict, parameters: Dict[str, Any]) -> dict:
    """Inject parameters into a template workflow.

    Handles two modes:
    1. **Placeholder mode** — template nodes contain ``{{param}}`` markers;
       these are replaced directly.
    2. **Schema mode** — when no placeholders, uses the widget index map
       to inject into the correct slot.

    Returns a new workflow dict.
    """
    wf = copy.deepcopy(workflow)

    for node in wf.get("nodes", []):
        node_type = node.get("type", "")
        widgets = node.get("widgets_values", [])

        if not widgets:
            continue

        new_widgets = _inject_by_schema(list(widgets), parameters, node_type)
        node["widgets_values"] = new_widgets

    return wf


def extract_placeholders(workflow: dict) -> List[str]:
    """Return a sorted list of unique placeholder names found in the workflow."""
    placeholders = set()
    for node in workflow.get("nodes", []):
        for val in node.get("widgets_values", []):
            if isinstance(val, str):
                for match in _PLACEHOLDER_RE.finditer(val):
                    placeholders.add(match.group(1))
    return sorted(placeholders)


def fill_defaults(workflow: dict) -> dict:
    """Fill remaining ``{{placeholders}}`` with sensible defaults so the workflow is always valid."""
    defaults = {
        "checkpoint": "sd_xl_base_1.0.safetensors",
        "clip_name1": "t5xxl_fp8_e4m3fn.safetensors",
        "clip_name2": "clip_l.safetensors",
        "unet_name": "flux1-dev-fp8.safetensors",
        "weight_dtype": "default",
        "vae_name": "ae.safetensors",
        "positive_prompt": "masterpiece, best quality",
        "negative_prompt": "worst quality, low quality",
        "width": 1024,
        "height": 1024,
        "batch_size": 1,
        "seed": -1,
        "steps": 25,
        "cfg": 7.0,
        "sampler_name": "euler",
        "scheduler": "karras",
        "denoise": 1.0,
        "guidance": 3.5,
        "filename_prefix": "ComfyUI",
    }
    wf = copy.deepcopy(workflow)
    for node in wf.get("nodes", []):
        widgets = node.get("widgets_values", [])
        if widgets:
            node["widgets_values"] = _replace_placeholders(list(widgets), defaults, node.get("type", ""))
    return wf
