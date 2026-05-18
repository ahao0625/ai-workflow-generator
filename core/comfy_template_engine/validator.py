"""Workflow validator.

Validates a rendered ComfyUI workflow against structural and semantic rules.
Integrates with knowledge/validators/rules.yaml via the IR validation system
and adds template-engine-specific structural checks.
"""

import copy
from typing import Any, Dict, List, Set

# Node types that qualify as terminal / output nodes
TERMINAL_NODE_TYPES = {"SaveImage", "PreviewImage", "VHS_VideoCombine", "SaveAnimatedWEBP"}

# Known port types for type-safety checks
PORT_TYPES = {"MODEL", "CLIP", "VAE", "LATENT", "IMAGE", "MASK", "CONDITIONING", "CONTROL_NET",
              "CLIP_VISION", "IPADAPTER", "MOTION_MODULE", "UPSCALE_MODEL"}

# Model-loader node types
MODEL_LOADER_TYPES = {"CheckpointLoaderSimple", "UNETLoader", "UnetLoaderGGUF", "DualCLIPLoader",
                      "TripleCLIPLoader", "CLIPLoader", "VAELoader", "CLIPLoaderGGUF"}

# Sampler node types
SAMPLER_TYPES = {"KSampler", "KSamplerAdvanced", "KSamplerSelect"}


def _build_port_map(workflow: dict) -> Dict[int, str]:
    """Build a map of link_id → port type string."""
    port_map: Dict[int, str] = {}
    for node in workflow.get("nodes", []):
        for out in node.get("outputs", []):
            port_type = out.get("type", "")
            for link_id in out.get("links", []):
                port_map[link_id] = port_type
    return port_map


def _build_node_map(workflow: dict) -> Dict[int, dict]:
    return {n["id"]: n for n in workflow.get("nodes", [])}


def validate_workflow(workflow: dict) -> Dict[str, Any]:
    """Run all structural validation checks on a ComfyUI workflow.

    Returns ``{"valid": bool, "errors": [str], "warnings": [str]}``.
    """
    errors: List[str] = []
    warnings: List[str] = []

    # ── structural checks ──────────────────────────────────────────
    if "nodes" not in workflow:
        errors.append("Missing top-level 'nodes' array")
        return {"valid": False, "errors": errors, "warnings": warnings}

    if "links" not in workflow:
        errors.append("Missing top-level 'links' array — nodes will have no visible connections in ComfyUI")

    nodes = workflow.get("nodes", [])
    links = workflow.get("links", [])

    # R09: unique node IDs
    node_ids: Set[int] = set()
    for node in nodes:
        nid = node.get("id")
        if nid is None:
            errors.append("Node has no 'id' field")
        elif nid in node_ids:
            errors.append(f"Duplicate node ID: {nid} (R09)")
        else:
            node_ids.add(nid)

    # R08: terminal node required
    has_terminal = any(n.get("type") in TERMINAL_NODE_TYPES for n in nodes)
    if not has_terminal:
        errors.append("Workflow must have a terminal output node (SaveImage / PreviewImage / VHS_VideoCombine) (R08)")

    # R10: type-safe connections
    port_map = _build_port_map(workflow)
    node_map = _build_node_map(workflow)
    link_ids_seen: Set[int] = set()

    for link in links:
        if len(link) < 6:
            errors.append(f"Malformed link (expected 6 elements): {link}")
            continue

        link_id, from_node, from_slot, to_node, to_slot, port_type = link

        if link_id in link_ids_seen:
            errors.append(f"Duplicate link ID: {link_id}")
        link_ids_seen.add(link_id)

        source_port = port_map.get(link_id)
        if source_port and source_port != port_type:
            warnings.append(
                f"Link {link_id}: declared type '{port_type}' does not match "
                f"source port type '{source_port}' (R10)"
            )

        if from_node not in node_map:
            errors.append(f"Link {link_id}: source node {from_node} not found")
        if to_node not in node_map:
            errors.append(f"Link {link_id}: target node {to_node} not found")

    # Check every node input has exactly one source connection (ComfyUI rule)
    for node in nodes:
        for inp in node.get("inputs", []):
            if inp.get("link") is None and inp.get("type", -1) == -1:
                continue  # widget constant, no link needed
            if inp.get("link") is None:
                warnings.append(
                    f"Node {node['id']} ({node.get('type')}): "
                    f"input '{inp.get('name')}' has no connection"
                )

    # R07: LoRA must thread both MODEL and CLIP
    lora_nodes = [n for n in nodes if n.get("type") == "LoraLoader"]
    for lora in lora_nodes:
        model_connected = any(
            inp.get("name") == "model" and inp.get("link") is not None
            for inp in lora.get("inputs", [])
        )
        clip_connected = any(
            inp.get("name") == "clip" and inp.get("link") is not None
            for inp in lora.get("inputs", [])
        )
        if not model_connected or not clip_connected:
            errors.append(
                f"LoRA node {lora['id']}: both MODEL and CLIP must be connected (R07)"
            )

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
    }


def validate_against_ir(workflow: dict, ir_errors: List[str]) -> Dict[str, Any]:
    """Merge structural validation with IR-level semantic errors.

    Args:
        workflow: The rendered ComfyUI workflow dict.
        ir_errors: Validation errors from ``WorkflowIR.validate()``.

    Returns a combined result dict.
    """
    result = validate_workflow(workflow)
    if ir_errors:
        result["errors"].extend(ir_errors)
        result["valid"] = False
    return result
