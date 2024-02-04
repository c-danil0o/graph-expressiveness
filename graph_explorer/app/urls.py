from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index_page'),
    path('generate/', views.generate, name='generated_graph'),
    path('search/', views.search, name='search_graph'),
    path('clear/', views.clear_filters, name='clear_filters')
    # path('simple/', views.test, name='show_graph')
]
