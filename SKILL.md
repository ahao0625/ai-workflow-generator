---
name: ai-workflow-generator
description: |
  Universal AI image/video generation workflow builder. Use this skill whenever the user mentions:
  - ComfyUI, A1111, InvokeAI, Forge, Fooocus, Diffusers, or any image generation platform
  - "generate a workflow", "build a pipeline", "create a comfyui json"
  - Any combination of: model (SD1.5/SDXL/Flux/SD3/video) + technique (ControlNet/LoRA/IPAdapter/inpaint/animatediff)
  - "convert workflow from X to Y platform"
  - Requests for Stable Diffusion, Flux, or video generation setup/code
  Trigger even if the user only partially describes a workflow (e.g. "I want to use Flux with a LoRA").
  Output is always a ready-to-use file (JSON / Python / YAML / prompt text) plus a dependency manifest.
---

# AI Workflow Generator / AI工作流生成器

> **Bilingual skill / 双语技能**: All knowledge files use Chinese + English parallel notation.  
> **Capability levels / 能力等级**: L1 (any LLM) → L4 (file I/O + tool calls). Degrade gracefully.

---

## Quick Reference / 快速参考

| Step | Action |
|------|--------|
| 1 | Detect target platform → load platform renderer |
| 2 | Parse intent → build IR (Internal Representation) |
| 3 | Validate IR against model compatibility rules |
| 4 | Render IR → platform-native format |
| 5 | Output: workflow file + `dependencies.md` + usage notes |

---

## Knowledge Files / 知识文件索引

Read the relevant file(s) before rendering. Use ALL applicable files for complex workflows.

```
knowledge/ir_schema.yaml         ← ALWAYS read first / 始终先读
knowledge/validators/rules.yaml  ← ALWAYS read / 始终读

knowledge/models/sd15.yaml       ← SD 1.x workflows
knowledge/models/sdxl.yaml       ← SDXL / Turbo / Lightning workflows  
knowledge/models/flux.yaml       ← Flux.1 dev/schnell/Fill/Canny/Depth
knowledge/models/sd3.yaml        ← SD3 / SD3.5 workflows
knowledge/models/video.yaml      ← AnimateDiff / SVD / CogVideoX / Wan / Hunyuan

knowledge/nodes/native_nodes.yaml   ← ComfyUI built-in nodes (100+)
knowledge/nodes/custom_nodes.yaml   ← Ecosystem extensions (IPAdapter/InstantID/etc)

knowledge/platforms/comfyui.yaml    ← Node JSON renderer
knowledge/platforms/a1111.yaml      ← A1111 / Forge parameter renderer
knowledge/platforms/diffusers.yaml  ← HuggingFace Diffusers Python renderer
knowledge/platforms/api.yaml        ← REST API body renderer (Replicate/Stability/etc)
knowledge/platforms/prompt_only.yaml ← Midjourney / DALL·E / Ideogram prompt renderer
knowledge/platforms/invokeai.yaml   ← InvokeAI Node Editor JSON renderer
```

---

## Programmatic IR Layer / 可编程中间表示层

For developers integrating this skill into Agent / MCP / Tool-calling systems, use the programmatic IR in `core/ir/`:

```python
from core import WorkflowIR, ModelFamily, PipelineType, TargetPlatform, SamplingParams, LoraRef

ir = WorkflowIR(
    model_family=ModelFamily.SDXL,
    pipeline_type=PipelineType.TXT2IMG,
    target_platform=TargetPlatform.COMFYUI,
    prompt="a beautiful landscape, masterpiece",
    negative_prompt="worst quality",
    sampling=SamplingParams.defaults_for(ModelFamily.SDXL),
    loras=[
        LoraRef(name="add_detail", weight_model=0.8),
        LoraRef(name="epiNoiseoffset", weight_model=0.6, weight_clip=0.6),
    ],
)

ir.validate()                # → list of validation errors
ir.supports_negative_prompt() # → model-family-aware check
ir.get_unique_dependencies()  # → all referenced model file names
```

**Key classes / 核心类:**

| Module | Purpose |
|--------|---------|
| `core/ir/parameter.py` | All enums (ModelFamily, PipelineType, TargetPlatform…) + dataclasses (SamplingParams, LoraRef, ControlNetRef, IPAdapterRef, AnimateDiffParams…) |
| `core/ir/node.py` | IRNode, NodeConnection, NodePort, STANDARD_NODE_PORTS — platform-agnostic node graph types |
| `core/ir/workflow.py` | `WorkflowIR` — the single source of truth for every workflow. `validate()`, `to_dict()`, `uses_dual_clip()`, `needs_flux_guidance()` … |
| `core/ir/translator.py` | `PlatformTranslator` ABC with `translate()`, `parse()`, `roundtrip_check()` — all adapters implement this |

**Adapter registry / 适配器注册:**

```python
from adapters.base_adapter import BaseAdapter, AdapterRegistry

# Find all adapters that support a given model+pipe combo
adapters = AdapterRegistry.find_adapter(ModelFamily.FLUX, PipelineType.TXT2IMG)

# Translate IR directly to a target platform
output = AdapterRegistry.translate(ir, TargetPlatform.COMFYUI)
```

**Knowledge index / 知识索引:**

```bash
python3 knowledge/build_index.py
# → knowledge/.cache/index.json (auto-generated, gitignored)
```

```python
from knowledge.build_index import query_index
query_index(model="flux", platform="comfyui")
```

---

## Step 1 — Platform Detection / 平台识别

### Explicit / 明确指定
User mentions a platform name → use it directly.

### Implicit / 隐含推断
| Signal / 信号 | Infer Platform / 推断平台 |
|---|---|
| "node", "节点", "JSON workflow" | ComfyUI |
| "webui", "a1111", "automatic" | A1111 |
| "python", "pipeline", "diffusers" | Diffusers |
| "api", "replicate", "stability ai" | API |
| "midjourney", "/imagine", "--ar" | Prompt-only |
| "forge" | A1111 (Forge variant) |
| "invoke", "invokeai" | InvokeAI (→ load knowledge/platforms/invokeai.yaml) |

### Unknown / 未知
If platform cannot be inferred, ask ONE question:
> "Which platform? / 使用哪个平台？ ComfyUI · A1111 · Diffusers · API · Other"

---

## Step 2 — Intent Parsing → IR Construction / 意图解析 → 构建中间表示

Load `knowledge/ir_schema.yaml` for the full IR schema.

**Parse in this order / 按此顺序解析:**
1. `model_family` — which model generation? (sd15 / sdxl / flux / sd3 / video)
2. `pipeline_type` — what kind of generation? (txt2img / img2img / inpaint / vid)
3. `modules[]` — which optional features? (lora / controlnet / ipadapter / upscale / etc.)
4. `params` — numerical settings (size, steps, cfg, seed…)
5. `output_format` — file format preference

**Defaults when unspecified / 未指定时的默认值:**
- model_family: `sdxl` (most versatile / 最通用)
- pipeline_type: `txt2img`
- size: model-family default (see model files)
- steps / cfg: model-family default
- seed: `-1` (random)

---

## Step 3 — Validation / 验证

Load `knowledge/validators/rules.yaml`.  
Run ALL rules against the constructed IR.  
**Block rendering if any CRITICAL rule fails. Warn for ADVISORY rules.**

Common cross-model conflicts to catch early:
- Flux has NO negative prompt → remove from IR silently, add note
- SD3 uses 3-way text encoding → cannot use CLIPTextEncode
- Inpaint pipeline MUST use VAEEncodeForInpaint, not VAEEncode
- LoRA must thread both MODEL and CLIP outputs (not just MODEL)

---

## Step 4 — Rendering / 渲染

Load the target platform file from `knowledge/platforms/`.  
Load the model-specific file from `knowledge/models/`.  
Load node definitions from `knowledge/nodes/` (ComfyUI targets only).

**Render the complete workflow following the platform renderer's instructions.**

Node ID assignment (ComfyUI): start at `1`, increment by `1`, topological order (sources first).  
Layout coordinates: `x` increases left→right in steps of `300`, `y` groups by layer.

**⚠️ CRITICAL for ComfyUI:** The workflow JSON MUST include a top-level `"links"` array alongside `"nodes"`. Without it, nodes display but have no visible connections in ComfyUI.

Each link is a 6-element tuple:
```
[link_id, from_node_id, from_slot_index, to_node_id, to_slot_index, "TYPE_STRING"]
```
- link_id starts at 1, sequential / link_id从1开始，顺序递增
- TYPE_STRING is: "MODEL" | "CLIP" | "VAE" | "LATENT" | "IMAGE" | "MASK" | "CONDITIONING"
- Node outputs must list their originating link_ids in `outputs[].links` arrays
- Top-level keys: `last_node_id`, `last_link_id`, `nodes`, `links`, `groups`, `config`, `version`

---

## Step 5 — Output Assembly / 输出组装

### Always produce 3 artifacts / 始终输出三件套:

**① Workflow file** (format depends on platform):
- ComfyUI → `workflow.json` (node graph) + `workflow_api.json` (API format)
- InvokeAI → `invokeai_workflow.json` (Node Editor format)
- A1111 → `params.json`
- Diffusers → `pipeline.py`
- API → `request.json` + `example.sh`
- Prompt-only → `prompt.txt`

**② `dependencies.md`** — list every required file + where to download it:
```markdown
## Models / 模型
- models/checkpoints/: <name>.safetensors  [Civitai / HuggingFace URL]
- models/loras/: <name>.safetensors        [Civitai / HuggingFace URL]
- models/controlnet/: <name>.pth/.safetensors

## Custom Nodes / 自定义节点 (ComfyUI only)
- Install via ComfyUI-Manager / 通过ComfyUI-Manager安装:
  - <repo-name>: <GitHub URL>
```

**③ Usage notes / 使用说明** (inline in response):
- How to load the file / 如何加载文件
- Key parameters to tune / 关键可调参数  
- Common errors + fixes / 常见报错及解决方法
- "Want me to add X?" follow-up suggestions / 后续扩展建议

---

## Cross-Platform Conversion / 跨平台转换

When user provides an existing workflow and asks to convert:
1. Parse the source format → extract IR fields
2. Validate IR (some fields may not map perfectly → note losses)
3. Render to target platform

**Common conversion losses / 常见转换损失:**
| From → To | Loss |
|---|---|
| ComfyUI → A1111 | Advanced node logic (masks, batch routes) |
| A1111 → ComfyUI | Embedded LoRA syntax `<lora:x:w>` must become LoraLoader nodes |
| Any → Prompt-only | All structural control lost; only content preserved |

---

## Capability Degradation / 能力降级

| Level | Environment | Behavior |
|---|---|---|
| L4 | File tools available | Write files to disk, present download links |
| L3 | Tool calls only | Output JSON in code blocks, offer to save |
| L2 | Long context (>32K) | Full multi-file output in one response |
| L1 | Basic LLM | Core workflow JSON only, split if needed |

---

## Execution Checklist / 执行检查清单

Before outputting, verify:
- [ ] IR constructed with no missing required fields
- [ ] All validator rules passed (or documented exceptions)
- [ ] Node IDs are unique and sequential (ComfyUI)
- [ ] Every node input has exactly one source connection (ComfyUI)
- [ ] LoRA nodes thread both MODEL and CLIP (ComfyUI)
- [ ] SaveImage or PreviewImage present as terminal node (ComfyUI)
- [ ] dependencies.md includes ALL models referenced in workflow
- [ ] Usage notes explain how to load the file on the target platform

---

## Automated Validation / 自动化验证

Run the test validator to check all test cases against their expected outputs:

```bash
python3 tests/validators/test_validation.py
```

The validator runs semantic checks (R01 Flux no negative, R06 VAEEncodeForInpaint, R15 Flux cfg=1)
and platform-specific validators (ComfyUI / A1111 / Diffusers / InvokeAI).

**Test coverage / 测试覆盖:**
| TC | Scenario / 场景 | Platform |
|----|----------------|----------|
| TC001 | SDXL + 2 LoRAs | ComfyUI |
| TC002 | Flux.1-dev + ControlNet | ComfyUI |
| TC003 | SD1.5 inpaint (R06) | ComfyUI |
| TC004 | SD1.5 + LoRA syntax | A1111 |
| TC005 | Flux schnell (R03) | A1111 |
| TC006 | SDXL pipeline.py | Diffusers |
| TC007 | SD3.5 Replicate API | API |
| TC008 | SDXL → Midjourney | Prompt-only |
| TC009 | AnimateDiff video | ComfyUI |
| TC010 | Stability AI API | API |
| TC011 | Multi-ControlNet chain | ComfyUI |
| TC012 | SDXL base + refiner | Diffusers |
| TC013 | SDXL txt2img | InvokeAI |
