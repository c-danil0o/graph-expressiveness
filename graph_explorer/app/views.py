from django.shortcuts import render
import os
import sys

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.append(BASE_DIR)

from core.src.use_cases.loader import Loader

loader = Loader()
loader.init()


def index(request):
    print(loader.sources)
    return render(request, 'index.html', {"sources": loader.sources, "visualizers": loader.visualizers})
