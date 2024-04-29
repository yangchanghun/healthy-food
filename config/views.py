from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
from userprofile.models import Profile
from django.http import JsonResponse


def index(request):
    return render(request, 'home.html')

def login(request) :
    return render(request, 'registration/login.html')

class UserCreateView(CreateView):
    template_name = 'registration/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('register_done')
    
    # def save(self, commit=True):
    #     user = super(CustomUserCreationForm, self).save(commit=False)
    #     user.email = self.cleaned_data['email']
    #     if commit:
    #         user.save()

    #         # Profile 객체 생성 및 연결
    #         profile = Profile.objects.create(
    #             user=user,
    #             user_image=self.cleaned_data['user_image'],
    #             nickname=self.cleaned_data['nickname'],
    #             phone_number=self.cleaned_data['phone_number'],
    #             address=self.cleaned_data['address'],
    #             detailed_address=self.cleaned_data['detailed_address'],
    #             is_seller=self.cleaned_data['is_seller']
    #         )

    #     return user


class UserCreateDoneTV(TemplateView):
    template_name='registration/register_done.html'


def check_duplicate(request):
    field_type = request.GET.get('field_type')
    field_value = request.GET.get('field_value')

    if field_type == 'email':
        is_taken = User.objects.filter(email=field_value).exists()
    elif field_type == 'nickname':
        is_taken = User.objects.filter(username=field_value).exists()
    else:
        is_taken = False

    data = {
        'is_taken': is_taken
    }
    return JsonResponse(data)