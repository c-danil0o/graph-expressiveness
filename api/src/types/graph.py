import typing
from abc import ABC, abstractmethod


class NodeModel(ABC):
    def __init__(self, node_id: int, data: dict):
        self.node_id = node_id
        self.data = data


class EdgeModel(ABC):
    def __init__(self, edge_id: int, data: dict, source: NodeModel, direction: NodeModel, directed: bool):
        self.edge_id = edge_id
        self.data = data
        self.source = source
        self.direction = direction
        self.directed = directed


class GraphModel(ABC):
    def __init__(self, name: str, root: NodeModel, edges: list[EdgeModel], nodes: list[NodeModel], ):
        self.name = name
        self.root = root
        self.edges = edges
        self.nodes = nodes
