from django.shortcuts import render
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy

def index(request):
    return render(request, 'home.html')

def login(request) :
    return render(request, 'registration/login.html')

def register(request):
    return render(request, 'registration/register.html')

class UserCreateView(CreateView):
    template_name='registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register_done')

class UserCreateDoneTV(TemplateView):
    template_name='registration/register_done.html'