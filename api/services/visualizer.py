from abc import ABC, abstractmethod


class BaseVisualizer(ABC):

    @abstractmethod
    def identifier(self):
        pass

    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def visualize(self, graph, request):
        pass
