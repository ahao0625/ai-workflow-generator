"""Composable workflow module system.

Inserts module nodes (LoRA, ControlNet, IPAdapter, etc.) into a base
template at the correct splice points, adjusting node IDs and links.
"""

import copy
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

MODULES_DIR = Path(__file__).resolve().parent.parent.parent / "templates" / "modules"

# Which link positions in KSampler carry MODEL / CLIP / CONDITIONING
KSAMPLER_MODEL_INPUT_SLOT = 0
KSAMPLER_POSITIVE_INPUT_SLOT = 1
KSAMPLER_NEGATIVE_INPUT_SLOT = 2
KSAMPLER_LATENT_INPUT_SLOT = 3

# Node types we recognise as model loaders / encoders / samplers
MODEL_LOADER_TYPES = {"CheckpointLoaderSimple", "UNETLoader", "UnetLoaderGGUF"}
CLIP_ENCODE_TYPES = {"CLIPTextEncode", "CLIPTextEncodeSDXL", "CLIPTextEncodeFlux", "CLIPTextEncodeSD3"}
SAMPLER_TYPES = {"KSampler", "KSamplerAdvanced", "KSamplerSelect"}


def _find_node_by_type(workflow: dict, type_set: set) -> Optional[dict]:
    for node in workflow.get("nodes", []):
        if node.get("type") in type_set:
            return node
    return None


def _find_nodes_by_type(workflow: dict, type_set: set) -> list:
    return [n for n in workflow.get("nodes", []) if n.get("type") in type_set]


def _max_node_id(workflow: dict) -> int:
    ids = [n.get("id", 0) for n in workflow.get("nodes", [])]
    return max(ids) if ids else 0


def _max_link_id(workflow: dict) -> int:
    ids = [link[0] for link in workflow.get("links", [])]
    return max(ids) if ids else 0


def _shift_ids(obj: dict, node_id_shift: int, link_id_shift: int) -> dict:
    """Shift node IDs and link IDs in a template fragment by the given offsets."""
    obj = copy.deepcopy(obj)
    for node in obj.get("nodes", []):
        node["id"] = node.get("id", 0) + node_id_shift
        for inp in node.get("inputs", []):
            if inp.get("link") is not None:
                inp["link"] = inp["link"] + link_id_shift
        for out in node.get("outputs", []):
            out["links"] = [(lid + link_id_shift) for lid in out.get("links", [])]
    for link in obj.get("links", []):
        link[0] = link[0] + link_id_shift
        link[1] = link[1] + node_id_shift
        link[3] = link[3] + node_id_shift
    return obj


def _load_module(module_name: str) -> dict:
    path = MODULES_DIR / f"{module_name}.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def compose_lora(workflow: dict, lora_name: str, weight_model: float = 0.8,
                 weight_clip: float = 0.8) -> dict:
    """Insert a single LoRA node between model loader and KSampler.

    Threads both MODEL and CLIP through the LoraLoader (R07 compliance).
    For multiple LoRAs, call repeatedly — each call chains after the previous.
    """
    wf = copy.deepcopy(workflow)
    module = _load_module("lora_slot")
    tmpl = module["node_template"]

    # Determine where to insert: find the current MODEL source going into KSampler
    ksampler = _find_node_by_type(wf, SAMPLER_TYPES)
    if ksampler is None:
        return wf

    model_input = ksampler["inputs"][KSAMPLER_MODEL_INPUT_SLOT]
    prev_model_link_id = model_input.get("link")
    if prev_model_link_id is None:
        return wf

    # Find the source node of the MODEL link
    prev_model_link = next((l for l in wf["links"] if l[0] == prev_model_link_id), None)
    if prev_model_link is None:
        return wf

    prev_model_node_id = prev_model_link[1]
    prev_model_slot = prev_model_link[2]

    # Also find CLIP source (same node for CheckpointLoaderSimple, different for Flux)
    clip_input = ksampler.get("inputs", [])
    # Find CLIP link — look for CLIPTextEncode nodes that use CLIP
    clip_source_node_id = prev_model_node_id
    clip_source_slot = 1

    # Check if it's a CheckpointLoaderSimple (CLIP at slot 1) or separate loader
    prev_model_node = next((n for n in wf["nodes"] if n["id"] == prev_model_node_id), None)
    if prev_model_node and prev_model_node["type"] == "CheckpointLoaderSimple":
        clip_source_slot = 1

    # Build the new LoRA node
    new_node_id = _max_node_id(wf) + 1
    new_link_id = _max_link_id(wf) + 1

    new_node = copy.deepcopy(tmpl)
    new_node["id"] = new_node_id
    new_node["order"] = new_node_id - 1
    new_node["widgets_values"] = [
        f"{lora_name}.safetensors",
        weight_model,
        weight_clip,
    ]
    new_node["properties"]["Node name for S&R"] = f"LoRA {lora_name}"
    new_node["pos"] = [650, 580 + (len(_find_nodes_by_type(wf, {"LoraLoader"})) * 100)]

    # Wire inputs: MODEL from previous node, CLIP from same source's CLIP output
    new_node["inputs"][0]["link"] = prev_model_link_id
    # CLIP link — find the CLIP output link from the same source node
    clip_links = [l for l in wf["links"] if l[1] == clip_source_node_id and l[2] == clip_source_slot]
    if clip_links:
        new_node["inputs"][1]["link"] = clip_links[0][0]

    # Wire outputs
    new_model_link = [new_link_id, new_node_id, 0, ksampler["id"], KSAMPLER_MODEL_INPUT_SLOT, "MODEL"]
    new_clip_link = [new_link_id + 1, new_node_id, 1, clip_source_node_id, clip_source_slot, "CLIP"]
    new_node["outputs"][0]["links"] = [new_link_id]
    new_node["outputs"][1]["links"] = [new_link_id + 1]

    # Update KSampler model input to point to new LoRA node
    ksampler["inputs"][KSAMPLER_MODEL_INPUT_SLOT]["link"] = new_link_id

    # If CLIP encode nodes pointed to the old model loader's CLIP,
    # they should now point to the LoRA CLIP output (last in chain).
    # For LoRA chaining: the CLIP encode nodes stay connected to the LAST LoRA's CLIP output.
    for node in wf["nodes"]:
        if node["type"] in CLIP_ENCODE_TYPES:
            for inp in node.get("inputs", []):
                if inp.get("type") == "CLIP" and inp.get("link") == clip_links[0][0]:
                    inp["link"] = new_link_id + 1

    wf["nodes"].append(new_node)
    wf["links"].extend([new_model_link, new_clip_link])
    wf["last_node_id"] = new_node_id
    wf["last_link_id"] = new_link_id + 1

    return wf


def compose_controlnet(workflow: dict, cn_model: str, strength: float = 1.0,
                       start_percent: float = 0.0, end_percent: float = 1.0,
                       preprocessor_node: Optional[dict] = None) -> dict:
    """Insert a ControlNet chain into the conditioning path.

    For multiple ControlNets, call repeatedly for serial chaining (R11).
    """
    wf = copy.deepcopy(workflow)
    module = _load_module("controlnet_slot")

    ksampler = _find_node_by_type(wf, SAMPLER_TYPES)
    if ksampler is None:
        return wf

    # Get current positive conditioning link into KSampler
    positive_input = ksampler["inputs"][KSAMPLER_POSITIVE_INPUT_SLOT]
    prev_cond_link_id = positive_input.get("link")
    if prev_cond_link_id is None:
        return wf

    prev_cond_link = next((l for l in wf["links"] if l[0] == prev_cond_link_id), None)
    if prev_cond_link is None:
        return wf

    base_id = _max_node_id(wf)
    base_link = _max_link_id(wf)

    # ControlNetLoader node
    cn_loader = copy.deepcopy(module["nodes"][0])
    cn_loader_id = base_id + 1
    cn_loader["id"] = cn_loader_id
    cn_loader["widgets_values"] = [cn_model]
    cn_loader["outputs"][0]["links"] = [base_link + 1]
    existing_cns = _find_nodes_by_type(wf, {"ControlNetLoader"})
    cn_loader["pos"] = [650, 580 + (len(existing_cns) * 120)]

    # ControlNetApplyAdvanced node
    cn_apply = copy.deepcopy(module["nodes"][1])
    cn_apply_id = base_id + 2
    cn_apply["id"] = cn_apply_id
    cn_apply["widgets_values"] = [strength, start_percent, end_percent]
    cn_apply["inputs"][0]["link"] = prev_cond_link_id
    cn_apply["inputs"][2]["link"] = base_link + 1
    # Negative conditioning is shared (same as before, or None for Flux)
    negative_input = ksampler["inputs"][KSAMPLER_NEGATIVE_INPUT_SLOT]
    cn_apply["inputs"][1]["link"] = negative_input.get("link") if negative_input else None
    cn_apply["outputs"][0]["links"] = [base_link + 2]
    cn_apply["outputs"][1]["links"] = [base_link + 3]
    cn_apply["pos"] = [950, 580 + (len(existing_cns) * 120)]

    # Link: ControlNetLoader → ControlNetApplyAdvanced
    cn_link = [base_link + 1, cn_loader_id, 0, cn_apply_id, 2, "CONTROL_NET"]
    # Link: ControlNetApplyAdvanced positive conditioning → KSampler
    cond_link = [base_link + 2, cn_apply_id, 0, ksampler["id"], KSAMPLER_POSITIVE_INPUT_SLOT, "CONDITIONING"]

    # Redirect KSampler positive to CN output
    ksampler["inputs"][KSAMPLER_POSITIVE_INPUT_SLOT]["link"] = base_link + 2

    wf["nodes"].extend([cn_loader, cn_apply])
    wf["links"].extend([cn_link, cond_link])
    wf["last_node_id"] = cn_apply_id
    wf["last_link_id"] = base_link + 2

    return wf


def compose(workflow: dict, modules: List[Dict[str, Any]]) -> dict:
    """Apply a list of module descriptors to the base workflow.

    Each module dict should have at minimum a ``"type"`` key:
        {"type": "lora", "name": "add_detail", "weight_model": 0.8}
        {"type": "controlnet", "model": "control_v11p_sd15_canny.pth"}

    Returns a new workflow dict (original is not mutated).
    """
    wf = copy.deepcopy(workflow)

    for mod in modules:
        mod_type = mod.get("type", "")
        if mod_type == "lora":
            wf = compose_lora(
                wf,
                lora_name=mod["name"],
                weight_model=mod.get("weight_model", 0.8),
                weight_clip=mod.get("weight_clip", 0.8),
            )
        elif mod_type == "controlnet":
            wf = compose_controlnet(
                wf,
                cn_model=mod["model"],
                strength=mod.get("strength", 1.0),
                start_percent=mod.get("start_percent", 0.0),
                end_percent=mod.get("end_percent", 1.0),
            )
        else:
            # Unknown module type — skip with a warning
            pass

    return wf
