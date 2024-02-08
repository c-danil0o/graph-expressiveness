from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index_page'),
    path('config/', views.config, name='open_config'),
   # path('show/', views.show_graph, name='show_graph'),
    path('generate/', views.generate, name='generated_graph'),
    path('search/', views.search, name='search_graph'),
    path('clear/', views.clear_filters, name='clear_filters'),
    path('workspace/<int:number>/', views.workspace, name='workspace')
    # path('simple/', views.test, name='show_graph')
]
