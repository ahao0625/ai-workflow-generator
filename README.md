# AI Workflow Generator / AI 工作流生成器

> **EN:** Tell AI what you want, it generates ready-to-use image generation workflow files.
> **中:** 告诉 AI 你想要什么，它帮你生成完整可用的绘图工作流文件。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Platform: ComfyUI · A1111 · Diffusers · API](https://img.shields.io/badge/Platform-ComfyUI%20·%20A1111%20·%20Diffusers%20·%20API-blue.svg)]()

---

## 📥 Download / 下载方式

<table>
<tr>
<td width="50%">

**EN — Download**

> **Option 1 (Recommended):** Click [📦 Download ZIP](https://github.com/ahao0625/ai-workflow-generator/releases/download/v1.0.0/ai-workflow-generator-v1.0.0.zip)

> **Option 2 (Clone):**
> ```bash
> git clone https://github.com/ahao0625/ai-workflow-generator.git
> ```

> **Option 3 (GitHub):** Open the [repo](https://github.com/ahao0625/ai-workflow-generator) → **Code → Download ZIP**

</td>
<td width="50%">

**中 — 下载方式**

> **方式一（推荐）：** 点击 [📦 下载压缩包](https://github.com/ahao0625/ai-workflow-generator/releases/download/v1.0.0/ai-workflow-generator-v1.0.0.zip)，解压即用。

> **方式二（Git）：**
> ```bash
> git clone https://github.com/ahao0625/ai-workflow-generator.git
> ```

> **方式三（网页）：** 打开 [GitHub 仓库](https://github.com/ahao0625/ai-workflow-generator) → **Code → Download ZIP**

</td>
</tr>
</table>

---

## 🌟 What It Does / 它能做什么

<table>
<tr>
<td width="50%">

**EN — What It Does**

This is a **SKILL.md** — a spec you give to any LLM (Claude, GPT-4, Gemini, Kimi, DeepSeek...). The AI generates ready-to-use workflow files:

| Target | Output |
|--------|--------|
| **ComfyUI** | `workflow.json` |
| **A1111 / Forge** | `params.json` |
| **Diffusers** | `pipeline.py` |
| **Replicate / Stability** | `request.json` + `example.sh` |
| **Midjourney / DALL·E** | `/imagine prompt` |

**Example:**
> *"Generate a SDXL workflow with 2 LoRAs and ControlNet"*
> → `workflow.json` + `dependencies.md` + usage guide

</td>
<td width="50%">

**中 — 它能做什么**

这是一个"给 AI 读的说明书"（SKILL.md）。不管你用的是 Claude、ChatGPT、Kimi 还是 DeepSeek，它都能生成工作流文件：

| 目标平台 | 生成的文件 |
|---------|-----------|
| **ComfyUI** | `workflow.json` |
| **A1111 / Forge** | `params.json` |
| **Diffusers** | `pipeline.py` |
| **Replicate / Stability** | `request.json` + `example.sh` |
| **Midjourney / DALL·E** | `/imagine prompt` |

**举个例子：**
> "帮我生成一个 SDXL 工作流，加两个 LoRA，要 ControlNet"
> → `workflow.json` + `dependencies.md` + 使用说明

</td>
</tr>
</table>

**Supported models / 支持的模型：** SD 1.5 · SDXL · SDXL Turbo · Flux.1 · SD3 · SD3.5 · AnimateDiff · SVD · CogVideoX · Wan 2.1

---

## ⚙️ How It Works / 工作原理

<table>
<tr>
<td width="50%">

**EN — How It Works**

```
You: "Generate a Flux workflow with ControlNet"
     ↓
① AI detects platform → ComfyUI renderer
     ↓
② AI parses request → builds IR
   (model family, pipeline type, LoRAs...)
     ↓
③ AI validates with 20 built-in rules
   ⚠️ Flux has NO negative prompt → auto-removed
   ⚠️ Inpaint → VAEEncodeForInpaint enforced
     ↓
④ AI renders IR to native format
     ↓
⑤ Outputs 3 files:
   · Workflow file (ready to use)
   · dependencies.md (what to download)
   · Usage notes (how to load it)
```

</td>
<td width="50%">

**中 — 工作原理**

```
你说："帮我生成一个 Flux 工作流，加 ControlNet"
     ↓
① AI 识别平台 → 用 ComfyUI 渲染器
     ↓
② AI 解析需求，构建"中间表示"（IR）
   模型族？文生图还是局部重绘？有哪些 LoRA？
     ↓
③ AI 用 20 条规则验证需求
   ⚠️ Flux 不能加负向提示词 → 自动去掉
   ⚠️ Inpaint 必须用 VAEEncodeForInpaint → 自动修正
     ↓
④ AI 调用对应平台的渲染器，生成原生格式
     ↓
⑤ 输出三件套：
   · 工作流文件（可直接使用）
   · dependencies.md（需要下载什么模型）
   · 使用说明（怎么加载，遇到问题怎么办）
```

</td>
</tr>
</table>

---

## 🚀 Setup / 配置方式

<table>
<tr>
<td width="50%">

**EN — Pick One**

### ① Claude (Recommended ✅)

1. [claude.ai](https://claude.ai) → **Projects → Create Project**
2. Paste [`adapters/prompt/claude_system.md`](adapters/prompt/claude_system.md) into Project Instructions
3. Drag `knowledge/` folder into the project
4. Chat: *"Generate a SDXL workflow with 2 LoRAs"*

> 💡 Claude has 200K context — full knowledge base fits easily.

### ② ChatGPT (GPTs)

1. [chat.openai.com](https://chat.openai.com) → **Create a GPT**
2. **Instructions**: paste [`adapters/prompt/chatgpt_instructions.md`](adapters/prompt/chatgpt_instructions.md)
3. **Knowledge**: upload `knowledge/` folder
4. Enable **Code Interpreter** + **Web Browsing**

### ③ Kimi / Qwen / Gemini / DeepSeek (Free)

1. Paste [`adapters/prompt/universal_system.md`](adapters/prompt/universal_system.md) into System Prompt
2. Upload `knowledge/` folder
3. Start chatting

### ④ Local (Ollama / LM Studio / Jan)

1. Set `SKILL.md` as System Prompt
2. Upload `knowledge/` folder
3. Chat

> ⚠️ Recommend 70B+ models (Qwen2.5-72B, Llama3.1-70B)

</td>
<td width="50%">

**中 — 总有一种适合你**

### ① Claude（最推荐 ✅）

1. [claude.ai](https://claude.ai) → **Projects → Create Project**
2. 把 [`adapters/prompt/claude_system.md`](adapters/prompt/claude_system.md) 粘贴到 Project Instructions
3. 把 `knowledge/` 文件夹拖进去
4. 开聊："生成一个 SDXL 工作流，加两个 LoRA"

> 💡 Claude 有 200K context，全部知识库都能装进去。

### ② ChatGPT（GPTs）

1. [chat.openai.com](https://chat.openai.com) → **Create a GPT**
2. **Instructions**：粘贴 [`adapters/prompt/chatgpt_instructions.md`](adapters/prompt/chatgpt_instructions.md)
3. **Knowledge**：上传 `knowledge/` 文件夹
4. 开启 **Code Interpreter** + **Web Browsing**

### ③ Kimi / 通义千问 / 文心一言（免费）

1. 把 [`adapters/prompt/universal_system.md`](adapters/prompt/universal_system.md) 粘贴到 System Prompt
2. 上传 `knowledge/` 文件夹
3. 开始用

### ④ 本地部署（Ollama / LM Studio / Jan）

1. 把 `SKILL.md` 作为 System Prompt
2. 上传 `knowledge/` 文件夹
3. 对话即可

> ⚠️ 建议 70B 以上模型（如 Qwen2.5-72B）

</td>
</tr>
</table>

<table>
<tr>
<td width="50%">

### ⑤ LangChain (Developers)

```python
from langchain.tools import BaseTool

tool = WorkflowGeneratorTool(
    skill_content=open("SKILL.md").read()
)

agent = initialize_agent([tool], llm)
agent.run("Generate SDXL workflow with 2 LoRAs")
```

### ⑥ Dify (Low-Code)

1. Dify → **Tools → Custom Tools → Import**
2. Upload [`adapters/dify/tool_manifest.yaml`](adapters/dify/tool_manifest.yaml)
3. Drag "AI Workflow Generator" into your workflow

### ⑦ Coze / 扣子

1. Coze → **Plugins → Create Plugin**
2. Import [`adapters/coze/plugin_manifest.json`](adapters/coze/plugin_manifest.json)
3. Use "Generate Workflow" node

</td>
<td width="50%">

### ⑤ LangChain（开发者）

```python
from langchain.tools import BaseTool

tool = WorkflowGeneratorTool(
    skill_content=open("SKILL.md").read()
)

agent = initialize_agent([tool], llm)
agent.run("生成一个 SDXL 工作流，加两个 LoRA")
```

### ⑥ Dify（低代码平台）

1. Dify → **工具 → 自定义工具 → 导入**
2. 上传 [`adapters/dify/tool_manifest.yaml`](adapters/dify/tool_manifest.yaml)
3. 在 Workflow 里拖入"AI 工作流生成器"节点

### ⑦ Coze / 扣子

1. Coze → **插件 → 创建插件**
2. 导入 [`adapters/coze/plugin_manifest.json`](adapters/coze/plugin_manifest.json)
3. 使用"生成工作流"节点

</td>
</tr>
</table>

---

## 📂 Knowledge Base / 知识库结构

<table>
<tr>
<td width="50%">

**EN — Structure**

```
knowledge/
├── ir_schema.yaml       ← Universal workflow language
├── rules.yaml            ← 20 validation rules
├── models/            ← Model specs
│   ├── sd15.yaml     ← 512px, 20 steps
│   ├── sdxl.yaml     ← 1024px, dual CLIP
│   ├── flux.yaml     ← No neg prompt
│   ├── sd3.yaml     ← Triple CLIP, MM-DiT
│   └── video.yaml     ← AnimateDiff/SVD/CogVideoX
├── nodes/             ← ComfyUI nodes
│   ├── native_nodes.yaml  ← 80+ built-in
│   └── custom_nodes.yaml  ← IPAdapter/InstantID/LayerDiffuse
└── platforms/         ← Platform renderers
    ├── comfyui.yaml       ← Node graph JSON
    ├── a1111.yaml        ← params.txt
    ├── diffusers.yaml    ← pipeline.py
    ├── api.yaml         ← Replicate/Stability
    └── prompt_only.yaml ← Midjourney
```

</td>
<td width="50%">

**中 — 结构**

```
knowledge/
├── ir_schema.yaml       ← 理解工作流的通用语言
├── rules.yaml            ← 20条验证规则
├── models/            ← 各模型族的规范
│   ├── sd15.yaml     ← 512px，20步
│   ├── sdxl.yaml     ← 1024px，双CLIP
│   ├── flux.yaml     ← 无负向提示
│   ├── sd3.yaml     ← 三路CLIP，MM-DiT
│   └── video.yaml     ← AnimateDiff/SVD/CogVideoX
├── nodes/             ← ComfyUI 节点百科
│   ├── native_nodes.yaml  ← 80+ 内置节点
│   └── custom_nodes.yaml  ← IPAdapter/InstantID/LayerDiffuse
└── platforms/         ← 平台渲染器
    ├── comfyui.yaml       ← 节点图 JSON
    ├── a1111.yaml        ← params.txt
    ├── diffusers.yaml    ← pipeline.py
    ├── api.yaml         ← Replicate/Stability
    └── prompt_only.yaml ← Midjourney
```

</td>
</tr>
</table>

---

## ✅ Test Coverage / 测试覆盖

<table>
<tr>
<td width="50%">

**EN — 12 Test Cases**

| Case | Platform | Tests |
|------|---------|-------|
| TC001 | ComfyUI | SDXL + 2 LoRAs, MODEL+CLIP dual chain |
| TC002 | ComfyUI | Flux + ControlNet, auto-remove neg prompt |
| TC003 | ComfyUI | Inpaint enforces VAEEncodeForInpaint |
| TC004 | A1111 | LoRA as `<lora:name:weight>` |
| TC005 | A1111 Forge | Flux schnell steps ≤ 8 |
| TC006 | Diffusers | SDXL pipeline.py completeness |
| TC007 | Replicate | SD3 API request format |
| TC008 | Midjourney | Cross-platform SDXL → prompt |
| TC009 | ComfyUI | AnimateDiff video workflow |
| TC010 | Stability | SD3 Ultra API request |
| TC011 | ComfyUI | Multiple ControlNets chained |
| TC012 | Diffusers | SDXL Base + Refiner two-stage |

</td>
<td width="50%">

**中 — 12 个测试用例**

| 用例 | 平台 | 验证什么 |
|------|------|---------|
| TC001 | ComfyUI | SDXL + 2 LoRA，MODEL+CLIP 双线 |
| TC002 | ComfyUI | Flux + ControlNet，负向提示词自动去除 |
| TC003 | ComfyUI | Inpaint 强制 VAEEncodeForInpaint |
| TC004 | A1111 | LoRA 嵌入语法 `<lora:name:weight>` |
| TC005 | A1111 Forge | Flux schnell 步数 ≤ 8 |
| TC006 | Diffusers | SDXL pipeline.py 完整性 |
| TC007 | Replicate | SD3 API 请求格式 |
| TC008 | Midjourney | SDXL → 自然语言提示词 |
| TC009 | ComfyUI | AnimateDiff 视频工作流 |
| TC010 | Stability | SD3 Ultra API 请求 |
| TC011 | ComfyUI | 多 ControlNet 链式串联 |
| TC012 | Diffusers | SDXL Base + Refiner 两阶段 |

</td>
</tr>
</table>

---

## ❓ FAQ / 常见问题

<table>
<tr>
<td width="50%">

**EN — FAQ**

**Q: I don't know which platform.**
A: Tell AI what tool you use. "ComfyUI" → workflow.json. "Replicate API" → API request.

**Q: The file doesn't run.**
A: Check dependencies.md — are all models downloaded with correct paths?

**Q: "Flux doesn't support negative prompt"**
A: The AI guard removed it. Flux architecture doesn't use this parameter.

**Q: Can I add a 3rd LoRA?**
A: Yes. Chain more LoraLoader nodes after existing ones.

**Q: Can it generate videos?**
A: Yes — AnimateDiff, SVD, CogVideoX, Wan 2.1.

</td>
<td width="50%">

**中 — 常见问题**

**Q: 我不知道该用哪个平台。**
A: 告诉 AI 你用什么工具，它会帮你选。

**Q: 生成的文件跑不起来。**
A: 检查 dependencies.md，确认模型文件都下载了且路径正确。

**Q: 报错 "Flux 不支持 negative prompt"。**
A: AI 在验证阶段发现并自动去掉了。Flux 架构本身不支持这个参数。

**Q: 能加第 3 个 LoRA 吗？**
A: 可以，在 LoRALoader 后继续串联更多节点。

**Q: 能生成视频吗？**
A: 能，支持 AnimateDiff、SVD、CogVideoX、Wan 2.1。

</td>
</tr>
</table>

---

## ☕ Support / 支持一杯咖啡

<table>
<tr>
<td width="50%">

If this project helps you, your support keeps it alive!

| WeChat | Alipay |
|:------:|:------:|
| <img src="assets/wechat-qr.png" width="200" alt="WeChat QR"/> | <img src="assets/alipay-qr.png" width="200" alt="Alipay QR"/> |

Every bit of support motivates me to keep updating 🌟

</td>
<td width="50%">

如果你觉得这个项目对你有帮助，欢迎打赏支持！

| 微信 | 支付宝 |
|:----:|:------:|
| <img src="assets/wechat-qr.png" width="200" alt="微信收款码"/> | <img src="assets/alipay-qr.png" width="200" alt="支付宝收款码"/> |

每一份支持都是我继续维护和更新的动力 🌟

</td>
</tr>
</table>

---

## 📄 License

MIT License — free to use, modify, commercial use welcome.
