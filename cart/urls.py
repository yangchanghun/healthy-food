from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('checkout/', views.cart_checkout, name='cart_checkout'),
]