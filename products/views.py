from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Category, Product

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.filter(active=True)
    products = Product.objects.filter(active=True)
    
    # 🔍 RECHERCHE SIMPLE
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        ).distinct()
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug, active=True)
        products = products.filter(category=category)
    
    return render(request, 'products/product_list.html', {
        'category': category,
        'categories': categories,
        'products': products,
    })

def product_detail(request, category_slug, product_slug):
    product = get_object_or_404(
        Product, 
        slug=product_slug, 
        category__slug=category_slug,
        active=True
    )
    
    sizes = [size.strip() for size in product.sizes.split(',')] if product.sizes else ['M']
    colors = product.colors if product.colors else {'noir': 'Noir'}
    
    return render(request, 'products/product_detail.html', {
        'product': product,
        'sizes': sizes,
        'colors': colors
    })