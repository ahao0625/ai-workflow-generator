# AI Workflow Generator / AI工作流生成器

> 用自然语言描述需求，即可在任意 AI 图像平台上生成可用工作流文件。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Status: Production](https://img.shields.io/badge/Status-Production Ready-green.svg)]()

---

## 是什么

一个**给 AI 读的技术说明书**（SKILL.md），配合结构化的模型知识库，让任何支持长上下文的 LLM（Claude / GPT-4 / Gemini / DeepSeek / Kimi…）都能在理解用户需求后，自动生成以下平台的工作流文件：

| 平台 | 输出格式 |
|------|---------|
| **ComfyUI** | `workflow.json` + `workflow_api.json` |
| **A1111 / Forge / SD.Next** | `params.json` |
| **HuggingFace Diffusers** | `pipeline.py` + `requirements.txt` |
| **Replicate / Stability AI** | `request.json` + `example.sh` |
| **Midjourney / DALL·E / Ideogram** | `/imagine prompt` + 参数 |

支持的模型族：SD 1.5 / SDXL / SDXL Turbo / Flux / SD3 / SD3.5 / AnimateDiff / SVD / CogVideoX / Wan 2.1

---

## 快速开始

### 方式一：粘贴 System Prompt（最简单）

1. 复制 `adapters/prompt/universal_system.md` 的内容
2. 粘贴到你的 AI 助手的 System Prompt 中
3. 上传 `knowledge/` 文件夹作为上下文
4. 开始对话：`"帮我生成一个 SDXL 工作流，加两个 LoRA"`

### 方式二：Claude Project（推荐）

1. 在 Claude 创建新 Project
2. 上传整个 `knowledge/` 文件夹
3. 把 `adapters/prompt/claude_system.md` 设为 Project Instructions
4. 开始使用

### 方式三：ChatGPT GPTs

1. 创建新 GPT
2. 把 `adapters/prompt/chatgpt_instructions.md` 粘贴到 Instructions
3. 上传 `knowledge/` 下所有 YAML 文件到 Knowledge
4. 开启 Code Interpreter

### 方式四：结构化调用（LangChain / Dify / Coze）

| 平台 | 文件 |
|------|------|
| LangChain | `adapters/langchain/workflow_generator_tool.py` |
| Dify | `adapters/dify/tool_manifest.yaml` |
| Coze (扣子) | `adapters/coze/plugin_manifest.json` |
| Open WebUI | `adapters/open_webui/skill_function.py` |
| Semantic Kernel | `adapters/semantic_kernel/skill.yaml` |

---

## 工作原理

```
用户自然语言描述
       ↓
① 平台识别（ComfyUI / A1111 / Diffusers / API / Prompt-only）
       ↓
② 意图解析 → 构建 IR（中间表示）
   - model_family / pipeline_type / loras / controlnets …
       ↓
③ 验证（20 条规则，CRITICAL 阻止渲染）
   - Flux 无负向提示词 / Inpaint 须用 VAEEncodeForInpaint / LoRA 双链路 …
       ↓
④ 平台渲染（IR → 原生格式）
   - 节点图 / 参数表 / Python 脚本 / API 请求 / 提示词
       ↓
⑤ 输出三件套
   - 工作流文件 + dependencies.md + 使用说明
```

---

## 目录结构

```
ai-workflow-generator/
├── SKILL.md                        # AI 技能核心说明（所有平台共用）
│
├── adapters/                       # 各平台适配层
│   ├── prompt/                     # System Prompt 版本
│   │   ├── claude_system.md        #   Claude 专用
│   │   ├── chatgpt_instructions.md #   GPTs 专用
│   │   ├── gemini_instruction.md   #   Gemini 专用
│   │   └── universal_system.md      #   通用版（最大兼容）
│   ├── langchain/                  # LangChain Tool
│   ├── dify/                       # Dify 自定义工具
│   ├── coze/                       # Coze 插件
│   ├── open_webui/                 # Open WebUI Tools
│   └── semantic_kernel/             # 微软 Semantic Kernel
│
├── knowledge/                      # 技能知识库
│   ├── ir_schema.yaml             #   中间表示规范
│   ├── validators/rules.yaml       #   20 条验证规则
│   ├── models/                     #   模型族规范
│   │   ├── sd15.yaml              #   SD 1.5
│   │   ├── sdxl.yaml              #   SDXL
│   │   ├── flux.yaml              #   Flux.1
│   │   ├── sd3.yaml               #   SD3 / 3.5
│   │   └── video.yaml             #   视频生成
│   ├── nodes/                      #   ComfyUI 节点库
│   │   ├── native_nodes.yaml       #   原生节点（80+）
│   │   └── custom_nodes.yaml       #   扩展节点（IPAdapter/InstantID/…）
│   └── platforms/                  #   平台渲染器
│       ├── comfyui.yaml            #   ComfyUI JSON 渲染器
│       ├── a1111.yaml              #   A1111 参数渲染器
│       ├── diffusers.yaml           #   Diffusers 脚本渲染器
│       ├── api.yaml                #   REST API 渲染器
│       └── prompt_only.yaml         #   纯提示词渲染器
│
└── tests/                         # 测试基础设施
    ├── test_cases.json             #   12 个标准测试用例
    └── expected_outputs/           #   期望输出样本
```

---

## 使用示例

### "帮我生成一个 SDXL 文生图工作流，加两个 LoRA"

→ 输出 ComfyUI `workflow.json` + `dependencies.md` + 使用说明

### "Flux.1-dev + ControlNet depth，输出 A1111 参数"

→ 输出 `params.json`（Flux 自动去除负向提示词，Forge 配置）

### "生成一个 SD3 的 Replicate API 请求"

→ 输出 `request.json` + `example.sh`（含 curl 命令）

### "把这个 ComfyUI 工作流转成 Diffusers Python"

→ 跨平台转换，自动标注转换损失

---

## 测试

测试用例位于 `tests/test_cases.json`，覆盖：

| 用例 | 平台 | 测试点 |
|------|------|--------|
| TC001 | ComfyUI | SDXL + 2 LoRA 链路正确性 |
| TC002 | ComfyUI | Flux + ControlNet + 无负向提示词 |
| TC003 | ComfyUI | SD1.5 Inpaint 强制 VAEEncodeForInpaint |
| TC004 | A1111 | LoRA 嵌入提示词语法 |
| TC005 | A1111 Forge | Flux schnell 步数约束 |
| TC006 | Diffusers | SDXL pipeline.py 完整性 |
| TC007 | Replicate | SD3 API 请求格式 |
| TC008 | Midjourney | 跨平台 SDXL → 自然语言提示词 |
| TC009 | ComfyUI | AnimateDiff 视频工作流 |
| TC010 | Stability | SD3 Ultra API 请求 |
| TC011 | ComfyUI | 多 ControlNet 链式串联 |
| TC012 | Diffusers | SDXL Base + Refiner 两阶段 |

---

## 贡献

欢迎提交 Issue 或 PR。以下为优先领域：

- 📡 新增 API 提供方（如 Together AI、Fireworks、Replicate VLM）
- 🎨 新模型族适配（如 FLUX.1 Pro、Stable Diffusion 3.5 Large）
- 🧪 补充测试用例
- 🌐 翻译（欢迎中英文以外的语言适配）

---

## License

MIT License — 可自由使用、修改、商业化。
