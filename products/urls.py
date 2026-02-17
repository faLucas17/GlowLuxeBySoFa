from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('categorie/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('produit/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
]