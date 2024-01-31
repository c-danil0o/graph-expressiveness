from django.urls import path
from . import views

urlpatterns = [
    path('', views.test)
    #path('simple/', views.test, name='show_graph')
]