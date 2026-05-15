# AI Workflow Generator

> Tell AI what you want, it generates ready-to-use image generation workflow files.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Platform: ComfyUI · A1111 · Diffusers · API](https://img.shields.io/badge/Platform-ComfyUI%20·%20A1111%20·%20Diffusers%20·%20API-blue.svg)]()

---

## 📥 Download

> **Option 1 (Recommended, no Git needed):** Click [📦 Download ZIP](https://github.com/ahao0625/ai-workflow-generator/releases/download/v1.0.0/ai-workflow-generator-v1.0.0.zip), unzip and go.

> **Option 2 (Clone with Git):**
> ```bash
> git clone https://github.com/ahao0625/ai-workflow-generator.git
> ```

> **Option 3 (From GitHub):** Open the [repo](https://github.com/ahao0625/ai-workflow-generator), click **Code → Download ZIP**.

---

## What It Does

This is a **SKILL.md** — a specification that you give to any LLM (Claude, GPT-4, Gemini, Kimi, DeepSeek, etc.). Once loaded, the AI can generate ready-to-use workflow files for:

| Target Platform | Output |
|----------------|--------|
| **ComfyUI** (node-based) | `workflow.json` — drag into ComfyUI, hit run |
| **A1111 / Forge** (web UI) | `params.json` — paste into WebUI |
| **HuggingFace Diffusers** (Python) | `pipeline.py` — run with `python pipeline.py` |
| **Replicate / Stability AI** (cloud API) | `request.json` + `example.sh` — curl to generate |
| **Midjourney / DALL·E / Ideogram** (prompt-only) | Optimized English prompt + params |

**Supported models:** SD 1.5 · SDXL · SDXL Turbo · Flux.1 · SD3 · SD3.5 · AnimateDiff · SVD · CogVideoX · Wan 2.1

**Example:**
> "Generate a SDXL txt2img workflow with 2 LoRAs and ControlNet depth"

→ Outputs: `workflow.json` + `dependencies.md` + usage guide

---

## How It Works

```
You: "Generate a Flux workflow with ControlNet"
     │
     ▼
① AI detects platform → you said ComfyUI → ComfyUI renderer
     │
     ▼
② AI parses your request into an Internal Representation (IR)
   Model family? txt2img or inpaint? LoRAs? ControlNets?
     │
     ▼
③ AI validates against 20 built-in rules
   ⚠️ Flux has no negative prompt → auto-removed
   ⚠️ Inpaint must use VAEEncodeForInpaint → auto-fixed
     │
     ▼
④ AI renders IR to native platform format
     │
     ▼
⑤ Outputs 3 files:
   · Workflow file (ready to use)
   · dependencies.md (what models to download)
   · Usage notes (how to load, troubleshoot)
```

---

## Setup (Pick One)

### Method 1: Claude (Recommended ✅)

1. Go to [claude.ai](https://claude.ai) → **Projects → Create Project**
2. Name it (e.g. "AI Workflow Helper")
3. Paste [`adapters/prompt/claude_system.md`](adapters/prompt/claude_system.md) into Project Instructions
4. Drag the entire `knowledge/` folder into the project
5. Start chatting: *"Generate a SDXL workflow with 2 LoRAs"*

> 💡 Claude has 200K context — it handles the full knowledge base without issues.

---

### Method 2: ChatGPT (GPTs)

1. Go to [chat.openai.com](https://chat.openai.com) → **Create a GPT**
2. **Instructions**: paste [`adapters/prompt/chatgpt_instructions.md`](adapters/prompt/chatgpt_instructions.md)
3. **Knowledge**: upload the entire `knowledge/` folder
4. **Capabilities**: enable **Code Interpreter** + **Web Browsing**
5. Save with a name, start using it

---

### Method 3: Kimi / Qwen / Gemini / DeepSeek (Free)

These support file upload + System Prompt:

1. Create an assistant / agent on the platform
2. Paste [`adapters/prompt/universal_system.md`](adapters/prompt/universal_system.md) into System Prompt
3. Upload the `knowledge/` folder
4. Start using it

---

### Method 4: Local Models (Ollama / LM Studio / Jan)

Works with local models too, just slightly slower:

1. Set `SKILL.md` content as System Prompt
2. Upload `knowledge/` folder
3. Chat

> ⚠️ Recommend 70B+ models (Qwen2.5-72B, Llama3.1-70B) for best results.

---

### Method 5: LangChain (Developers)

```python
from langchain.tools import BaseTool

tool = WorkflowGeneratorTool(
    skill_content=open("SKILL.md").read()
)

agent = initialize_agent([tool], llm, agent="react-docstore")
agent.run("Generate a SDXL workflow with 2 LoRAs")
```

---

### Method 6: Dify (Low-Code AI Platform)

1. Dify → **Tools → Custom Tools → Import**
2. Upload [`adapters/dify/tool_manifest.yaml`](adapters/dify/tool_manifest.yaml)
3. Drag "AI Workflow Generator" node into your workflow

---

### Method 7: Coze (Bot Platform)

1. Coze → **Plugins → Create Plugin**
2. Import [`adapters/coze/plugin_manifest.json`](adapters/coze/plugin_manifest.json)
3. Use "Generate Workflow" node in your bot workflow

---

### Method 8: Open WebUI (Local UI for Ollama)

1. Copy [`adapters/open_webui/skill_function.py`](adapters/open_webui/skill_function.py) to `~/.open-webui/tools/`
2. Enable in **Admin → Tools**
3. AI auto-calls the tool when you mention workflows

---

### Method 9: Semantic Kernel (.NET)

```csharp
var kernel = Kernel.CreateBuilder()
    .AddOpenAIChatCompletion(model, apiKey)
    .AddPlugin<WorkflowPlugin>("WorkflowGenerator");

var result = await kernel.InvokeAsync(
    "WorkflowGenerator_GenWorkflow",
    new() { ["description"] = "Generate SDXL workflow with 2 LoRAs" }
);
```

---

### Method 10: Zapier / Make (Automation)

Connect to your automation stack:
1. Trigger on incoming text
2. Call AI to generate workflow
3. Send result to email / Slack / Notion

---

## Demo

**Input:**
> "Generate a SDXL txt2img workflow with 2 LoRAs: add_detail weight 0.8, epiNoiseoffset weight 0.6. Prompt: a beautiful landscape"

**Output (3 files):**

① **workflow.json** — drag into ComfyUI, 9 nodes, MODEL+CLIP dual chain auto-routed

② **dependencies.md** — model files to download:
- juggernautXL_v9.safetensors → [Civitai link]
- add_detail.safetensors → [Civitai link]
- epiNoiseoffset_v2.safetensors → [Civitai link]

③ **Usage guide** — "Put files in ComfyUI/models/checkpoints/ and loras/, then click Queue"

---

## Knowledge Base Structure

```
knowledge/
├── ir_schema.yaml              ← Universal language for describing workflows
├── rules.yaml                   ← 20 rules (auto-corrects wrong configs)
├── models/                    ← Each model's quirks
│   ├── sd15.yaml              ← 512px, 20 steps, dpmpp_2m
│   ├── sdxl.yaml              ← 1024px, dual CLIP, refiner support
│   ├── flux.yaml              ← No negative prompt, FluxGuidance
│   ├── sd3.yaml              ← Triple CLIP, MM-DiT
│   └── video.yaml             ← AnimateDiff / SVD / Wan 2.1
├── nodes/                     ← ComfyUI node encyclopedia
│   ├── native_nodes.yaml       ← 80+ built-in nodes
│   └── custom_nodes.yaml       ← IPAdapter / InstantID / LayerDiffuse
└── platforms/                 ← Platform-specific translators
    ├── comfyui.yaml            ← Node IDs, connection rules, layout coords
    ├── a1111.yaml             ← params.txt format, LoRA syntax
    ├── diffusers.yaml         ← pipeline.py templates
    ├── api.yaml              ← Replicate / Stability API schema
    └── prompt_only.yaml       ← Midjourney param engine
```

---

## Test Coverage

12 test cases validated:

| Case | Platform | What It Tests |
|------|---------|---------------|
| TC001 | ComfyUI | SDXL + 2 LoRAs, correct MODEL+CLIP dual chain |
| TC002 | ComfyUI | Flux + ControlNet, auto-remove negative prompt |
| TC003 | ComfyUI | Inpaint enforces VAEEncodeForInpaint (R06) |
| TC004 | A1111 | LoRA embedded as `<lora:name:weight>` |
| TC005 | A1111 Forge | Flux schnell step ≤ 8 (R03) |
| TC006 | Diffusers | SDXL pipeline.py completeness |
| TC007 | Replicate | SD3 API request format |
| TC008 | Midjourney | Cross-platform SDXL → natural language prompt |
| TC009 | ComfyUI | AnimateDiff video workflow node chain |
| TC010 | Stability | SD3 Ultra API request |
| TC011 | ComfyUI | Multiple ControlNets chained (not parallel) |
| TC012 | Diffusers | SDXL Base + Refiner two-stage |

---

## FAQ

**Q: I don't know which platform to use.**
A: Tell AI what tool you use. "I use ComfyUI" → ComfyUI workflow. "I call Replicate API" → API request.

**Q: The generated file doesn't run.**
A: Check dependencies.md — are all model files downloaded and paths correct? Common issues: missing custom nodes, VAE not loaded, LoRA path wrong.

**Q: It says "Flux doesn't support negative prompt"**
A: That's the safety guard. AI detected a negative prompt in a Flux workflow and removed it automatically. Flux's architecture doesn't support this parameter.

**Q: Can I add a 3rd LoRA?**
A: Yes. Chain more LoraLoader nodes after the existing ones. Each LoRA = one node. Order affects final output.

**Q: Can it generate videos?**
A: Yes. Supports AnimateDiff (SD1.5/SDXL animation), SVD (image→video), CogVideoX, Wan 2.1. Tell AI which model you want.

---

## ☕ Support

If this project helps you, your support keeps it alive!

| WeChat | Alipay |
|:------:|:------:|
| <img src="assets/wechat-qr.png" width="200" alt="WeChat QR Code"/> | <img src="assets/alipay-qr.png" width="200" alt="Alipay QR Code"/> |

Every bit of support motivates me to keep updating and maintaining 🌟

---

## License

MIT License — free to use, modify, commercial use welcome.
