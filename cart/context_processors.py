# cart/context_processors.py
from .models import Cart

def cart_items_count(request):
    cart_items_count = 0
    if request.session.session_key:
        try:
            cart = Cart.objects.get(session_key=request.session.session_key)
            cart_items_count = cart.items.count()
        except Cart.DoesNotExist:
            # Pas de panier pour cette session
            pass
        except Cart.MultipleObjectsReturned:
            # Gérer le cas de multiples paniers
            carts = Cart.objects.filter(session_key=request.session.session_key)
            cart_items_count = carts.first().items.count()
            # Optionnel: nettoyer les doublons
            for cart in carts[1:]:
                cart.delete()
    
    return {'cart_items_count': cart_items_count}