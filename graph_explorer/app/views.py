from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
import sys

# sys.path.append(r'C:\Users\Vladimir\Desktop\prog\5semestar\sok\projekat\graph-expressiveness')
sys.path.append(r'C:\Users\Aleksa\Desktop\sok-project\graph-expressiveness')
from core.src.use_cases import load_plugins

# from plugin.visualizer import SimpleVisualizer
#

a = {'blocks_num': 10, 'graph_name': 'asd', 'latest_block': -1, 'depth': 2}


def test(request):
    load_plugins.load_plugins()
    sources = load_plugins.get_source_plugins()
    visualizers = load_plugins.get_visualizer_plugins()
    graph = sources[0].load(a)
    visualization_html = visualizers[0].show(graph)
    # print(graph)
    return render(request, 'index.html',
                  {"sources": sources, "visualizers": visualizers, "visualization_html": visualization_html})
# def simple_visualizer_test():
#     visualizer = SimpleVisualizer()
#     generated_html = visualizer.show()
#     return HttpResponse(generated_html)
