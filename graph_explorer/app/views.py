import re

from django.shortcuts import render
import os
import sys

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.append(BASE_DIR)

from core.src.use_cases.loader import Loader
from core.src.use_cases.main_view import MainView
from core.src.models.tree import Tree
from core.src.use_cases.tree_view import TreeView

loader = Loader()
loader.init()
main_view = MainView()
visualizer_id = -1
source_id = -1


def index(request):
    return render(request, 'index.html', {"sources": loader.sources, "visualizers": loader.visualizers})


def generate(request):
    visualizer_id = int(request.POST.get("visualizers"))
    source_id = int(request.POST.get("sources"))
    print(visualizer_id, source_id)
    vis = main_view.generate_main_view(source_id, visualizer_id)
    tree_view = TreeView(loader.get_loaded_graph(source_id))
    return render(request, 'index.html', {"sources": loader.sources, "visualizers": loader.visualizers,
                                          "visualization_html": main_view.generate_main_view(source_id, visualizer_id),
                                          "tree_view_html": tree_view.generate_tree_view()})


def search(request):
    search_text: str = str(request.POST.get("query"))
    print(search_text)
    pattern = r'^(\w+)\s*(==|>|>=|<|<=|!=)\s*(.+)$'
    match = re.match(pattern, search_text)
    tree_view = TreeView(loader.get_loaded_graph(source_id))
    if match:
        print("filter")
        return render(request, 'index.html', {"sources": loader.sources, "visualizers": loader.visualizers,"tree_view_html": tree_view.generate_tree_view(),
                                              "visualization_html": main_view.generate_from_filter_query(match.group(1), match.group(2), match.group(3))})
    else:
        return render(request, 'index.html', {"sources": loader.sources, "visualizers": loader.visualizers,"tree_view_html": tree_view.generate_tree_view(),
                                              "visualization_html": main_view.generate_from_search_query(search_text)})


def clear_filters(request):
    tree_view = TreeView(loader.get_loaded_graph(source_id))
    return render(request, 'index.html', {"sources": loader.sources, "visualizers": loader.visualizers,
                                          "visualization_html": main_view.clear_filters(), "tree_view_html": tree_view.generate_tree_view()})
