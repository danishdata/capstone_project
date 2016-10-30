from django.conf.urls import patterns, include, url
from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^scatter/', views.scatter, name = 'scatter'),
    url(r'^wordcloud/', views.wordcloud, name = 'wordcloud'),
    url(r'^data/', views.data, name = 'data'),
]