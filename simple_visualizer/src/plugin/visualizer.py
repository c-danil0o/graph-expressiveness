from urllib import request

from django.shortcuts import render

from api.src.services.visualizer_plugin import VisualizerPlugin
from api.src.types.graph import Graph, Node, Edge


class Visualizer(VisualizerPlugin):

    def identifier(self):
        return "graph-explorer-simple-visualizer"

    def name(self):
        return "simple-visualizer"

    def show(self):

        node1 = Node(1, {"label": "Node 1"})
        node2 = Node(2, {"label": "Node 2"})
        node3 = Node(3, {"label": "Node 3"})
        node4 = Node(4, {"label": "Node 4"})

        edge1 = Edge(101, {"weight": 5}, node1, node2, directed=True)
        edge2 = Edge(102, {"weight": 3}, node2, node3, directed=False)
        edge3 = Edge(103, {"weight": 7}, node3, node4, directed=True)

        graph = Graph("Example Graph", node1, [edge1, edge2, edge3], [node1, node2, node3, node4])

        nodes = [{"node_id": node.node_id, "data": node.data} for node in graph.nodes]

        edges = [{"source": edge.source.node_id, "target": edge.destination.node_id} for edge in graph.edges]

        context = {
            "nodes": nodes,
            "edges": edges,
        }
        return render(request, "simple_visualizator/simple_visualizator.html", context=context)

