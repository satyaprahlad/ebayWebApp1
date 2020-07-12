from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [

    path('hi', views.hi, name='home-page' ),
    path('bye',views.bye, name='bye-page'),
    path('getSellerData',views.sellerSearch, name='sellerSearch1'),
    path('',views.homePage, name='sellerInput'),
    path('googlescrape', views.googlescrape,name='googlescrape')
]
