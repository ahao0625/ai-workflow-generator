from abc import ABC, abstractmethod
from typing import Any, Dict

from .workflow import WorkflowIR
from .parameter import TargetPlatform


class PlatformTranslator(ABC):

    @property
    @abstractmethod
    def target_platform(self) -> TargetPlatform:
        ...

    @abstractmethod
    def translate(self, ir: WorkflowIR) -> Dict[str, Any]:
        ...

    @abstractmethod
    def parse(self, raw: Dict[str, Any]) -> WorkflowIR:
        ...

    def validate_ir(self, ir: WorkflowIR) -> Dict[str, Any]:
        errors = ir.validate()
        return {"valid": len(errors) == 0, "errors": errors}

    def roundtrip_check(self, ir: WorkflowIR) -> bool:
        serialized = self.translate(ir)
        parsed = self.parse(serialized)
        return ir.model_family == parsed.model_family and ir.pipeline_type == parsed.pipeline_type
