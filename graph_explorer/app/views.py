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


def index(request):
    return render(request, 'index.html', {"sources": loader.sources, "visualizers": loader.visualizers})


def generate(request):
    visualizer_id = int(request.POST.get("visualizers"))
    source_id = int(request.POST.get("sources"))
    vis = main_view.generate_main_view(source_id, visualizer_id)
    tree_view = TreeView(loader, source_id)
    tree_view.generate_tree_view()
    return render(request, 'index.html', {"sources": loader.sources, "visualizers": loader.visualizers,
                                          "visualization_html": vis})
