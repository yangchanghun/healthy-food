from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    nickname = forms.CharField(max_length=30)
    user_image = forms.ImageField()
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=15)
    address = forms.CharField(max_length=100)
    detailed_address = forms.CharField(max_length=100)
    is_seller = forms.BooleanField(required=False)
    
    class Meta:
        model = User
        fields = ('username', 'user_image', 'password1', 'password2', 'nickname', 'email', 'phone_number', 'address', 'detailed_address', 'is_seller')



    # def save(self, commit=True):
    #     user = super(CustomUserCreationForm, self).save(commit=False)
    #     user.email = self.cleaned_data['email']
    #     user.profile.user_image = self.cleaned_data['user_image']
    #     user.profile.nickname = self.cleaned_data['nickname']
    #     user.profile.phone_number = self.cleaned_data['phone_number']
    #     user.profile.address = self.cleaned_data['address']
    #     user.profile.detailed_address = self.cleaned_data['detailed_address']
    #     user.profile.is_seller = self.cleaned_data['is_seller']
    #     if commit:
    #         user.save()
    #     return user