from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .node import IRNode, NodeConnection, NodePortType, get_node_ports
from .parameter import (
    ModelFamily,
    PipelineType,
    TargetPlatform,
    OutputFormat,
    SamplingParams,
    LoraRef,
    ControlNetRef,
    IPAdapterRef,
    HiresFixParams,
    UpscaleModelParams,
    FaceRestoreParams,
    AnimateDiffParams,
)


@dataclass
class WorkflowIR:
    ir_version: str = "2.0"
    model_family: ModelFamily = ModelFamily.SDXL
    model_name: Optional[str] = None
    pipeline_type: PipelineType = PipelineType.TXT2IMG
    target_platform: TargetPlatform = TargetPlatform.COMFYUI

    prompt: str = ""
    negative_prompt: str = ""

    sampling: SamplingParams = field(default_factory=SamplingParams)
    output_format: OutputFormat = OutputFormat.PNG
    save_metadata: bool = True

    loras: List[LoraRef] = field(default_factory=list)
    controlnets: List[ControlNetRef] = field(default_factory=list)
    ipadapter: Optional[IPAdapterRef] = None

    hires_fix: Optional[HiresFixParams] = None
    upscale_model: Optional[UpscaleModelParams] = None
    face_restore: Optional[FaceRestoreParams] = None
    animatediff: Optional[AnimateDiffParams] = None

    input_image: Optional[str] = None
    input_mask: Optional[str] = None

    nodes: List[IRNode] = field(default_factory=list)
    connections: List[NodeConnection] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ir_version": self.ir_version,
            "model_family": self.model_family.value,
            "model_name": self.model_name,
            "pipeline_type": self.pipeline_type.value,
            "target_platform": self.target_platform.value,
            "prompt": self.prompt,
            "negative_prompt": self.negative_prompt,
            "sampling": {
                "width": self.sampling.width,
                "height": self.sampling.height,
                "steps": self.sampling.steps,
                "cfg": self.sampling.cfg,
                "sampler_name": self.sampling.sampler_name.value,
                "scheduler": self.sampling.scheduler.value,
                "seed": self.sampling.seed,
                "denoise": self.sampling.denoise,
                "batch_size": self.sampling.batch_size,
            },
            "output_format": self.output_format.value,
            "loras": [{"name": l.name, "weight_model": l.weight_model, "weight_clip": l.weight_clip} for l in self.loras],
            "controlnets": [
                {
                    "model": c.model,
                    "preprocessor": c.preprocessor,
                    "strength": c.strength,
                    "start_percent": c.start_percent,
                    "end_percent": c.end_percent,
                    "input_image": c.input_image,
                }
                for c in self.controlnets
            ],
        }

    def uses_dual_clip(self) -> bool:
        return self.model_family in (ModelFamily.SDXL, ModelFamily.SDXL_TURBO)

    def uses_triple_clip(self) -> bool:
        return self.model_family == ModelFamily.SD3

    def supports_negative_prompt(self) -> bool:
        return self.model_family not in (ModelFamily.FLUX, ModelFamily.SDXL_TURBO)

    def needs_flux_guidance(self) -> bool:
        return self.model_family == ModelFamily.FLUX

    def needs_16ch_latent(self) -> bool:
        return self.model_family in (ModelFamily.FLUX, ModelFamily.SD3)

    def needs_inpaint_encode(self) -> bool:
        return self.pipeline_type == PipelineType.INPAINT

    def is_video(self) -> bool:
        return self.pipeline_type in (PipelineType.IMG2VID, PipelineType.TXT2VID)

    def validate(self) -> List[str]:
        errors: List[str] = []
        if self.needs_inpaint_encode() and not self.input_mask:
            errors.append("INPAINT pipeline requires input_mask")
        if self.is_video() and self.model_family != ModelFamily.VIDEO:
            errors.append(f"Video pipeline requires model_family=video, got {self.model_family.value}")
        if not self.supports_negative_prompt() and self.negative_prompt:
            errors.append(f"{self.model_family.value} does not support negative prompt (R01)")
        # R03: Flux schnell distilled for ≤8 steps
        if (
            self.model_family == ModelFamily.FLUX
            and self.model_name
            and "schnell" in self.model_name.lower()
            and self.sampling.steps > 8
        ):
            errors.append(
                f"flux1-schnell is distilled for 1–4 steps; "
                f"current steps={self.sampling.steps} wastes compute (R03)"
            )
        if self.target_platform == TargetPlatform.COMFYUI:
            if not self._has_terminal_node():
                errors.append("ComfyUI workflow must have a terminal output node (SaveImage/PreviewImage/VHS_VideoCombine) (R08)")
            if not self._nodes_have_unique_ids():
                errors.append("ComfyUI nodes must have unique IDs (R09)")
        if self.target_platform == TargetPlatform.INVOKEAI:
            if self.model_family == ModelFamily.FLUX:
                errors.append("Flux is not supported in InvokeAI Node Editor (R24)")
            if self._has_integer_node_ids():
                errors.append("InvokeAI node IDs must be UUID strings, not integers (R21)")
        if self.target_platform == TargetPlatform.A1111:
            if self.sampling.width % 8 != 0 or self.sampling.height % 8 != 0:
                errors.append("A1111 dimensions must be divisible by 8 (R17)")
        if self.target_platform == TargetPlatform.DIFFUSERS:
            if not self.prompt:
                errors.append("Diffusers pipeline requires a prompt")
        return errors

    def _has_integer_node_ids(self) -> bool:
        for n in self.nodes:
            try:
                int(n.id)
                return True
            except (ValueError, TypeError):
                pass
        return False

    def _has_terminal_node(self) -> bool:
        terminal_types = {"SaveImage", "PreviewImage", "VHS_VideoCombine", "SaveAnimatedWEBP"}
        return any(n.class_type in terminal_types for n in self.nodes)

    def _nodes_have_unique_ids(self) -> bool:
        ids = [n.id for n in self.nodes]
        return len(ids) == len(set(ids))

    def get_unique_dependencies(self) -> List[str]:
        deps: List[str] = []
        if self.input_image:
            deps.append(self.input_image)
        if self.input_mask:
            deps.append(self.input_mask)
        for lora in self.loras:
            deps.append(f"{lora.name}.safetensors")
        for cn in self.controlnets:
            deps.append(cn.model)
            if cn.input_image:
                deps.append(cn.input_image)
        if self.ipadapter:
            deps.append(self.ipadapter.model)
            deps.append(self.ipadapter.clip_vision)
            deps.append(self.ipadapter.image)
        if self.upscale_model:
            deps.append(self.upscale_model.model)
        if self.animatediff:
            deps.append(self.animatediff.motion_model)
            if self.animatediff.motion_lora:
                deps.append(self.animatediff.motion_lora)
        return list(set(deps))
