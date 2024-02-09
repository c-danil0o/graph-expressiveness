import os

from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from jinja2 import Environment, FileSystemLoader, PackageLoader

from api.src.services.visualizer_plugin import VisualizerPlugin
from api.src.types.graph import Graph, Node, Edge


class Visualizer(VisualizerPlugin):

    def identifier(self):
        return "graph-explorer-simple-visualizer"

    def name(self):
        return "simple-visualizer"

    def show(self, input_graph):

        graph = input_graph

        nodes = [{"node_id": node.node_id, "data": node.data} for node in graph.nodes]

        edges = [{"source": edge.source.node_id, "target": edge.destination.node_id} for edge in graph.edges]

        context = {
            "nodes": nodes,
            "links": edges,
        }

        path = os.path.join(os.path.dirname(__file__))
        jinja_env = Environment(loader=FileSystemLoader(path))
        template = jinja_env.get_template('simple_visualization.html')

        return template.render(context)

