# Engineering Upgrade

This project has been upgraded with a **ComfyUI Template Engine** — a
deterministic, schema-driven system that replaces ad-hoc LLM graph topology
generation with composable templates.

## Architecture

```
User Prompt → WorkflowIR → ComfyUI Template Engine → workflow.json
                │                    │
         (validation)    ┌───────────┼───────────┐
                         │           │           │
                    template      module      injector
                    selector     composer      + validator
```

### Components

| Module | Purpose |
|--------|---------|
| `template_selector` | Maps `(model_family, pipeline_type)` to a base template JSON with `{{placeholder}}` markers |
| `module_composer` | Inserts optional modules (LoRA, ControlNet, IPAdapter) into the base template at the correct splice points, adjusting node/link IDs |
| `injector` | Replaces `{{placeholder}}` markers with actual parameter values using the widget schema registry |
| `validator` | Structural checks (terminal node, unique IDs, type-safe links, LoRA threading) integrated with IR-level rules |
| `schema_registry` | Reads node widget field order from `metadata/node_widgets_schema.json` (with built-in fallback for 30+ node types) |
| `capability_registry` | Reads node I/O port definitions and model-family compatibility from `metadata/node_capabilities.json` (with built-in fallback) |

### Templates

Base templates in `templates/base/`:
- `sdxl_txt2img.json` — SDXL (and SD1.5) txt2img, 7 nodes
- `flux_txt2img.json` — Flux.1 txt2img (DualCLIP + FluxGuidance + 16ch latent), 9 nodes
- `sd15_txt2img.json` — SD1.5 txt2img (single CLIP, 4ch latent), 7 nodes

Module slots in `templates/modules/`:
- `lora_slot.json` — LoRA (threads MODEL+CLIP, R07 compliant)
- `controlnet_slot.json` — ControlNet (serial chaining, R11 compliant)
- `ipadapter_slot.json` — IPAdapter (model + CLIP vision)

### Usage

```python
from core import (
    load_template, compose, inject_parameters,
    validate_workflow, fill_defaults,
    REQUIRES_FLUX_GUIDANCE, NO_NEGATIVE_PROMPT,
)

# 1. Select and load the base template
wf = load_template("flux", "txt2img")

# 2. Compose optional modules into the graph
wf = compose(wf, [
    {"type": "lora", "name": "add_detail", "weight_model": 0.8},
])

# 3. Inject user parameters (replaces {{placeholders}})
wf = inject_parameters(wf, {
    "positive_prompt": "a cyberpunk city at night",
    "steps": 4,
    "cfg": 1.0,
    "guidance": 1.0,
})

# 4. Fill any remaining placeholders with defaults
wf = fill_defaults(wf)

# 5. Validate
result = validate_workflow(wf)
print(result["valid"], result["errors"], result["warnings"])
```

### Key design decisions

- **AI is no longer responsible for graph topology.** The LLM only needs to
  select the right template and provide parameter values. Node placement,
  link wiring, and ID assignment are handled deterministically.
- **Templates use `{{placeholder}}` markers.** This makes them human-readable
  and easy to verify without running Python code.
- **Schemas have built-in fallbacks.** Both registries include comprehensive
  hardcoded defaults, so they work even if the JSON metadata files are absent.
- **The IR layer (`WorkflowIR.validate()`) remains the source of truth for
  semantic rules** (R01–R24). The template validator adds structural checks
  specific to rendered ComfyUI JSON.
