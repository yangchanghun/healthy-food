from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart
from orders.models import Order, OrderItem
from django.contrib.auth.decorators import login_required


def cart_detail(request):
    cart = Cart.objects.get_or_create(user=request.user)[0]
    return render(request, 'cart/cart.html', {'cart': cart})


from django.utils import timezone

def cart_checkout(request):
    cart = Cart.objects.get_or_create(user=request.user)[0]
    # 주문을 생성하고 카트에 있는 항목을 주문으로 이동
    order = Order.objects.create(user=request.user, created_at=timezone.now())
    for item in cart.cart_items.all():
        OrderItem.objects.create(order=order, menu=item.menu, quantity=item.quantity)
    cart.items.clear()
    return redirect('orders:order_history')
