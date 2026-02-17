from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('ajouter/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('supprimer/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('whatsapp-checkout/', views.whatsapp_checkout, name='whatsapp_checkout'),
]