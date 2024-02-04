from django.template.loader import render_to_string

from api.src.types.graph import Graph
from core.src.models.tree import Tree
from core.src.use_cases.loader import Loader


class TreeView(object):
    def __init__(self, graph: Graph):
        self.graph = graph
        self.tree = None

    def generate_tree_view(self) -> str:
        if self.graph.get_node_count() <= 0:
            return ''
        self.tree = Tree(self.graph)
        context = {
            "input_tree": self.tree.get_json(),
        }
        return render_to_string('tree_view_template.html', context)
