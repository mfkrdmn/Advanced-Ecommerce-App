from django import views
from django.urls import path
from . import views

urlpatterns = [
    path('store', views.store, name = 'store'),
    path('store/<slug:category_slug>/', views.store, name = 'products_by_category'),
]



