from abc import abstractmethod
import typing

from api.src.services.base_service import ServiceBase
from api.src.types.param import Param


class SourcePlugin(ServiceBase):
    @abstractmethod
    def load(self, config: dict):
        pass

    @abstractmethod
    def params(self) -> list[Param]:
        pass
