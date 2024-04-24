from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.models import Group
from .forms import CustomUserCreationForm

def index(request):
    return render(request, 'home.html')

def login(request) :
    return render(request, 'registration/login.html')

class UserCreateView(CreateView):
    template_name = 'registration/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('register_done')

    def form_valid(self, form):
        self.object = form.save()
        if form.cleaned_data.get('is_seller'):
            group = Group.objects.get(name='Sellers')
            self.object.groups.add(group)
        return redirect(self.get_success_url())

class UserCreateDoneTV(TemplateView):
    template_name='registration/register_done.html'