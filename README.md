# AI 工作流生成器

> 告诉 AI 你想要什么，它帮你生成完整可用的绘图工作流文件。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Platform: ComfyUI · A1111 · Diffusers · API](https://img.shields.io/badge/Platform-ComfyUI%20·%20A1111%20·%20Diffusers%20·%20API-blue.svg)]()

---

## 一句话介绍

这是一个"给 AI 读的说明书"（SKILL.md）。不管你用的是 Claude、ChatGPT、Kimi 还是 DeepSeek，只要把这份说明书扔给它，它就能根据你的需求，生成 ComfyUI 节点图、A1111 参数、Diffusers 脚本、API 请求或 Midjourney 提示词。

**你只需要说人话，比如：**
> "帮我生成一个 SDXL 工作流，加两个 LoRA，要 ControlNet depth"

它就帮你把文件生成好。

---

## 支持哪些平台

| 你想用在 | 会生成这样的文件 |
|---------|----------------|
| **ComfyUI**（节点式工作流） | `workflow.json`，拖进 ComfyUI 直接跑 |
| **A1111 / Forge**（网页界面） | `params.txt`，复制到 WebUI 用 |
| **HuggingFace Diffusers**（Python 脚本） | `pipeline.py`，`python pipeline.py` 直接出图 |
| **Replicate / Stability AI**（云端 API） | `request.json` + `example.sh`，curl 命令调 API |
| **Midjourney / DALL·E / Ideogram**（纯提示词） | 优化好的英文提示词 + 参数说明 |

支持的模型：SD 1.5 · SDXL · SDXL Turbo · Flux.1 · SD3 · SD3.5 · AnimateDiff · SVD · CogVideoX · Wan 2.1

---

## 工作原理

```
你："帮我生成一个 Flux 工作流，加 ControlNet"
     │
     ▼
① AI 识别平台  → 你说 ComfyUI → 用 ComfyUI 渲染器
     │
     ▼
② AI 解析你的需求，构建"中间表示"（IR）
   模型族？文生图还是局部重绘？有哪些 LoRA？
     │
     ▼
③ AI 用 20 条规则验证需求
   ⚠️ Flux 不能加负向提示词 → 自动去掉
   ⚠️ Inpaint 必须用 VAEEncodeForInpaint → 自动修正
     │
     ▼
④ AI 调用对应平台的渲染器，生成原生格式文件
     │
     ▼
⑤ 输出三件套：
   · 工作流文件（可直接使用）
   · dependencies.md（需要下载什么模型）
   · 使用说明（怎么加载，遇到问题怎么办）
```

---

## 配置方式（总有一种适合你）

### 方式一：Claude（最推荐 ✅）

适合日常随手用，不折腾。

**步骤：**

1. 打开 [claude.ai](https://claude.ai)，登录
2. 点击左下角 **Projects → Create Project**，起名"AI绘图助手"
3. 在 Project Instructions 里粘贴 [`adapters/prompt/claude_system.md`](adapters/prompt/claude_system.md) 的内容
4. 把整个 `knowledge/` 文件夹**拖进去**（或上传）
5. 开聊，比如："生成一个 SDXL 文生图工作流"

> 💡 Claude 有 200K context，模型族知识和节点库全部装进去都没问题。

---

### 方式二：ChatGPT（适合有 ChatGPT Plus 的人）

**步骤：**

1. 打开 [chat.openai.com](https://chat.openai.com)，点 **Create a GPT**
2. **Instructions** 标签：粘贴 [`adapters/prompt/chatgpt_instructions.md`](adapters/prompt/chatgpt_instructions.md) 内容
3. **Knowledge** 标签：上传整个 `knowledge/` 文件夹
4. **Capabilities** 标签：勾选 **Code Interpreter**（让它帮你写文件）和 **Web Browsing**（查最新模型信息）
5. 起个名字，比如"AI绘图工作流助手"，保存

> 💡 Code Interpreter 开启后，它会直接把生成的文件写到可下载状态，不用你手动复制粘贴。

---

### 方式三：Kimi / 秘塔搜索 / 通义千问 / 文心一言（免费党）

这些平台支持**上传文件 + System Prompt**，配置最简单：

1. 在对应平台创建一个"助手"或"智能体"
2. 把 [`adapters/prompt/universal_system.md`](adapters/prompt/universal_system.md) 的内容粘贴进去
3. 上传 `knowledge/` 文件夹
4. 开始用

> 💡 通义、秘塔、Kimi 都支持长上下文，Diffusers 的 pipeline.py 模板（几百行）都能完整塞进去。

---

### 方式四：本地部署（Ollama / LM Studio / Jan）

本地模型也能用，只是输出速度会稍慢：

1. 把 `SKILL.md` 内容作为 System Prompt 传入
2. 上传 `knowledge/` 文件夹
3. 对话即可

> ⚠️ 本地模型建议用 70B 以上参数量的模型（如 Qwen2.5-72B、Llama3.1-70B），小模型对多知识文件的理解能力有限。

---

### 方式五：LangChain（开发者集成）

把技能封装成 LangChain Tool，在自己的 AI 应用里调用：

```python
# adapters/langchain/workflow_generator_tool.py
from langchain.tools import BaseTool

tool = WorkflowGeneratorTool(
    skill_content=open("SKILL.md").read()
)

# 在 Agent 里使用
agent = initialize_agent([tool], llm, agent="react-docstore")
agent.run("生成一个 SDXL 工作流，加两个 LoRA")
```

---

### 方式六：Dify（低代码 AI 应用平台）

在 Dify 里直接导入为自定义工具：

1. Dify → **工具 → 自定义工具 → 导入**
2. 上传 [`adapters/dify/tool_manifest.yaml`](adapters/dify/tool_manifest.yaml)
3. 在 Workflow 里拖入"AI 工作流生成器"节点，输入自然语言描述
4. 输出直接拿到 workflow JSON / Python 代码

---

### 方式七：Coze / 扣子（国内 bot 平台）

在 Coze 里发布为插件：

1. Coze → **插件 → 创建插件**
2. 导入 [`adapters/coze/plugin_manifest.json`](adapters/coze/plugin_manifest.json)
3. 在 Bot 工作流里使用"生成工作流"节点

---

### 方式八：Open WebUI（本地 Web UI for Ollama）

Open WebUI 支持自定义 Tools：

1. 把 [`adapters/open_webui/skill_function.py`](adapters/open_webui/skill_function.py) 放到 `~/.open-webui/tools/`
2. 在 Admin → Tools 里启用
3. 对话中提到工作流时，AI 会自动调用这个工具

---

### 方式九：微软 Semantic Kernel（.NET 生态）

在 .NET 项目里注册为 SK Plugin：

```csharp
// adapters/semantic_kernel/WorkflowPlugin.cs
var kernel = Kernel.CreateBuilder()
    .AddOpenAIChatCompletion(model, apiKey)
    .AddPlugin<WorkflowPlugin>("WorkflowGenerator");

var result = await kernel.InvokeAsync(
    "WorkflowGenerator_GenWorkflow",
    new() { ["description"] = "生成 SDXL 工作流，加两个 LoRA" }
);
```

---

### 方式十：Zapier / Make（自动化工作流）

配合 AI Actions，把工作流生成接进自动化流程：

1. 在 Zapier Create（MCP 或 AI Actions）里配置
2. 触发条件：收到特定格式的文本
3. 动作：调用 AI 生成工作流 → 发送邮件 / Slack / 保存到 Notion

---

## 效果演示

**输入：**
> "帮我生成一个 SDXL 文生图工作流，加两个 LoRA：add_detail 权重0.8，epiNoiseoffset 权重0.6。提示词：a beautiful landscape"

**输出（三件套）：**

① **workflow.json** — 拖入 ComfyUI 即可，9个节点，自动串联 MODEL+CLIP 双链路

② **dependencies.md** — 列出所需文件：
- juggernautXL_v9.safetensors → [Civitai 下载链接]
- add_detail.safetensors → [Civitai 下载链接]
- epiNoiseoffset_v2.safetensors → [Civitai 下载链接]

③ **使用说明** — "把这个文件放进 ComfyUI/models/checkpoints/，LoRA 放进 loras/，然后点击队列"

---

## 知识库结构

```
knowledge/
├── ir_schema.yaml              ← AI 理解"工作流"的通用语言
├── rules.yaml                   ← 20条规则（自动修正错误配置）
├── models/                    ← 各模型族的脾气
│   ├── sd15.yaml              ← 512px，20步，dpmpp_2m
│   ├── sdxl.yaml              ← 1024px，双CLIP，refiner追加
│   ├── flux.yaml              ← 无负向提示，FluxGuidance引导
│   ├── sd3.yaml               ← 三路CLIP，MM-DiT
│   └── video.yaml             ← AnimateDiff / SVD / Wan 2.1
├── nodes/                     ← ComfyUI 节点百科
│   ├── native_nodes.yaml       ← 80+ 内置节点
│   └── custom_nodes.yaml       ← IPAdapter / InstantID / LayerDiffuse
└── platforms/                 ← 各平台翻译字典
    ├── comfyui.yaml            ← 节点ID、连线规则、布局坐标
    ├── a1111.yaml             ← params.txt 格式、LoRA语法
    ├── diffusers.yaml         ← pipeline.py 模板
    ├── api.yaml              ← Replicate / Stability API schema
    └── prompt_only.yaml       ← Midjourney 参数引擎
```

---

## 测试覆盖

已通过 12 个标准测试用例验证：

| 用例 | 验证什么 |
|------|---------|
| TC001 | SDXL + 2 LoRA 链路正确（MODEL+CLIP 双线） |
| TC002 | Flux + ControlNet，负向提示词自动去除 |
| TC003 | Inpaint 强制 VAEEncodeForInpaint（R06） |
| TC004 | A1111 LoRA 嵌入语法 `<lora:name:weight>` |
| TC005 | Flux schnell 步数 ≤8（R03） |
| TC006 | Diffusers pipeline.py 完整性 |
| TC007 | Replicate API 请求格式 |
| TC008 | SDXL → Midjourney 提示词跨平台转换 |
| TC009 | AnimateDiff 视频工作流节点链 |
| TC010 | Stability AI API 请求 |
| TC011 | 多 ControlNet 链式串联（非并联） |
| TC012 | SDXL Base + Refiner 两阶段 Diffusers |

---

## 常见问题

**Q: 我不知道该用哪个平台，怎么办？**
A: 告诉 AI 你用什么工具，它会帮你选。如果你说"我用 ComfyUI"，它就生成 ComfyUI 的；说"我调用 Replicate API"，它就生成 API 请求。

**Q: 生成的文件跑不起来怎么办？**
A: 看输出的 dependencies.md，检查模型文件是否都下载了且路径正确。常见问题：缺少自定义节点（如 IPAdapter）、VAE 没加载、LoRA 路径写错了。

**Q: 报错 "Flux 不支持 negative prompt"？**
A: 这是正常的安全拦截。AI 在验证阶段发现 Flux 工作流里有负向提示词，直接帮你去掉了。Flux 模型的架构本身不支持这个参数，加了也没效果。

**Q: 我想加第3个 LoRA，可以吗？**
A: 可以。在 LoRALoader 后面继续串联更多 LoraLoader 节点即可。每个 LoRA 占一个节点，顺序会影响最终效果。

**Q: 能生成视频吗？**
A: 能。支持 AnimateDiff（SD1.5/SDXL 动画化）、SVD（图生视频）、CogVideoX、Wan 2.1。告诉 AI 你想用什么模型，它生成对应的工作流。

---

## ☕ 支持一杯咖啡

如果你觉得这个项目对你有帮助，欢迎打赏支持！

| 微信 | 支付宝 |
|:----:|:------:|
| <img src="assets/wechat-qr.png" width="200" alt="微信收款码"/> | <img src="assets/alipay-qr.png" width="200" alt="支付宝收款码"/> |

每一份支持都是我继续维护和更新的动力 🌟

---

## License

MIT License — 免费商用，欢迎 fork 和 PR。
