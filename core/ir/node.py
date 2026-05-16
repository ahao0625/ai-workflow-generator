from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


class NodePortType(str, Enum):
    MODEL = "MODEL"
    CLIP = "CLIP"
    VAE = "VAE"
    LATENT = "LATENT"
    IMAGE = "IMAGE"
    MASK = "MASK"
    CONDITIONING = "CONDITIONING"
    CONTROL = "CONTROL"
    STRING = "STRING"
    INT = "INT"
    FLOAT = "FLOAT"


@dataclass
class NodePort:
    name: str
    port_type: NodePortType
    slot_index: int = 0


@dataclass
class NodeConnection:
    from_node_id: str
    from_port: str        # port name, e.g. "MODEL"
    to_node_id: str
    to_port: str          # port name, e.g. "model"
    from_slot: int = 0    # output slot index on source node
    to_slot: int = 0      # input slot index on destination node
    port_type: str = ""   # ComfyUI type string, e.g. "MODEL", "LATENT"

    def as_comfyui_link(
        self,
        link_id: int,
        node_id_map: Dict[str, int],
    ) -> Tuple[int, int, int, int, int, str]:
        """Return a ComfyUI-format link tuple.

        ComfyUI links array format:
            [link_id, from_node_id, from_slot_index, to_node_id, to_slot_index, type_string]

        Args:
            link_id:      Global auto-incrementing link ID (starts at 1).
            node_id_map:  Maps internal string IDs to ComfyUI integer node IDs.
        """
        return (
            link_id,
            node_id_map[self.from_node_id],
            self.from_slot,
            node_id_map[self.to_node_id],
            self.to_slot,
            self.port_type or self.from_port,
        )


@dataclass
class IRNode:
    id: str
    class_type: str
    label: str = ""
    inputs: Dict[str, Any] = field(default_factory=dict)
    outputs: List[NodePort] = field(default_factory=list)
    widget_values: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def get_input(self, name: str, default: Any = None) -> Any:
        return self.inputs.get(name, default)

    def set_input(self, name: str, value: Any):
        self.inputs[name] = value

    def has_output_of_type(self, port_type: NodePortType) -> bool:
        return any(p.port_type == port_type for p in self.outputs)

    def clone(self, new_id: str) -> "IRNode":
        node = IRNode(
            id=new_id,
            class_type=self.class_type,
            label=self.label,
            inputs=dict(self.inputs),
            outputs=[NodePort(p.name, p.port_type, p.slot_index) for p in self.outputs],
            widget_values=dict(self.widget_values),
            metadata=dict(self.metadata),
        )
        return node


STANDARD_NODE_PORTS = {
    "CheckpointLoaderSimple": [
        NodePort("MODEL", NodePortType.MODEL, 0),
        NodePort("CLIP", NodePortType.CLIP, 1),
        NodePort("VAE", NodePortType.VAE, 2),
    ],
    "UNETLoader": [
        NodePort("MODEL", NodePortType.MODEL, 0),
    ],
    "DualCLIPLoader": [
        NodePort("CLIP", NodePortType.CLIP, 0),
    ],
    "VAELoader": [
        NodePort("VAE", NodePortType.VAE, 0),
    ],
    "CLIPTextEncode": [
        NodePort("CONDITIONING", NodePortType.CONDITIONING, 0),
    ],
    "CLIPTextEncodeSDXL": [
        NodePort("CONDITIONING", NodePortType.CONDITIONING, 0),
    ],
    "CLIPTextEncodeFlux": [
        NodePort("CONDITIONING", NodePortType.CONDITIONING, 0),
    ],
    "FluxGuidance": [
        NodePort("CONDITIONING", NodePortType.CONDITIONING, 0),
    ],
    "EmptyLatentImage": [
        NodePort("LATENT", NodePortType.LATENT, 0),
    ],
    "EmptySD3LatentImage": [
        NodePort("LATENT", NodePortType.LATENT, 0),
    ],
    "KSampler": [
        NodePort("LATENT", NodePortType.LATENT, 0),
    ],
    "VAEDecode": [
        NodePort("IMAGE", NodePortType.IMAGE, 0),
    ],
    "VAEEncode": [
        NodePort("LATENT", NodePortType.LATENT, 0),
    ],
    "VAEEncodeForInpaint": [
        NodePort("LATENT", NodePortType.LATENT, 0),
    ],
    "LoraLoader": [
        NodePort("MODEL", NodePortType.MODEL, 0),
        NodePort("CLIP", NodePortType.CLIP, 1),
    ],
    "ControlNetLoader": [
        NodePort("CONTROL_NET", NodePortType.CONTROL, 0),
    ],
    "ControlNetApplyAdvanced": [
        NodePort("CONDITIONING", NodePortType.CONDITIONING, 0),
    ],
    "LoadImage": [
        NodePort("IMAGE", NodePortType.IMAGE, 0),
        NodePort("MASK", NodePortType.MASK, 1),
    ],
    "SaveImage": [],
    "PreviewImage": [],
    "VHS_VideoCombine": [],
    "LoadAnimateDiffModel": [
        NodePort("MOTION_MODULE", NodePortType.MODEL, 0),
    ],
    "AnimateDiffLoaderWithContext": [
        NodePort("MODEL", NodePortType.MODEL, 0),
    ],
}


def get_node_ports(class_type: str) -> List[NodePort]:
    return STANDARD_NODE_PORTS.get(class_type, [])
