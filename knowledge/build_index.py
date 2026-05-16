import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional


KNOWLEDGE_DIR = Path(__file__).resolve().parent
CACHE_DIR = KNOWLEDGE_DIR / ".cache"
CACHE_FILE = CACHE_DIR / "index.json"


def _load_yaml_safe(yaml_path: Path) -> Dict[str, Any]:
    contents: Dict[str, Any] = {}
    current_key: Optional[str] = None
    current_indent = 0
    list_buffer: List[str] = []

    try:
        with open(yaml_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        return contents

    for line in lines:
        stripped = line.rstrip()
        if not stripped or stripped.startswith("#"):
            continue
        indent = len(line) - len(line.lstrip())
        if stripped.endswith(":") and not stripped.startswith("-"):
            key = stripped.rstrip(":").strip()
            if key.startswith("&") or key.startswith("*"):
                continue
            contents[key] = ""
            current_key = key
            current_indent = indent
        elif current_key and indent > current_indent:
            val = stripped.lstrip("- ").strip().strip('"').strip("'")
            if val:
                if current_key not in contents or not isinstance(contents[current_key], list):
                    if isinstance(contents.get(current_key), str) and contents.get(current_key) == "":
                        contents[current_key] = []
                if isinstance(contents.get(current_key), list):
                    contents[current_key].append(val)
                else:
                    contents[current_key] = val
    return contents


def build_model_index() -> Dict[str, Any]:
    index: Dict[str, Any] = {}
    models_dir = KNOWLEDGE_DIR / "models"
    if not models_dir.exists():
        return index
    for yaml_file in sorted(models_dir.glob("*.yaml")):
        model_key = yaml_file.stem
        raw = _load_yaml_safe(yaml_file)
        family = raw.get("model_family", model_key)
        arch = raw.get("architecture", {})
        variants = raw.get("variants", {})
        index[model_key] = {
            "family": str(family),
            "base_resolution": arch.get("base_resolution") if isinstance(arch, dict) else None,
            "latent_channels": arch.get("latent_channels") if isinstance(arch, dict) else None,
            "has_negative_prompt": not arch.get("negative_prompt") == False if isinstance(arch, dict) else True,
            "variants": list(variants.keys()) if isinstance(variants, dict) else [],
            "recommended_sampler": None,
            "recommended_scheduler": None,
            "recommended_steps": None,
            "recommended_cfg": None,
        }
        if isinstance(variants, dict):
            for vname, vdata in variants.items():
                if isinstance(vdata, dict):
                    if not index[model_key]["recommended_steps"]:
                        index[model_key]["recommended_steps"] = vdata.get("steps")
                        index[model_key]["recommended_cfg"] = vdata.get("cfg")
                        index[model_key]["recommended_sampler"] = vdata.get("sampler")
                        index[model_key]["recommended_scheduler"] = vdata.get("scheduler")
    return index


def build_node_index() -> Dict[str, Any]:
    index: Dict[str, Any] = {}
    nodes_dir = KNOWLEDGE_DIR / "nodes"
    if not nodes_dir.exists():
        return index
    for yaml_file in sorted(nodes_dir.glob("*.yaml")):
        node_key = yaml_file.stem
        raw = _load_yaml_safe(yaml_file)
        index[node_key] = {
            "node_count": 0,
            "categories": [],
        }
    return index


def build_platform_index() -> Dict[str, Any]:
    index: Dict[str, Any] = {}
    platforms_dir = KNOWLEDGE_DIR / "platforms"
    if not platforms_dir.exists():
        return index
    for yaml_file in sorted(platforms_dir.glob("*.yaml")):
        platform_key = yaml_file.stem
        raw = _load_yaml_safe(yaml_file)
        output_formats = raw.get("output_formats")
        if isinstance(output_formats, list):
            output_formats = output_formats
        else:
            output_formats = []
        index[platform_key] = {
            "platform": raw.get("platform", platform_key),
            "output_formats": output_formats,
        }
    return index


def build_full_index() -> Dict[str, Any]:
    return {
        "models": build_model_index(),
        "nodes": build_node_index(),
        "platforms": build_platform_index(),
    }


def get_cached_index() -> Optional[Dict[str, Any]]:
    if CACHE_FILE.exists():
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None
    return None


def rebuild_cache() -> Dict[str, Any]:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    index = build_full_index()
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
    return index


def query_index(model: Optional[str] = None, platform: Optional[str] = None) -> Dict[str, Any]:
    cached = get_cached_index()
    if cached is None:
        cached = rebuild_cache()
    result: Dict[str, Any] = {}
    if model and model in cached.get("models", {}):
        result["model"] = cached["models"][model]
    if platform and platform in cached.get("platforms", {}):
        result["platform"] = cached["platforms"][platform]
    return result


if __name__ == "__main__":
    idx = rebuild_cache()
    print(f"Indexed {len(idx.get('models', {}))} models, "
          f"{len(idx.get('nodes', {}))} node categories, "
          f"{len(idx.get('platforms', {}))} platforms")
    print(f"Cache written to {CACHE_FILE}")
