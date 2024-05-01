from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .models import Follow
from django.contrib.auth.models import User
from django.views import generic
from product.models import Product
from feed.models import Content
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
        context['posts'] = Content.objects.filter(user=self.request.user, content_type='post')
        context['reviews'] = Content.objects.filter(user=self.request.user, content_type='review')
        context['userprofile'] = self.request.user.profile
        return context

# 팔로우/언팔로우 처리
@login_required
def follow_unfollow(request, user_id):
    other_user = get_object_or_404(get_user_model(), pk=user_id)
    follow, created = Follow.objects.get_or_create(follower=request.user, following=other_user)
    # 이미 팔로우되어 있다면, 기록을 삭제(언팔로우)
    if not created:
        follow.delete()
    return redirect('feed:view_user', pk=user_id)

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
        context['reviews'] = Content.objects.filter(seller=self.request.user, content_type='review')

        return context