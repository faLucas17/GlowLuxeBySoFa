from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('compte/', include('accounts.urls')),
    path('boutique/', include('products.urls')),
    path('panier/', include('cart.urls')),
    path('commandes/', include('orders.urls')),
    path('paiement/', include('payments.urls')),
    path('avis/', include('reviews.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)