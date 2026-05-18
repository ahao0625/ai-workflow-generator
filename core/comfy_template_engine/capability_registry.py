"""Node capability registry.

Reads node input/output port definitions from ``metadata/node_capabilities.json``
at import time.  Used to validate that links connect compatible port types
and that required inputs are satisfied.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

METADATA_DIR = Path(__file__).resolve().parent.parent.parent / "metadata"

# Built-in fallback when metadata JSON is absent or incomplete
_BUILTIN_FALLBACK: Dict[str, Dict[str, Any]] = {
    "CheckpointLoaderSimple": {
        "inputs": [],
        "outputs": ["MODEL", "CLIP", "VAE"],
        "compatible_models": ["sd15", "sdxl", "sdxl_turbo", "video"],
    },
    "UNETLoader": {
        "inputs": [],
        "outputs": ["MODEL"],
        "compatible_models": ["flux", "sd3"],
    },
    "DualCLIPLoader": {
        "inputs": [],
        "outputs": ["CLIP"],
        "compatible_models": ["flux"],
    },
    "VAELoader": {
        "inputs": [],
        "outputs": ["VAE"],
        "compatible_models": ["flux", "sd3"],
    },
    "CLIPTextEncode": {
        "inputs": ["CLIP"],
        "outputs": ["CONDITIONING"],
        "compatible_models": ["sd15", "video"],
    },
    "CLIPTextEncodeSDXL": {
        "inputs": ["CLIP"],
        "outputs": ["CONDITIONING"],
        "compatible_models": ["sdxl", "sdxl_turbo"],
    },
    "CLIPTextEncodeFlux": {
        "inputs": ["CLIP"],
        "outputs": ["CONDITIONING"],
        "compatible_models": ["flux"],
    },
    "CLIPTextEncodeSD3": {
        "inputs": ["CLIP"],
        "outputs": ["CONDITIONING"],
        "compatible_models": ["sd3"],
    },
    "FluxGuidance": {
        "inputs": ["CONDITIONING"],
        "outputs": ["CONDITIONING"],
        "compatible_models": ["flux"],
    },
    "EmptyLatentImage": {
        "inputs": [],
        "outputs": ["LATENT"],
        "compatible_models": ["sd15", "sdxl", "sdxl_turbo", "video"],
    },
    "EmptySD3LatentImage": {
        "inputs": [],
        "outputs": ["LATENT"],
        "compatible_models": ["flux", "sd3"],
    },
    "KSampler": {
        "inputs": ["MODEL", "CONDITIONING", "CONDITIONING", "LATENT"],
        "outputs": ["LATENT"],
        "compatible_models": ["sd15", "sdxl", "flux", "sd3", "video"],
    },
    "KSamplerAdvanced": {
        "inputs": ["MODEL", "CONDITIONING", "CONDITIONING", "LATENT"],
        "outputs": ["LATENT"],
        "compatible_models": ["sd15", "sdxl", "flux", "sd3"],
    },
    "VAEDecode": {
        "inputs": ["LATENT", "VAE"],
        "outputs": ["IMAGE"],
        "compatible_models": ["sd15", "sdxl", "flux", "sd3", "video"],
    },
    "VAEEncode": {
        "inputs": ["IMAGE", "VAE"],
        "outputs": ["LATENT"],
        "compatible_models": ["sd15", "sdxl"],
    },
    "VAEEncodeForInpaint": {
        "inputs": ["IMAGE", "MASK", "VAE"],
        "outputs": ["LATENT"],
        "compatible_models": ["sd15", "sdxl"],
    },
    "LoraLoader": {
        "inputs": ["MODEL", "CLIP"],
        "outputs": ["MODEL", "CLIP"],
        "compatible_models": ["sd15", "sdxl", "sdxl_turbo", "flux", "sd3"],
    },
    "ControlNetLoader": {
        "inputs": [],
        "outputs": ["CONTROL_NET"],
        "compatible_models": ["sd15", "sdxl"],
    },
    "ControlNetApplyAdvanced": {
        "inputs": ["CONDITIONING", "CONDITIONING", "CONTROL_NET"],
        "outputs": ["CONDITIONING", "CONDITIONING"],
        "compatible_models": ["sd15", "sdxl"],
    },
    "SaveImage": {
        "inputs": ["IMAGE"],
        "outputs": [],
        "compatible_models": ["sd15", "sdxl", "flux", "sd3", "video"],
    },
    "PreviewImage": {
        "inputs": ["IMAGE"],
        "outputs": [],
        "compatible_models": ["sd15", "sdxl", "flux", "sd3", "video"],
    },
    "VHS_VideoCombine": {
        "inputs": ["IMAGE"],
        "outputs": [],
        "compatible_models": ["video"],
    },
    "LoadAnimateDiffModel": {
        "inputs": [],
        "outputs": ["MOTION_MODULE"],
        "compatible_models": ["video"],
    },
    "AnimateDiffLoaderWithContext": {
        "inputs": ["MODEL", "MOTION_MODULE"],
        "outputs": ["MODEL"],
        "compatible_models": ["video"],
    },
    "IPAdapterModelLoader": {
        "inputs": [],
        "outputs": ["IPADAPTER"],
        "compatible_models": ["sd15", "sdxl"],
    },
    "CLIPVisionLoader": {
        "inputs": [],
        "outputs": ["CLIP_VISION"],
        "compatible_models": ["sd15", "sdxl"],
    },
    "IPAdapterApply": {
        "inputs": ["IPADAPTER", "CLIP_VISION", "IMAGE", "MODEL"],
        "outputs": ["MODEL"],
        "compatible_models": ["sd15", "sdxl"],
    },
    "LoadImage": {
        "inputs": [],
        "outputs": ["IMAGE", "MASK"],
        "compatible_models": ["sd15", "sdxl", "flux", "sd3", "video"],
    },
}


def _load_capabilities() -> dict:
    path = METADATA_DIR / "node_capabilities.json"
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if data:
                return data
    return _BUILTIN_FALLBACK


_NODE_CAPABILITIES: Optional[dict] = None


def get_capabilities() -> dict:
    """Return the full node capabilities dict (cached)."""
    global _NODE_CAPABILITIES
    if _NODE_CAPABILITIES is None:
        _NODE_CAPABILITIES = _load_capabilities()
    return _NODE_CAPABILITIES


def get_inputs(node_type: str) -> List[str]:
    """Return the ordered list of input port names for a node type."""
    caps = get_capabilities()
    return caps.get(node_type, {}).get("inputs", [])


def get_outputs(node_type: str) -> List[str]:
    """Return the ordered list of output port names for a node type."""
    caps = get_capabilities()
    return caps.get(node_type, {}).get("outputs", [])


def get_compatible_models(node_type: str) -> List[str]:
    """Return the list of model families this node type supports."""
    caps = get_capabilities()
    return caps.get(node_type, {}).get("compatible_models", [])


def is_compatible(node_type: str, model_family: str) -> bool:
    """Check whether a node type is compatible with a given model family."""
    models = get_compatible_models(node_type)
    if not models:
        return True  # unknown nodes default to compatible
    return model_family in models


def list_node_types() -> List[str]:
    """List all known node types in the capability registry."""
    return sorted(get_capabilities().keys())


def validate_node_compatibility(workflow: dict, model_family: str) -> List[str]:
    """Check all nodes in a workflow for model-family compatibility.

    Returns a list of human-readable warnings for incompatible nodes.
    """
    warnings: List[str] = []
    caps = get_capabilities()

    for node in workflow.get("nodes", []):
        node_type = node.get("type", "")
        if node_type not in caps:
            continue

        compatible = caps[node_type].get("compatible_models", [])
        if compatible and model_family not in compatible:
            warnings.append(
                f"Node {node['id']} ({node_type}) may not be compatible "
                f"with model family '{model_family}'"
            )

    return warnings
