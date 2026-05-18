"""Schema registry.

Reads node widget schemas from ``metadata/node_widgets_schema.json`` at
import time and provides lookup helpers.  Falls back to a built-in minimal
set when the metadata file is absent.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional

METADATA_DIR = Path(__file__).resolve().parent.parent.parent / "metadata"

# Built-in fallback when metadata JSON is unavailable
_BUILTIN_FALLBACK: Dict[str, Dict[str, List[str]]] = {
    "KSampler": {
        "comfyui_0.3": [
            "seed", "control_after_generate", "steps", "cfg",
            "sampler_name", "scheduler", "denoise",
        ]
    },
    "KSamplerAdvanced": {
        "comfyui_0.3": [
            "seed", "control_after_generate", "steps", "cfg",
            "sampler_name", "scheduler", "denoise",
            "start_at_step", "end_at_step", "return_with_leftover_noise",
        ]
    },
    "CheckpointLoaderSimple": {
        "comfyui_0.3": ["ckpt_name"]
    },
    "UNETLoader": {
        "comfyui_0.3": ["unet_name", "weight_dtype"]
    },
    "DualCLIPLoader": {
        "comfyui_0.3": ["clip_name1", "clip_name2", "type"]
    },
    "VAELoader": {
        "comfyui_0.3": ["vae_name"]
    },
    "LoraLoader": {
        "comfyui_0.3": ["lora_name", "strength_model", "strength_clip"]
    },
    "CLIPTextEncode": {
        "comfyui_0.3": ["text"]
    },
    "CLIPTextEncodeSDXL": {
        "comfyui_0.3": [
            "text_g", "text_l", "width", "height",
            "target_width", "target_height", "crop_w", "crop_h",
        ]
    },
    "CLIPTextEncodeFlux": {
        "comfyui_0.3": ["text", "width", "height"]
    },
    "CLIPTextEncodeSD3": {
        "comfyui_0.3": [
            "text_g", "text_l", "text_t5", "width", "height",
            "target_width", "target_height", "crop_w", "crop_h",
        ]
    },
    "EmptyLatentImage": {
        "comfyui_0.3": ["width", "height", "batch_size"]
    },
    "EmptySD3LatentImage": {
        "comfyui_0.3": ["width", "height", "batch_size"]
    },
    "FluxGuidance": {
        "comfyui_0.3": ["guidance"]
    },
    "SaveImage": {
        "comfyui_0.3": ["filename_prefix"]
    },
    "PreviewImage": {
        "comfyui_0.3": ["filename_prefix"]
    },
    "ControlNetLoader": {
        "comfyui_0.3": ["control_net_name"]
    },
    "ControlNetApplyAdvanced": {
        "comfyui_0.3": ["strength", "start_percent", "end_percent"]
    },
    "IPAdapterModelLoader": {
        "comfyui_0.3": ["ipadapter_file"]
    },
    "CLIPVisionLoader": {
        "comfyui_0.3": ["clip_name"]
    },
    "IPAdapterApply": {
        "comfyui_0.3": ["weight", "weight_type", "combine_embeds"]
    },
    "VHS_VideoCombine": {
        "comfyui_0.3": [
            "frame_rate", "loop_count", "filename_prefix",
            "format", "pix_fmt", "crf", "save_metadata",
        ]
    },
    "LoadAnimateDiffModel": {
        "comfyui_0.3": ["motion_module"]
    },
    "AnimateDiffLoaderWithContext": {
        "comfyui_0.3": [
            "context_length", "context_stride", "context_overlap",
        ]
    },
}


def _load_schema() -> dict:
    path = METADATA_DIR / "node_widgets_schema.json"
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if data:
                return data
    return _BUILTIN_FALLBACK


# Module-level cache — loaded once on first access
_NODE_WIDGET_SCHEMA: Optional[dict] = None


def get_schema() -> dict:
    """Return the full node widget schema dict (cached)."""
    global _NODE_WIDGET_SCHEMA
    if _NODE_WIDGET_SCHEMA is None:
        _NODE_WIDGET_SCHEMA = _load_schema()
    return _NODE_WIDGET_SCHEMA


def get_widget_fields(node_type: str, version: str = "comfyui_0.3") -> List[str]:
    """Return the ordered list of widget fields for a given node type."""
    schema = get_schema()
    return schema.get(node_type, {}).get(version, [])


def get_widget_index(node_type: str, field_name: str, version: str = "comfyui_0.3") -> Optional[int]:
    """Return the positional index of a widget field, or None."""
    fields = get_widget_fields(node_type, version)
    try:
        return fields.index(field_name)
    except ValueError:
        return None


def list_node_types() -> List[str]:
    """List all known node types in the schema."""
    return sorted(get_schema().keys())
