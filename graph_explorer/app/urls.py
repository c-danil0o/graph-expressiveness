from django.urls import path
from . import views

urlpatterns = [
    path('', views.test)
   # path('simple/', views.simple_visualizer_test(), name='show_graph')
]