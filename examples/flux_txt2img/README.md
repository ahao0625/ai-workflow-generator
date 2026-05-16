# Example: Flux.1-dev txt2img

Minimal Flux.1-dev text-to-image workflow for ComfyUI.

## Nodes

| ID | Class | Role |
|----|-------|------|
| 1 | DualCLIPLoader | Load CLIP-L + T5-XXL text encoders |
| 2 | UNETLoader | Load Flux DiT model |
| 3 | VAELoader | Load Flux AE VAE |
| 4 | CLIPTextEncodeFlux | Encode positive prompt (no negative) |
| 5 | FluxGuidance | Set guidance (3.5 for dev, 1.0 for schnell) |
| 6 | EmptySD3LatentImage | 16-channel latent at 1024×1024 |
| 7 | KSampler | Sample with cfg=1.0, euler+simple |
| 8 | VAEDecode | Decode 16-ch latent to image |
| 9 | SaveImage | Save PNG output |

## Key Notes

- **No negative prompt**: Flux does not support negative prompts.
- **KSampler cfg must be 1.0**: Guidance is controlled by the FluxGuidance node.
- **16-channel latent**: Uses EmptySD3LatentImage, not EmptyLatentImage.
- **Dual CLIP**: Requires both CLIP-L (clip_l.safetensors) and T5-XXL (t5xxl_fp16.safetensors).

## Required Models

See `dependencies.md`.
