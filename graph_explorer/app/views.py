from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
import sys

# sys.path.append(r'C:\Users\Vladimir\Desktop\prog\5semestar\sok\projekat\graph-expressiveness')
sys.path.append(r'/home/dc/Code/SOK/graph_exp')
from core.src.use_cases import load_plugins

# from plugin.visualizer import SimpleVisualizer
#

a = {'blocks_num': 10, 'graph_name': 'asd', 'latest_block': -1}


def test(request):
    load_plugins.load_plugins()
    sources = load_plugins.get_source_plugins()
    visualizers = load_plugins.get_visualizer_plugins()
    visualization_html = visualizers[0].show(sources[0].load(a))

    return render(request, 'index.html',
                  {"sources": sources, "visualizers": visualizers, "visualization_html": visualization_html})
# def simple_visualizer_test():
#     visualizer = SimpleVisualizer()
#     generated_html = visualizer.show()
#     return HttpResponse(generated_html)
