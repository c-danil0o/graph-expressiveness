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
from core.src.use_cases.tree_view import TreeView

loader = Loader()
loader.init()
main_view = MainView()
visualizer_id = -1
source_id = -1
plugin_config: dict = {}
workspace_id = 1


def index(request):
    return render(request, 'index.html', {"sources": loader.sources, "visualizers": loader.visualizers})


def config(request):
    global visualizer_id, source_id, workspace_id, plugin_config
    visualizer_id = int(request.POST.get("visualizers"))
    source_id = int(request.POST.get("sources"))
    print(visualizer_id, source_id)
    if 'show' in request.POST:
        if loader.is_graph_loaded(source_id, plugin_config):
            #if main_view.is_workspace_loaded(workspace_id):
            return render_new_graph(request)

    return render(request, 'index.html',
                  {"sources": loader.sources, "visualizers": loader.visualizers, "modal_opened": True,
                   "settings": loader.get_settings(source_id), "source_id": source_id, "visualizer_id": visualizer_id})


def generate(request):
    global visualizer_id, source_id, plugin_config, workspace_id
    plugin_settings = loader.get_settings(source_id)
    plugin_config = {}
    for setting in plugin_settings:
        try:
            plugin_config[setting.key] = setting.data_type(request.POST.get(setting.key))
        except Exception as e:
            print(e)
            return render(request, 'index.html',
                          {"sources": loader.sources, "visualizers": loader.visualizers, "modal_opened": True,
                           "modal_error": True,
                           "settings": plugin_settings, "source_id": source_id, "visualizer_id": visualizer_id})
    loader.load_graph(source_id, plugin_config)
    return render_new_graph(request)


def search(request):
    global plugin_config, workspace_id, visualizer_id, source_id
    search_text: str = str(request.POST.get("query"))
    print(search_text)
    pattern = r'^(\w+)\s*(==|>|>=|<|<=|!=)\s*(.+)$'
    match = re.match(pattern, search_text)
    if match:
        main_view_html = main_view.generate_from_filter_query(match.group(1), match.group(2), match.group(3),
                                                              workspace_id)
        tree_view = TreeView(loader.get_loaded_graph(source_id, plugin_config))
        return render(request, 'index.html', {"sources": loader.sources, "visualizers": loader.visualizers,
                                              "tree_view_html": tree_view.generate_tree_view(),
                                              "visualization_html": main_view_html, "source_id": source_id,
                                              "visualizer_id": visualizer_id})
    else:
        main_view_html = main_view.generate_from_search_query(search_text, workspace_id)
        tree_view = TreeView(loader.get_loaded_graph(source_id, plugin_config))
        return render(request, 'index.html', {"sources": loader.sources, "visualizers": loader.visualizers,
                                              "tree_view_html": tree_view.generate_tree_view(),
                                              "visualization_html": main_view_html, "source_id": source_id,
                                              "visualizer_id": visualizer_id})


def clear_filters(request):
    main_view_html = main_view.clear_filters(workspace_id)
    tree_view = TreeView(loader.get_loaded_graph(source_id, plugin_config))
    return render(request, 'index.html', {"sources": loader.sources, "visualizers": loader.visualizers,
                                          "visualization_html": main_view_html,
                                          "tree_view_html": tree_view.generate_tree_view(), "source_id": source_id,
                                          "visualizer_id": visualizer_id})


def set_workspace(request, number: int):
    global workspace_id
    workspace_id = number
    if main_view.is_workspace_loaded(workspace_id):
        return render_existing_graph(request)
    else:
        return index(request)


def render_existing_graph(request):
    tree_view = TreeView(loader.get_loaded_graph(source_id, plugin_config))
    return render(request, 'index.html', {"sources": loader.sources, "visualizers": loader.visualizers,
                                          "visualization_html": main_view.render_workspace_graph(workspace_id),
                                          "tree_view_html": tree_view.generate_tree_view(), "source_id": main_view.get_workspace_source(workspace_id),
                                          "visualizer_id": main_view.get_workspace_visualizer(workspace_id)})


def render_new_graph(request):
    global source_id, visualizer_id, plugin_config
    tree_view = TreeView(loader.get_loaded_graph(source_id, plugin_config))
    return render(request, 'index.html', {"sources": loader.sources, "visualizers": loader.visualizers,
                                          "visualization_html": main_view.generate_main_view(source_id, visualizer_id,
                                                                                             plugin_config,
                                                                                             workspace_id),
                                          "tree_view_html": tree_view.generate_tree_view(), "source_id": source_id,
                                          "visualizer_id": visualizer_id})
