from django.shortcuts import render

# À implémenter plus tard pour Stripe
def payment_process(request):
    return render(request, 'payments/process.html')