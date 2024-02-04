import copy

from core.src.use_cases.loader import Loader
from api.src.types.graph import Graph, Node, Edge
from core.src.models.plugin import Plugin


def is_node_valid_search(node: Node, search_text: str) -> bool:
    node_data = node.data
    if search_text in str(node.node_id):
        return True
    for value in node_data.values():
        if search_text in str(value):
            return True
    return False


def compare(comparator: str, value1, value2) -> bool:
    if comparator == '==':
        return value1 == value2
    elif comparator == '>':
        return value1 > value2
    elif comparator == '>=':
        return value1 >= value2
    elif comparator == '<':
        return value1 < value2
    elif comparator == '<=':
        return value1 <= value2
    elif comparator == '!=':
        return value1 != value2
    else:
        return False


def is_node_valid_filter(node: Node, attribute: str, comparator: str, value: str) -> bool:
    if attribute == "id":
        return compare(comparator, node.node_id, value)
    else:
        try:
            node_data = node.data
            data_type = type(node_data[attribute])
            value = data_type(value)
            return compare(comparator, node_data[attribute], value)
        except:
            return False


class MainView(object):
    def __init__(self):
        self.loader = Loader()
        self.sources = self.loader.sources
        self.visualizers = self.loader.visualizers
        self.full_graph: Graph = None
        self.current_graph: Graph = None
        self.current_visualizer_plugin_id: int = 0
        self.current_source_plugin_id: int = 0

    def generate_main_view(self, source_plugin_id: int, visualizer_plugin_id: int):
        self.current_graph = self.loader.get_loaded_graph(source_plugin_id)
        self.full_graph = copy.deepcopy(self.current_graph)
        self.current_source_plugin_id = source_plugin_id
        self.current_visualizer_plugin_id = visualizer_plugin_id
        return self.visualizers[visualizer_plugin_id].plugin.show(self.current_graph)

    def generate_from_search_query(self, search_text: str):
        if self.current_graph is None:
            return ''
        new_graph: Graph = Graph(self.current_graph.name, None, [], [])
        for node in self.current_graph.nodes:
            if is_node_valid_search(node, search_text):
                new_graph.add_node(node)
        self.add_edges(new_graph)
        return self.visualizers[self.current_visualizer_plugin_id].plugin.show(new_graph)

    def generate_from_filter_query(self, attribute: str, comparator: str, value: str):
        if self.current_graph is None:
            return ''
        new_graph: Graph = Graph(self.current_graph.name, None, [], [])
        for node in self.current_graph.nodes:
            if is_node_valid_filter(node, attribute, comparator, value):
                new_graph.add_node(node)
        self.add_edges(new_graph)
        return self.visualizers[self.current_visualizer_plugin_id].plugin.show(new_graph)

    def clear_filters(self):
        if self.full_graph is None:
            return ''
        self.current_graph = copy.deepcopy(self.full_graph)
        self.loader.set_loaded_graph(self.current_graph, self.current_source_plugin_id)
        return self.visualizers[self.current_visualizer_plugin_id].plugin.show(self.full_graph)

    def add_edges(self, new_graph: Graph):
        if new_graph.get_node_count() > 0:
            new_graph.set_root(new_graph.nodes[0])
            for edge in self.current_graph.edges:
                if edge.source in new_graph.nodes and edge.destination in new_graph.nodes:
                    new_graph.add_edge(edge)
        self.current_graph = new_graph
        self.loader.set_loaded_graph(self.current_graph, self.current_source_plugin_id)

