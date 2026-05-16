# Example: AnimateDiff txt2vid (Basic)

Basic AnimateDiff text-to-video workflow for ComfyUI using SD1.5 base.

## Nodes

| ID | Class | Role |
|----|-------|------|
| 1 | CheckpointLoaderSimple | Load SD1.5 checkpoint |
| 2 | CLIPTextEncode | Positive prompt |
| 3 | CLIPTextEncode | Negative prompt |
| 4 | LoadAnimateDiffModel | Load motion module (mm_sd_v15_v2) |
| 5 | AnimateDiffLoaderWithContext | Apply motion to model |
| 6 | EmptyLatentImage | 512×512, 16-frame batch |
| 7 | KSampler | Sample with 20 steps |
| 8 | VAEDecode | Decode latent frames |
| 9 | VHS_VideoCombine | Combine frames → MP4 |

## Key Notes

- Motion module loaded: mm_sd_v15_v2 (SD1.5 motion)
- AnimateDiffLoaderWithContext must sit between CheckpointLoader and KSampler
- LoRA nodes (if any) go BEFORE AnimateDiffLoaderWithContext
- VHS_VideoCombine requires VideoHelperSuite custom node
- Output: 16 frames at 8 fps → 2 seconds of video

## Required Models

See `dependencies.md`.

## Required Custom Nodes

- `Kosinkadink/ComfyUI-AnimateDiff-Evolved`
- `Kosinkadink/ComfyUI-VideoHelperSuite`
