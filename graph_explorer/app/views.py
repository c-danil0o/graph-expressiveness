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
    return render(request, 'index.html', {"sources": loader.sources, "visualizers": loader.visualizers, "visualization_html": main_view.generate_main_view(0, 0)})
