from abc import abstractmethod

from api.src.services.base_service import ServiceBase


class SourcePlugin(ServiceBase):
    @abstractmethod
    def load(self, config: dict):
        pass
