from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from .models import Follow
from django.contrib.auth.models import User, Group
from django.views import generic
from product.models import Product
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

def index(request):
    User = get_user_model()
    users = User.objects.all()
    return render(request, 'follow/index.html', {'users': users})

class UserDV(generic.DetailView):
    model = User
    template_name = 'follow/user_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 사용자가 판매자 그룹에 속해있는지 확인
        context['is_seller'] = self.request.user.groups.filter(name='Sellers').exists()
        return context

@login_required
def following(request):
    if request.method == 'POST':
        # 팔로우할 사람 선택
        user_to_follow_id = request.POST.get('user_id')
        user_to_follow = get_user_model().objects.get(pk=user_to_follow_id)
        # 현재 유저
        follower = request.user
        # 이미 팔로우하고 있는지 확인
        if not Follow.objects.filter(follower=follower, following=user_to_follow).exists():
            Follow.objects.create(follower=follower, following=user_to_follow)
        return HttpResponseRedirect(reverse('follow:index'))
    

class SellerProductLV(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    model = Product
    template_name = 'follow/seller_page.html'
    context_object_name = 'products'
    login_url = reverse_lazy('follow:index')

    def test_func(self): # 현재 유저가 그룹에 속하면 접속, 아니면 403 에러
        # 현재 로그인한 사용자가 Sellers 그룹에 속해 있는지 확인
        return self.request.user.groups.filter(name='Sellers').exists()
    
    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user).prefetch_related('images')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_images = {}
        for product in context['products']:
            product_images[product.id] = product.images.first().image_url if product.images.exists() else None
        context['product_images'] = product_images

        return context