from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Follow
from django.contrib.auth.models import User, Group

def index(request):
    User = get_user_model()
    users = User.objects.all()
    return render(request, 'follow/index.html', {'users': users})

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
    

def is_seller(request):
    # 현재 사용자가 Sellers 그룹에 속해 있는지 확인
    if request.user.groups.filter(name='Sellers').exists():
        # 속해 있다면 seller_page.html로 이동
        return render(request, 'follow/seller_page.html')
    else:
        return HttpResponseRedirect(reverse('follow:index'))

