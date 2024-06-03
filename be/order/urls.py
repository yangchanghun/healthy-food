from django.urls import path
from . import api

# config path('api/orders/', include('order.urls')),

urlpatterns = [
    path('create/', api.create_order, name='create_order'),
    # path('', api.order_list, name='order_list'),
    # path('<uuid:pk>/', api.order_detail, name='order_detail'),
]
