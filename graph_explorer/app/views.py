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

loader = Loader()
loader.init()
main_view = MainView()


def index(request):
    return render(request, 'index.html', {"sources": loader.sources, "visualizers": loader.visualizers})


def generate(request):
    visualizer_id = int(request.POST.get("visualizers"))
    source_id = int(request.POST.get("sources"))
    print(visualizer_id, source_id)
    return render(request, 'index.html', {"sources": loader.sources, "visualizers": loader.visualizers,
                                          "visualization_html": main_view.generate_main_view(source_id, visualizer_id)})


def search(request):
    search_text: str = str(request.POST.get("query"))
    print(search_text)
    pattern = r'^(\w+)\s*(==|>|>=|<|<=|!=)\s*(.+)$'
    match = re.match(pattern, search_text)
    if match:
        print("filter")
        return render(request, 'index.html', {"sources": loader.sources, "visualizers": loader.visualizers,
                                              "visualization_html": main_view.generate_from_filter_query(match.group(1), match.group(2), match.group(3))})
    else:
        return render(request, 'index.html', {"sources": loader.sources, "visualizers": loader.visualizers,
                                              "visualization_html": main_view.generate_from_search_query(search_text)})


def clear_filters(request):
    return render(request, 'index.html', {"sources": loader.sources, "visualizers": loader.visualizers,
                                          "visualization_html": main_view.clear_filters()})