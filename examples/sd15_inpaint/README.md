# Example: SD1.5 Inpaint

Inpainting workflow for ComfyUI using VAEEncodeForInpaint.

## Nodes

| ID | Class | Role |
|----|-------|------|
| 1 | CheckpointLoaderSimple | Load SD1.5 checkpoint |
| 2 | CLIPTextEncode | Positive prompt |
| 3 | CLIPTextEncode | Negative prompt |
| 4 | LoadImage | Input image to inpaint |
| 5 | LoadImage | Mask image (white = inpaint area) |
| 6 | VAEEncodeForInpaint | Encode image + mask to latent (R06) |
| 7 | KSampler | Sample with denoise=0.9 |
| 8 | VAEDecode | Decode latent to image |
| 9 | SaveImage | Save result |

## Key Notes

- **Must use VAEEncodeForInpaint**, NOT VAEEncode. Plain VAEEncode corrupts masks.
- The mask image should have white pixels where you want inpainting, black where you want to preserve.
- denoise=0.9 gives strong inpainting; lower to 0.7 for more subtle changes.
- SD1.5 works best at 512×512.

## Required Models

See `dependencies.md`.
