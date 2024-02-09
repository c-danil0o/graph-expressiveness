import copy

from core.src.use_cases.loader import Loader
from api.src.types.graph import Graph, Node, Edge


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


class Workspace(object):
    def __init__(self, current_graph: Graph = None, full_graph: Graph = None):
        self.current_graph: Graph = current_graph
        self.full_graph: Graph = full_graph
        self.visualizer_id = -1
        self.source_id = -1
        self.config = {}

    def set_current_graph(self, graph: Graph):
        self.current_graph = graph

    def set_full_graph(self, graph: Graph):
        self.full_graph = graph

    def is_loaded(self) -> bool:
        return self.current_graph is not None

    def set_visualizer_id(self, visualizer_id: int):
        self.visualizer_id = visualizer_id

    def set_source_id(self, source_id: int):
        self.source_id = source_id

    def set_config(self, config):
        self.config = config

class MainView(object):
    def __init__(self):
        self.loader = Loader()
        self.sources = self.loader.sources
        self.visualizers = self.loader.visualizers
        self.current_workspace: int = 1
        self.workspaces: dict[int, Workspace] = {1: Workspace(), 2: Workspace(), 3: Workspace()}

    def generate_main_view(self, source_plugin_id: int, visualizer_plugin_id: int, config: dict, workspace_id: int):
        self.workspaces[workspace_id].set_current_graph(self.loader.get_loaded_graph(source_plugin_id, config))
        print(self.workspaces[workspace_id].current_graph)
        self.workspaces[workspace_id].set_full_graph(copy.deepcopy(self.workspaces[workspace_id].current_graph))
        self.workspaces[workspace_id].set_visualizer_id(visualizer_plugin_id)
        self.workspaces[workspace_id].set_source_id(source_plugin_id)
        self.workspaces[workspace_id].set_config(config)

        return self.visualizers[visualizer_plugin_id].plugin.show(self.workspaces[workspace_id].current_graph)

    def generate_from_search_query(self, search_text: str, workspace_id: int):
        if self.workspaces[workspace_id].current_graph is None:
            return ''
        new_graph: Graph = Graph(self.workspaces[workspace_id].current_graph.name, None, [], [])
        for node in self.workspaces[workspace_id].current_graph.nodes:
            if is_node_valid_search(node, search_text):
                new_graph.add_node(node)
        self.add_edges(new_graph, workspace_id)
        self.workspaces[workspace_id].set_current_graph(new_graph)
        return self.visualizers[self.workspaces[workspace_id].visualizer_id].plugin.show(new_graph)

    def generate_from_filter_query(self, attribute: str, comparator: str, value: str, workspace_id: int):
        if self.workspaces[workspace_id].current_graph is None:
            return ''
        new_graph: Graph = Graph(self.workspaces[workspace_id].current_graph.name, None, [], [])
        for node in self.workspaces[workspace_id].current_graph.nodes:
            if is_node_valid_filter(node, attribute, comparator, value):
                new_graph.add_node(node)
        self.add_edges(new_graph, workspace_id)
        self.workspaces[workspace_id].set_current_graph(new_graph)
        return self.visualizers[self.workspaces[workspace_id].visualizer_id].plugin.show(new_graph)

    def clear_filters(self, workspace_id: int):
        if self.workspaces[workspace_id].full_graph is None:
            return ''
        self.workspaces[workspace_id].current_graph = copy.deepcopy(self.workspaces[workspace_id].full_graph)
        return self.visualizers[self.workspaces[workspace_id].visualizer_id].plugin.show(self.workspaces[workspace_id].full_graph)

    def add_edges(self, new_graph: Graph, workspace_id: int):
        if new_graph.get_node_count() > 0:
            new_graph.set_root(new_graph.nodes[0])
            for edge in self.workspaces[workspace_id].current_graph.edges:
                if edge.source in new_graph.nodes and edge.destination in new_graph.nodes:
                    new_graph.add_edge(edge)
        self.workspaces[workspace_id].current_graph = new_graph

    def is_workspace_loaded(self, workspace_id: int):
        return self.workspaces[workspace_id].is_loaded()

    def render_workspace_graph(self, workspace_id: int):
        return self.visualizers[self.workspaces[workspace_id].visualizer_id].plugin.show(self.workspaces[workspace_id].current_graph)

    def get_workspace_visualizer(self, workspace_id: int):
        return self.workspaces[workspace_id].visualizer_id

    def get_workspace_source(self, workspace_id: int):
        return self.workspaces[workspace_id].source_id

    def get_workspace_config(self, workspace_id: int):
        return self.workspaces[workspace_id].config

    def change_visualizer(self, workspace_id: int, visualizer_id: int):
        self.workspaces[workspace_id].set_visualizer_id(visualizer_id)
        return self.visualizers[self.workspaces[workspace_id].visualizer_id].plugin.show(self.workspaces[workspace_id].current_graph)
