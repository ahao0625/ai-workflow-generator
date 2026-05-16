from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List


class ModelFamily(str, Enum):
    SD15 = "sd15"
    SD2 = "sd2"
    SDXL = "sdxl"
    SDXL_TURBO = "sdxl_turbo"
    FLUX = "flux"
    SD3 = "sd3"
    CASCADE = "cascade"
    VIDEO = "video"


class PipelineType(str, Enum):
    TXT2IMG = "txt2img"
    IMG2IMG = "img2img"
    INPAINT = "inpaint"
    OUTPAINT = "outpaint"
    IMG2VID = "img2vid"
    TXT2VID = "txt2vid"
    UPSCALE = "upscale"
    FACEFIX = "facefix"


class SamplerName(str, Enum):
    EULER = "euler"
    EULER_ANCESTRAL = "euler_ancestral"
    DPMPP_2M = "dpmpp_2m"
    DPMPP_2M_SDE = "dpmpp_2m_sde"
    DPMPP_3M_SDE = "dpmpp_3m_sde"
    DPMPP_2S_ANCESTRAL = "dpmpp_2s_ancestral"
    DDIM = "ddim"
    UNI_PC = "uni_pc"
    LCM = "lcm"
    HEUN = "heun"


class Scheduler(str, Enum):
    NORMAL = "normal"
    KARRAS = "karras"
    EXPONENTIAL = "exponential"
    SGM_UNIFORM = "sgm_uniform"
    SIMPLE = "simple"
    DDIM_UNIFORM = "ddim_uniform"
    BETA = "beta"


class TargetPlatform(str, Enum):
    COMFYUI = "comfyui"
    COMFYUI_API = "comfyui_api"
    A1111 = "a1111"
    DIFFUSERS = "diffusers"
    REPLICATE = "replicate"
    STABILITY = "stability"
    INVOKEAI = "invokeai"
    MIDJOURNEY = "midjourney"
    DALLE = "dalle"
    IDEOGRAM = "ideogram"
    PROMPT_ONLY = "prompt_only"


class OutputFormat(str, Enum):
    PNG = "png"
    JPG = "jpg"
    WEBP = "webp"
    MP4 = "mp4"
    GIF = "gif"


@dataclass
class LoraRef:
    name: str
    weight_model: float = 0.8
    weight_clip: float = 0.8


@dataclass
class ControlNetRef:
    model: str
    preprocessor: str = "none"
    strength: float = 1.0
    start_percent: float = 0.0
    end_percent: float = 1.0
    input_image: Optional[str] = None


@dataclass
class IPAdapterRef:
    model: str
    clip_vision: str
    image: str
    weight: float = 1.0
    weight_type: str = "linear"
    combine_embeds: str = "concat"


@dataclass
class HiresFixParams:
    enabled: bool = False
    upscale_by: float = 2.0
    upscale_method: str = "bislerp"
    steps: int = 15
    denoise: float = 0.45
    sampler: Optional[str] = None


@dataclass
class UpscaleModelParams:
    model: str
    factor: float = 4.0


@dataclass
class FaceRestoreParams:
    method: str = "codeformer"
    fidelity: float = 0.7


@dataclass
class AnimateDiffParams:
    motion_model: str
    context_length: int = 16
    context_stride: int = 1
    context_overlap: int = 4
    fps: int = 8
    total_frames: int = 16
    motion_lora: Optional[str] = None
    motion_lora_strength: float = 1.0


@dataclass
class SamplingParams:
    width: int = 1024
    height: int = 1024
    steps: int = 25
    cfg: float = 7.0
    sampler_name: SamplerName = SamplerName.EULER
    scheduler: Scheduler = Scheduler.KARRAS
    seed: int = -1
    denoise: float = 1.0
    batch_size: int = 1

    @classmethod
    def defaults_for(cls, family: ModelFamily) -> "SamplingParams":
        defaults = {
            ModelFamily.SD15:     dict(width=512, height=512, steps=20, cfg=7.0, sampler_name=SamplerName.DPMPP_2M, scheduler=Scheduler.KARRAS),
            ModelFamily.SD2:      dict(width=768, height=768, steps=20, cfg=7.0, sampler_name=SamplerName.DPMPP_2M, scheduler=Scheduler.KARRAS),
            ModelFamily.SDXL:     dict(width=1024, height=1024, steps=25, cfg=7.0, sampler_name=SamplerName.DPMPP_2M, scheduler=Scheduler.KARRAS),
            ModelFamily.SDXL_TURBO: dict(width=1024, height=1024, steps=4, cfg=1.0, sampler_name=SamplerName.EULER, scheduler=Scheduler.SGM_UNIFORM),
            ModelFamily.FLUX:     dict(width=1024, height=1024, steps=20, cfg=1.0, sampler_name=SamplerName.EULER, scheduler=Scheduler.SIMPLE),
            ModelFamily.SD3:      dict(width=1024, height=1024, steps=28, cfg=4.5, sampler_name=SamplerName.DPMPP_2M, scheduler=Scheduler.SGM_UNIFORM),
            ModelFamily.CASCADE:  dict(width=1024, height=1024, steps=20, cfg=4.0, sampler_name=SamplerName.EULER, scheduler=Scheduler.KARRAS),
            ModelFamily.VIDEO:    dict(width=512, height=512, steps=20, cfg=7.0, sampler_name=SamplerName.DPMPP_2M, scheduler=Scheduler.KARRAS),
        }
        return cls(**defaults.get(family, {}))
