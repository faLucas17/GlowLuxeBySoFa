import requests
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Cart, CartItem
from products.models import Product
from django.contrib import messages
import urllib.parse


def _get_cart(request):
    if not request.session.session_key:
        request.session.create()
    
    try:
        cart = Cart.objects.get(session_key=request.session.session_key)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(session_key=request.session.session_key)
    except Cart.MultipleObjectsReturned:
        # Gérer le cas où il y a plusieurs paniers
        carts = Cart.objects.filter(session_key=request.session.session_key)
        cart = carts.first()
        # Supprimer les doublons
        for duplicate_cart in carts[1:]:
            duplicate_cart.delete()
    
    return cart

def cart_detail(request):
    cart = _get_cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})

def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        size = request.POST.get('size')
        color = request.POST.get('color')
        quantity = int(request.POST.get('quantity', 1))
        
        cart = _get_cart(request)
        
        # Vérifier si l'article existe déjà
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            size=size,
            color=color,
            defaults={'quantity': quantity, 'price': product.current_price}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        messages.success(request, f"{product.name} ajouté au panier!")
        return redirect('product_detail', category_slug=product.category.slug, product_slug=product.slug)
    
    return redirect('product_list')

def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart=_get_cart(request))
    cart_item.delete()
    return redirect('cart_detail')

def send_whatsapp_notification(customer_name, phone_number, cart_total):
    """
    Envoie une notification WhatsApp au client
    """
    print(f"🔔 NOTIFICATION POUR {customer_name}")
    print(f"💰 Total: {cart_total} FCFA")
    print("Message qui serait envoyé:")
    print("-" * 40)
    
    message = f"Bonjour {customer_name},\n\n"
    message += "Nous avons bien reçu votre commande GlowLuxe.\n"
    message += f"Montant total : {cart_total} FCFA\n\n"
    message += "Notre équipe vous contactera très prochainement pour confirmer la livraison et le paiement.\n\n"
    message += "Merci de votre confiance !\n"
    message += "L'équipe GlowLuxe"
    
    print(message)
    print("-" * 40)
    
    return True  

def whatsapp_checkout(request):
    cart = _get_cart(request)
    
    if not cart.items.exists():
        messages.warning(request, "Votre panier est vide!")
        return redirect('cart_detail')
    
    # Construction du message WhatsApp
    message = " *NOUVELLE COMMANDE GlowLuxe* \n"
    message += "═══════════════════════════\n\n"
    message += "*DÉTAILS DE LA COMMANDE*\n"
    message += "────────────────────────\n\n"

    for item in cart.items.all():
        message += f" *{item.product.name}*\n"
        message += f"   Taille: {item.size}\n"
        message += f"   Couleur: {item.color}\n"
        message += f"   Prix: {item.price} FCFA\n"
        message += f"   Qté: {item.quantity}\n"
        message += f"   ➤ Sous-total: {item.total_price} FCFA\n\n"

    message += "═══════════════════════════\n"
    message += f" *TOTAL: {cart.total_price} FCFA* \n"
    message += "═══════════════════════════\n\n"
    message += "*LIVRAISON*\n"
    message += "──────────\n"
    message += "Veuillez indiquer:\n"
    message += "✓ Nom complet\n"
    message += "✓ Adresse\n"
    message += "✓ Téléphone\n"
    message += "✓ Paiement (Wave/Orange Money)\n\n"
    message += " *Envoyez ce message pour confirmer*"
    
    # Encodage pour URL WhatsApp
    encoded_message = urllib.parse.quote(message)
    
    # Numéro WhatsApp 
    whatsapp_number = "221778228460"
    
    whatsapp_url = f"https://wa.me/{whatsapp_number}?text={encoded_message}"
    
    return redirect(whatsapp_url)