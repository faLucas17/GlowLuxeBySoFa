from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from products.models import Product

def home(request):
    featured_products = Product.objects.filter(featured=True, active=True)[:8]
    return render(request, 'core/home.html', {'featured_products': featured_products})

def about(request):
    return render(request, 'core/about.html')

def favoris_view(request):
    # Récupérer les favoris depuis le localStorage via le template
    return render(request, 'core/favoris.html')