    # 주문기능 구현, 주문기록 저장
from django.shortcuts import render, redirect, get_object_or_404
from cart.models import CartItem
from orders.models import Order, OrderItem
from product.models import Product
from cart.models import Cart
from django.db.models import Sum

def order_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        # 장바구니에 상품을 추가하거나 업데이트
        cart_item, created = CartItem.objects.get_or_create(cart=cart, menu=product)
        cart_item.quantity += quantity
        cart_item.save()
        # 장바구니에 상품을 추가한 후에 메시지를 추가
        # 주문 후에는 장바구니 페이지로 이동
        return redirect('orders:order_product', product_id=product_id)
    # GET 요청인 경우에는 주문 페이지를 렌더링
    return render(request, 'orders/order.html', {'product': product})


from decimal import Decimal

def order_history(request):
    orders = Order.objects.all()
    for order in orders:
        for item in order.order_items.all():
            item.total_price = item.menu.price * item.quantity

    context = {
        'orders': orders,
        
    }
    return render(request, 'orders/order_history.html', context)
