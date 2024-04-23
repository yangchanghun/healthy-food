from django.urls import path
from . import views
app_name = 'orders'

urlpatterns = [
    path('<int:product_id>/', views.order_product, name='order_product'),
    path('order_history/',views.order_history,name='order_history')

]