# your_app_name/context_processors.py
from .cart import Cart

def cart_context(request):
    if 'cart_item' in request.session:
        cart = Cart(request)
        return {'cart': cart}
    else:
        return {'cart': None}
