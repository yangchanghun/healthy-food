from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.http import HttpResponse
from .models import *
from django.contrib.auth.decorators import login_required
from itertools import groupby
from operator import attrgetter
from cart.cart import Cart

@login_required
def create_order(request):
    # POST 요청인지 확인
    if request.method == 'POST':
        cart = Cart(request)
        user = request.user
        
        # 장바구니가 비어있는지 확인
        if not cart:
            return HttpResponse('장바구니가 비어 있습니다.', status=400)
        
        order = Order.objects.create(
            user=user,
        )
        
        for item in cart:  
            OrderItem.objects.create(
                order=order,
                product=item['product'],  
                quantity=item['quantity'],
            )

        # 장바구니 비우기 (주문이 완료된 후)
        cart.clear()
        
        return redirect('orders:order_detail', order_id=order.id) 
        
    else:
        # GET 요청 시 에러 메시지 반환
        return HttpResponse('잘못된 요청입니다.', status=405)


@login_required
def order_history(request):
    user = request.user
    orders = Order.objects.filter(user=user) 
    orders_with_total = []
    for order in orders:
        total_price = order.get_total_price()  # 이전에 정의한 get_total_price 메소드 사용
        orders_with_total.append((order, total_price))
    
    # 템플릿에 orders_with_total 리스트를 전달
    return render(request, 'orders/order_history.html', {'orders_with_total': orders_with_total})

@login_required
def sales_history(request):
    # order_id에 따라 그룹화하기 위해 정렬
    sold_items = OrderItem.objects.filter(product__seller=request.user).order_by('order_id').select_related('order', 'product')
    # 각 그룹은 동일한 order_id를 가진 OrderItem들의 리스트
    grouped_sold_items = [list(group) for key, group in groupby(sold_items, key=attrgetter('order_id'))]
    groups_with_total = []
    for group in grouped_sold_items:
        total_price = 0
        for item in group:
            item_total_price = item.get_total_item_price()  # 이전에 정의한 get_total_item_price 메소드 사용
            total_price += item_total_price
        groups_with_total.append((group, total_price))
    return render(request, 'orders/sales_history.html', {'groups_with_total': groups_with_total})


@login_required
def order_detail(request, order_id):
    # 주문 ID를 사용하여 주문 정보를 가져옴
    order = get_object_or_404(Order, id=order_id)

    # 해당 주문에 속한 모든 상품 아이템들을 가져옴
    order_items = OrderItem.objects.filter(order=order)

    # 주문 정보와 상품 아이템들을 템플릿에 전달하여 주문 상세 페이지를 렌더링
    return render(request, 'orders/order_detail.html', {'order': order, 'order_items': order_items})

