# Dependencies

## Custom Nodes
- **ComfyUI-IPAdapter-Plus** → [GitHub](https://github.com/cubiq/ComfyUI_IPAdapter_plus)
  - Install via ComfyUI-Manager: `cubiq/ComfyUI_IPAdapter_plus`

## Models

### Checkpoints
- `models/checkpoints/sd_xl_base_1.0.safetensors` → [Download](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0)

### VAE
- `models/vae/sdxl_vae.safetensors` → [Download](https://huggingface.co/stabilityai/sdxl-vae) (if not bundled with checkpoint)

### IP-Adapter Models
- `models/ipadapter/ip-adapter-faceid_sdxl.bin` → [Download (huggingface)](https://huggingface.co/h94/IP-Adapter-FaceID)
- `models/ipadapter/ip-adapter-faceid-plusv2_sdxl.bin` → [Download (huggingface)](https://huggingface.co/h94/IP-Adapter-FaceID) (optional, better for SDXL)
- `models/clip_vision/CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors` → [Download](https://huggingface.co/h94/IP-Adapter)

### InsightFace (for FaceID)
- Download InsightFace models and place in `ComfyUI/custom_nodes/ComfyUI_IPAdapter_plus/models/insightface/`
  - Download link: [insightface models](https://github.com/deepinsight/insightface)
  - Required files: `1k3d68.onnx`, `2d106det.onnx`, `det_10g.onnx`, etc.
