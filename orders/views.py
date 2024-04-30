from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from .models import *
from django.contrib.auth.decorators import login_required

@login_required
def create_order(request):
    # POST 요청인지 확인
    if request.method == 'POST':
        cart = request.session[settings.CART_ID]
        user = request.user
        
        # 장바구니가 비어있는지 확인
        if not cart:
            return HttpResponse('장바구니가 비어 있습니다.', status=400)
        
        order = Order.objects.create(
            created_at = models.DateTimeField(auto_now_add=True),
            user = user,
            )
        
        for item_id, comp in cart.items():
            # 여기서 item_id는 메뉴의 ID, quantity는 주문 개수
            # 예제 코드에서는 메뉴 모델을 Menu라고 가정
            # menu_item = Menu.objects.get(id=item_id) # 메뉴 객체 조회
            quantity = comp['quantity']
            OrderItem.objects.create(
                order_id=order.pk,
                menu_id=item_id,
                quantity=quantity
            )

        # 장바구니 비우기 (주문이 완료된 후)
        cart.clear()
        
        return redirect('orders:order_detail', order_id=order.id) 
        
    return render(request, 'orders/create_order.html', {'cart': cart})
