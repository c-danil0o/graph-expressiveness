import typing


class Graph:
    def __init__(self, *args, **kwargs):
        self.__id: int = kwargs.get('id', None)
        self.name: str = kwargs.get('name', None)
        self.nodes: list[Node] = kwargs.get('nodes', None)
        self.vertices: list[Vertex] = kwargs.get('vertices', None)
        self.root: Node = kwargs.get('root', None)


class Node:
    def __init__(self, *args, **kwargs):
        self.__id: int = kwargs.get('id', None)
        self.__data: dict = kwargs.get('data', None)


class Vertex:
    def __init__(self, *args, **kwargs):
        self.__id: int = kwargs.get('id', None)
        self.__directed: bool = kwargs.get('directed', False)
        self.__source: Node = kwargs.get('source', None)
        self.__destination: Node = kwargs.get('destination', None)

    @property
    def directed(self):
        return self.__directed

    @directed.setter
    def directed(self, value: bool):
        if isinstance(value, bool):
            self.__directed = value
        else:
            raise TypeError('Has to be boolean')
