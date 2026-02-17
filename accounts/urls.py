from django.urls import path
from . import views

urlpatterns = [
    path('inscription/', views.register, name='register'),
    path('connexion/', views.login_view, name='login'),
    path('deconnexion/', views.logout_view, name='logout'),
    path('profil/', views.profile, name='profile'),
]