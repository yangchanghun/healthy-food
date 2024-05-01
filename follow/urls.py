from django.urls import path
from follow.views import *

app_name = 'follow'
urlpatterns = [
    path('', index, name='index'),
    path('<int:pk>/', UserDV.as_view(), name='user_detail'),   
    path('follow_unfollow/<int:user_id>/', follow_unfollow, name='follow_unfollow'),
    path('seller/', SellerProductLV.as_view(), name='is_seller')
]
