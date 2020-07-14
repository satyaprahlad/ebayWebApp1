from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.hi, name='home-page' ),
    path('googlescrape', views.googlescrape,name='googlescrape')
]
