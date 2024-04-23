from django.urls import path
from follow.views import *

app_name = 'follow'
urlpatterns = [
    path('', index, name='index'),
    path('follow/', following, name='follow'),
    path('seller/', is_seller, name='is_seller')
]
