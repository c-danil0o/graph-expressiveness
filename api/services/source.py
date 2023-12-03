from abc import ABC, abstractmethod


class BaseLoader(ABC):

    @abstractmethod
    def identifier(self):
        pass

    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def load_file(self, file_name, unique_key=None):
        pass

    # @abstractmethod
    # def make_graph(self, tree):
    #     pass
