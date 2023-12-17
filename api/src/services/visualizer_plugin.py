from abc import abstractmethod

from api.src.services.base_service import ServiceBase


class VisualizerPlugin(ServiceBase):
    @abstractmethod
    def show(self):
        pass