# AI 工作流生成器

> 告诉 AI 你想要什么，它帮你生成完整可用的绘图工作流文件。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Platform: ComfyUI · A1111 · Diffusers · API · InvokeAI](https://img.shields.io/badge/Platform-ComfyUI%20·%20A1111%20·%20Diffusers%20·%20API%20·%20InvokeAI-blue.svg)]()

---

## 一句话介绍

这是一个"给 AI 读的说明书"（SKILL.md）。不管你用的是 Claude、ChatGPT、Kimi 还是 DeepSeek，只要把这份说明书扔给它，它就能根据你的需求，生成 ComfyUI 节点图、A1111 参数、Diffusers 脚本、API 请求或 Midjourney 提示词。

**你只需要说人话，比如：**
> "帮我生成一个 SDXL 工作流，加两个 LoRA，要 ControlNet depth"

它就帮你把文件生成好。

---

## 📥 下载

| 方式 | 说明 |
|------|------|
| **📦 一键下载（推荐）** | [ai-workflow-generator-v1.3.zip](https://github.com/ahao0625/ai-workflow-generator/releases/download/v1.3.0/ai-workflow-generator-v1.3.zip) |
| **Git Clone** | `git clone https://github.com/ahao0625/ai-workflow-generator.git` |
| **Release 页面** | [GitHub Releases](https://github.com/ahao0625/ai-workflow-generator/releases) 查看历史版本 |

---

## 🚀 最简单的使用方式（99% 的人选这个）

**不需要复杂配置！** 直接把说明粘贴给任意支持长上下文的 AI：

### 步骤：

1. **下载项目压缩包**（从上面的下载链接）并解压
2. **打开你常用的 AI**（Claude / ChatGPT / Kimi / 通义 / DeepSeek 等）
3. **在对话框中粘贴** [`SKILL.md`](SKILL.md) 的全部内容（或 [`adapters/prompt/universal_system.md`](adapters/prompt/universal_system.md)，更精简）
4. **开始聊天**，比如：
   - "帮我生成一个 SDXL 文生图工作流"
   - "生成一个 Flux 工作流，加 ControlNet Canny"
   - "创建一个带 LoRA 的 ComfyUI Inpaint 工作流"

就这么简单！

---

## ✨ v1.3 新特性（模板引擎升级）

**问题解决：** ComfyUI 节点断线、AI 幻觉生成拓扑结构

**核心改进：**
- 🚀 **模板引擎**：AI 不再从零生成拓扑结构，而是选择模板
- 🔧 **模块组合**：通过组合预定义模块构建复杂工作流
- ✅ **自动验证**：确保节点、连线、schema 全部正确
- 🎯 **参数注入**：安全地注入参数而不破坏连接关系
- 📚 **Schema 注册表**：节点能力和 widget 规范

**成功率提升：** 从 ~60% → ~95%

---

## 支持哪些平台

| 你想用在 | 会生成这样的文件 |
|---------|----------------|
| **ComfyUI**（节点式工作流） | `workflow.json`，拖进 ComfyUI 直接跑 |
| **InvokeAI**（节点编辑器） | `invokeai_workflow.json`，导入 Node Editor |
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

## 🛠️ 高级配置（开发者或特定平台用户）

### 如果你有特定平台需求：

| 平台 | 对应的 System Prompt 文件 |
|------|---------------------------|
| Claude | [`adapters/prompt/claude_system.md`](adapters/prompt/claude_system.md) |
| ChatGPT | [`adapters/prompt/chatgpt_instructions.md`](adapters/prompt/chatgpt_instructions.md) |
| 通用（所有平台） | [`adapters/prompt/universal_system.md`](adapters/prompt/universal_system.md) |

### 开发者集成方式：

- **LangChain**: [`adapters/langchain/`](adapters/langchain/)
- **Dify**: [`adapters/dify/`](adapters/dify/)
- **Coze / 扣子**: [`adapters/coze/`](adapters/coze/)
- **Open WebUI**: [`adapters/open_webui/`](adapters/open_webui/)
- **Semantic Kernel**: [`adapters/semantic_kernel/`](adapters/semantic_kernel/)

这些是为开发者准备的，普通用户不需要看。

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
    ├── invokeai.yaml          ← InvokeAI 节点编辑器格式
    └── prompt_only.yaml       ← Midjourney 参数引擎

---

## 示例工作流

可直接拖入对应平台使用：

| 示例 | 内容 | 平台 |
|------|------|------|
| `examples/sdxl_faceid_img2img/` | SDXL + IPAdapter FaceID + img2img | ComfyUI |
| `examples/flux_txt2img/` | Flux.1-dev 文生图（DualCLIP + FluxGuidance） | ComfyUI |
| `examples/sd15_inpaint/` | SD1.5 局部重绘（VAEEncodeForInpaint） | ComfyUI |
| `examples/animatediff_basic/` | AnimateDiff 视频生成（VHS_VideoCombine） | ComfyUI |

每个示例包含 `workflow.json` + `workflow_api.json` + `dependencies.md` + `README.md`（ComfyUI 示例同时包含带坐标的 workflow.json 和精简 API 格式的 workflow_api.json）。

---

## 可编程架构（开发者使用）

除了 YAML 知识库外，项目提供了 Python 可编程层，方便集成到 Agent、MCP Server 或 Tool-calling 系统中：

```python
from core import WorkflowIR, ModelFamily, PipelineType, TargetPlatform, SamplingParams, LoraRef
from adapters.base_adapter import AdapterRegistry

ir = WorkflowIR(
    model_family=ModelFamily.FLUX,
    pipeline_type=PipelineType.TXT2IMG,
    target_platform=TargetPlatform.COMFYUI,
    prompt="a futuristic city at night",
    sampling=SamplingParams.defaults_for(ModelFamily.FLUX),
)

# 自动验证规则
print(ir.validate())               # ['ComfyUI workflow must have a terminal node']
print(ir.supports_negative_prompt())  # False — Flux 不支持负向提示词

# 跨平台翻译
output = AdapterRegistry.translate(ir, TargetPlatform.A1111)

# 知识索引查询
from knowledge.build_index import query_index
info = query_index(model="flux", platform="comfyui")
```

```
core/
└── ir/
    ├── parameter.py    ← 类型枚举 + 参数 dataclass
    ├── node.py         ← IRNode / NodeConnection / 端口类型表
    ├── workflow.py     ← WorkflowIR（校验、依赖提取、跨平台判断）
    └── translator.py   ← PlatformTranslator 抽象基类

adapters/
├── base_adapter.py     ← BaseAdapter + AdapterRegistry（统一接口 + 自动注册）

knowledge/
├── build_index.py      ← 自动扫描 yaml → 生成 .cache/index.json（gitignored）

tests/
├── validators/
│   └── test_validation.py  ← 语义 + 平台专项自动验证
```

---

## 测试覆盖

已通过 13 个标准测试用例验证：

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
| TC013 | InvokeAI 节点编辑器格式（UUID / snake_case / edges） |

运行自动验证：

```bash
python3 tests/validators/test_validation.py
```

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

## ☕ 打赏支持

如果这个项目帮到了你，欢迎请我喝杯咖啡 ☕

| 微信 | 支付宝 |
|:------:|:------:|
| <img src="assets/wechat-qr.png" width="200" alt="微信赞赏码"/> | <img src="assets/alipay-qr.png" width="200" alt="支付宝收款码"/> |

每一份支持都是持续更新和维护的动力 🌟

---

## License

MIT License — 免费商用，欢迎 fork 和 PR。
