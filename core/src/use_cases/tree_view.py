from api.src.types.graph import Graph
from core.src.models.tree import Tree
from core.src.use_cases.loader import Loader


class TreeView(object):
    def __init__(self, loader: Loader, source_plugin_id: int):
        self.loader = loader
        self.graph = loader.get_loaded_graph(source_plugin_id)
        self.tree = None

    def generate_tree_view(self):
        self.tree = Tree(self.graph.root, self.graph)
        print(self.tree)
