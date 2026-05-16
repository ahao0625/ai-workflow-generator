# Example: SDXL + IPAdapter FaceID + img2img

This demo workflow combines three techniques:

| Node | Role |
|------|------|
| CheckpointLoaderSimple (1) | Load SDXL checkpoint |
| CLIPTextEncodeSDXL ×2 (2,3) | Positive / Negative prompts |
| LoadImage (4) | **Reference face** for IPAdapter FaceID identity transfer |
| LoadImage (5) | **Base image** for img2img denoising |
| IPAdapterUnifiedLoader (6) | Load SDXL FaceID IPAdapter model |
| IPAdapterAdvanced (7) | Apply face identity to MODEL |
| VAEEncode (8) | Encode base image into latent for img2img |
| KSampler (9) | Sample with denoise=0.75 (img2img strength) |
| VAEDecode (10) | Decode latent to image |
| SaveImage (11) | Save result |

## Required Models
See `dependencies.md`.

## Note
This is **img2img** (not inpaint). For inpainting, replace VAEEncode with `VAEEncodeForInpaint` and provide a mask.
