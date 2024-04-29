from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from userprofile.models import Profile

class CustomUserCreationForm(UserCreationForm):
    nickname = forms.CharField(max_length=30)
    user_image = forms.ImageField()
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=15)
    address = forms.CharField(max_length=100)
    detailed_address = forms.CharField(max_length=100)
    is_seller = forms.BooleanField(required=False)

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
    
    class Meta:
        model = User
        fields = ('username', 'user_image', 'password1', 'password2', 'nickname', 'email', 'phone_number', 'address', 'detailed_address', 'is_seller')

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

            # Profile 객체 생성 및 연결
            profile = Profile.objects.create(
                user=user,
                user_image=self.cleaned_data['user_image'],
                nickname=self.cleaned_data['nickname'],
                phone_number=self.cleaned_data['phone_number'],
                address=self.cleaned_data['address'],
                detailed_address=self.cleaned_data['detailed_address'],
                is_seller=self.cleaned_data['is_seller']
            )

            # 사용자가 판매자로 등록되었는지 확인
            if self.cleaned_data['is_seller']:
                # 'Sellers' 그룹 가져오기, 없으면 생성
                group= Group.objects.get(name='Sellers')
                # 사용자를 'Sellers' 그룹에 추가
                group.user_set.add(user)

        return user