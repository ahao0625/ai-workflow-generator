# 推广文案 / Promotional Copy

> 存放各类推广文案，按平台适配。直接复制使用。

---

## 社交媒体（微博/X/朋友圈）

```
你还在一个个节点地搭 ComfyUI 工作流吗？

现在只需要说一句话：
"帮我生成一个 SDXL 工作流，加两个 LoRA，要 ControlNet"

AI 直接给你吐出完整的 workflow.json + 模型下载链接 + 使用说明。

支持 ComfyUI · A1111 · Diffusers · Replicate · Midjourney
SD1.5 / SDXL / Flux / SD3 / 视频模型 全覆盖

开源免费 👇
github.com/ahao0625/ai-workflow-generator
```

---

## 技术社区（V2EX / 掘金 / CSDN）

**标题：用 一个 SKILL.md，让任意 LLM 变成你的 AI 绘图工作流生成器**

你有没有遇到过这种情况——

看到一个很酷的绘图效果，想要复现，但：

- **不记得** LoRA 应该串在哪个节点后面
- **不知道** Flux 的 KSampler cfg 必须设成 1.0
- **搞不清** SD3 要用 CLIPTextEncodeSD3 而不是普通 CLIPTextEncode
- 每次都要翻文档、查攻略，折腾半天才能跑通

现在，你只需要把这些知识**交给 AI**。

---

**它是怎么工作的？**

```
你说："帮我生成一个 SDXL 文生图工作流，加两个 LoRA"
  ↓
AI 自动识别你用的是 ComfyUI
  ↓
AI 读取知识库，构建"中间表示"（IR）
  ↓
AI 用 20 条规则验证你的需求
   ⚠️ "你用了 2 个 LoRA，好，MODEL 和 CLIP 都要串联"
   ⚠️ "SDXL 的 CLIP 是双路的，用 CLIPTextEncodeSDXL"
  ↓
AI 生成三件套：
  ✅ workflow.json  （拖进 ComfyUI 直接跑）
  ✅ dependencies.md（列好要下载哪些模型）
  ✅ 使用说明        （怎么加载，遇到问题查哪里）
```

---

**它能生成哪些平台？**

| 平台 | 生成的产物 | 用在哪 |
|------|-----------|--------|
| ComfyUI | `workflow.json` | 本地节点式工作流 |
| A1111 / Forge | `params.json` | 网页界面一键导入 |
| Diffusers | `pipeline.py` | Python 脚本本地跑 |
| Replicate / Stability | `request.json` + `curl.sh` | 云端 API 调用 |
| Midjourney | `/imagine prompt` | Discord / Web |

**支持的模型族**：SD1.5 · SDXL · SDXL Turbo · Flux.1 · SD3 · SD3.5 · AnimateDiff · SVD · CogVideoX · Wan 2.1

---

**为什么它比直接问 GPT 更好？**

普通的 GPT 你要手动告诉它：
- SDXL 的节点叫 `CLIPTextEncodeSDXL` 不是 `CLIPTextEncode`
- Flux 的 VAE 叫 `ae.safetensors` 不是普通的 VAE
- AnimateDiff 需要 `AnimateDiffLoaderWithContext` 节点

这个技能把**所有这些细节**都结构化地存进知识库，AI 每次都查规范生成，**不会漏、不会错**。

---

**接入方式（总有一种适合你）**

- **Claude Project** → 上传 knowledge/ + 粘贴 System Prompt ✅
- **ChatGPT GPTs** → Instructions + Knowledge + Code Interpreter
- **本地 Ollama / LM Studio** → System Prompt + 文件上传
- **开发者** → LangChain Tool / Dify 自定义工具 / Coze 插件 / Semantic Kernel

**3 分钟配置，终身使用。**

---

**开源地址**：https://github.com/ahao0625/ai-workflow-generator
**MIT 协议**，随便用，随便改。

---

## 一句话 Slogan

> **"说你想要的，AI 帮你生成。"**

---

## 对比图配套文案

| 以前 | 现在 |
|------|------|
| 打开 ComfyUI | 告诉 AI 你要什么 |
| 翻文档查节点名 | AI 自动选对节点 |
| 手动连 MODEL 和 CLIP | AI 自动串联双链路 |
| 查 Flux 参数规范 | AI 内置 Flux 规则 |
| 写 params.txt | AI 生成直接可用的文件 |
| 平均 30 分钟配置 | 30 秒搞定 |

> **"30分钟的活，30秒做完。"**
