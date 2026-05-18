from .ir.workflow import WorkflowIR
from .ir.node import IRNode, NodeConnection, NodePort, NodePortType, get_node_ports, STANDARD_NODE_PORTS
from .ir.parameter import (
    ModelFamily, PipelineType, SamplerName, Scheduler,
    TargetPlatform, OutputFormat, SamplingParams,
    LoraRef, ControlNetRef, IPAdapterRef,
    HiresFixParams, UpscaleModelParams, FaceRestoreParams, AnimateDiffParams,
)
from .ir.translator import PlatformTranslator

from .comfy_template_engine.template_selector import (
    select_template, load_template, list_available_templates, has_template,
    REQUIRES_FLUX_GUIDANCE, REQUIRES_16CH_LATENT, NO_NEGATIVE_PROMPT,
    USES_DUAL_CLIP, USES_TRIPLE_CLIP,
)
from .comfy_template_engine.injector import (
    inject_parameters, extract_placeholders, fill_defaults,
)
from .comfy_template_engine.module_composer import compose, compose_lora, compose_controlnet
from .comfy_template_engine.validator import validate_workflow, validate_against_ir
from .comfy_template_engine.schema_registry import (
    get_widget_fields, get_widget_index, get_schema as get_widget_schema,
)
from .comfy_template_engine.capability_registry import (
    get_capabilities, get_inputs, get_outputs, get_compatible_models,
    is_compatible, validate_node_compatibility,
)

__all__ = [
    # IR
    "WorkflowIR",
    "IRNode", "NodeConnection", "NodePort", "NodePortType",
    "get_node_ports", "STANDARD_NODE_PORTS",
    "ModelFamily", "PipelineType", "SamplerName", "Scheduler",
    "TargetPlatform", "OutputFormat", "SamplingParams",
    "LoraRef", "ControlNetRef", "IPAdapterRef",
    "HiresFixParams", "UpscaleModelParams", "FaceRestoreParams", "AnimateDiffParams",
    "PlatformTranslator",
    # Template engine — selection
    "select_template", "load_template", "list_available_templates", "has_template",
    "REQUIRES_FLUX_GUIDANCE", "REQUIRES_16CH_LATENT", "NO_NEGATIVE_PROMPT",
    "USES_DUAL_CLIP", "USES_TRIPLE_CLIP",
    # Template engine — injection
    "inject_parameters", "extract_placeholders", "fill_defaults",
    # Template engine — composition
    "compose", "compose_lora", "compose_controlnet",
    # Template engine — validation
    "validate_workflow", "validate_against_ir",
    # Template engine — schema & capability
    "get_widget_fields", "get_widget_index", "get_widget_schema",
    "get_capabilities", "get_inputs", "get_outputs", "get_compatible_models",
    "is_compatible", "validate_node_compatibility",
]
