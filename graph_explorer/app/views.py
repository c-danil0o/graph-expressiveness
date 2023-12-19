from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render

from plugin.visualizer import SimpleVisualizer

def test(request):
    return render(request, 'index.html', {"sources": ["Ethereum", "Twitter"], "visualizers": ["Simple", "Block"]})
def simple_visualizer_test():
    visualizer = SimpleVisualizer()
    generated_html = visualizer.show()
    return HttpResponse(generated_html)