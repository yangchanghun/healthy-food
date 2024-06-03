from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.http import JsonResponse
from .models import Order, OrderItem

@api_view(['POST'])
def create_order(request):
    user_data = request.data.get('user')
    order_data = request.data.get('order')
    print(user_data)
    print(order_data)
    
    return JsonResponse({'message': '주문이 완료되었습니다.'}, status=201)
