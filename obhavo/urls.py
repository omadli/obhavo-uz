from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.main, name="home"),
    path('search/', views.search, name='search'),
    path('city/<str:city_name>/', views.main, name="city"),
]
