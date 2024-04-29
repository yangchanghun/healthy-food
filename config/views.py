from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, ProfileForm
from django.http import JsonResponse
from django.contrib.auth.models import User
from userprofile.models import Profile

def index(request):
    return render(request, 'home.html')

def login(request) :
    return render(request, 'registration/login.html')

def register_user(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            # 사용자 모델 저장
            new_user = user_form.save()
            new_profile = profile_form.save(commit=False)
            new_profile.user = new_user  # User 모델과 Profile 모델 연결
            new_profile.save()  # 프로필 모델 DB에 저장
            return redirect('register_done')  # 가입 완료 페이지로 리다이렉트
    else:
        user_form = CustomUserCreationForm()
        profile_form = ProfileForm()

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'registration/register.html', context)


class UserCreateDoneTV(TemplateView):
    template_name='registration/register_done.html'


def check_duplicate(request):
    field_type = request.GET.get('field_type')
    field_value = request.GET.get('field_value')

    if field_type == 'email':
        is_taken = User.objects.filter(email=field_value).exists()
    elif field_type == 'nickname':
        # 닉네임 중복 검사를 Profile 모델을 통해 수행
        is_taken = Profile.objects.filter(nickname=field_value).exists()
    else:
        is_taken = False

    data = {
        'is_taken': is_taken
    }
    return JsonResponse(data)