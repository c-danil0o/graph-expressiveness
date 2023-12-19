from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from core.src.use_cases import load_plugins


# from plugin.visualizer import SimpleVisualizer
#
def test(request):
    load_plugins.load_plugins()
    sources = load_plugins.get_source_plugins()
    visualizers = load_plugins.get_visualizer_plugins()
    return render(request, 'index.html', {"sources": sources, "visualizers": visualizers})
# def simple_visualizer_test():
#     visualizer = SimpleVisualizer()
#     generated_html = visualizer.show()
#     return HttpResponse(generated_html)
