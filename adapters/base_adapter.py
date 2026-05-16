from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from core.ir.workflow import WorkflowIR
from core.ir.translator import PlatformTranslator
from core.ir.parameter import TargetPlatform, ModelFamily, PipelineType


class AdapterCapability:
    def __init__(self, can_import: bool = True, can_export: bool = True,
                 can_validate: bool = True, can_convert: bool = False):
        self.can_import = can_import
        self.can_export = can_export
        self.can_validate = can_validate
        self.can_convert = can_convert


class BaseAdapter(ABC):

    @property
    @abstractmethod
    def platform(self) -> TargetPlatform:
        ...

    @property
    @abstractmethod
    def supported_families(self) -> List[ModelFamily]:
        ...

    @property
    @abstractmethod
    def supported_pipelines(self) -> List[PipelineType]:
        ...

    @property
    def capability(self) -> AdapterCapability:
        return AdapterCapability()

    @property
    def translator(self) -> Optional[PlatformTranslator]:
        return None

    @abstractmethod
    def export_workflow(self, ir: WorkflowIR) -> Dict[str, Any]:
        ...

    @abstractmethod
    def import_workflow(self, raw: Dict[str, Any]) -> WorkflowIR:
        ...

    @abstractmethod
    def validate(self, ir: WorkflowIR) -> List[str]:
        ...

    def supports(self, model_family: ModelFamily, pipeline_type: PipelineType) -> bool:
        return model_family in self.supported_families and pipeline_type in self.supported_pipelines

    def convert_from(self, other_adapter: "BaseAdapter", raw: Dict[str, Any]) -> Optional[WorkflowIR]:
        if not self.capability.can_convert:
            return None
        ir = other_adapter.import_workflow(raw)
        return ir

    def convert_to(self, ir: WorkflowIR) -> Optional[Dict[str, Any]]:
        if not self.capability.can_convert:
            return None
        return self.export_workflow(ir)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} platform={self.platform.value}>"


class AdapterRegistry:
    _adapters: Dict[TargetPlatform, BaseAdapter] = {}

    @classmethod
    def register(cls, adapter: BaseAdapter):
        cls._adapters[adapter.platform] = adapter

    @classmethod
    def get(cls, platform: TargetPlatform) -> Optional[BaseAdapter]:
        return cls._adapters.get(platform)

    @classmethod
    def list_all(cls) -> List[BaseAdapter]:
        return list(cls._adapters.values())

    @classmethod
    def find_adapter(cls, model_family: ModelFamily, pipeline_type: PipelineType) -> List[BaseAdapter]:
        return [a for a in cls._adapters.values() if a.supports(model_family, pipeline_type)]

    @classmethod
    def translate(cls, ir: WorkflowIR, target: TargetPlatform) -> Optional[Dict[str, Any]]:
        adapter = cls.get(target)
        if adapter is None:
            return None
        return adapter.export_workflow(ir)
