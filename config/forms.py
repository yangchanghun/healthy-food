from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from userprofile.models import Profile
from django.db import transaction


"""
여기에 정의된 form을 사용하면 email 필드 값이 email이 맞는지, 보안 등 이점이 있습니다

      html에서 불러오는 form이 이 코드입니다
        {{ user_form.as_p }}
        {{ profile_form.as_p }}
        
그런데 view에 정의해 주신 check_duplicate 함수는 사용하지 못하겠지요..
그래서 
        <!-- 프로필 이미지 업로드 필드 -->
        <div class="mb-3">
          <label for="{{ form.user_image.id_for_label }}" class="form-label">프로필 이미지</label>
          {% render_field form.user_image class="form-control" %}
        </div>
요런식으로 하나씩 form을 구성하신 것 같은데 이 방법도 좋습니다!
실제로 위에 코드를 사용하셔도 아마 작동이 될겁니다

**요약**
현재 form을 이용해서 구현을 해 놓았고
html에서 form을 다 구현해 받아야 하는 10개의 값을 다 받으면

        <!-- 유저네임 필드 -->
        <div class="mb-3">
          <label for="{{ form.username.id_for_label }}" class="form-label">유저네임</label>
          {% render_field form.username class="form-control" %}
        </div>
        
이와 같은 코드를 10번 반복해야 한다!

그러므로
check_duplicate를 이용하기 위해서 현재 파일에 있는 email, nickname을 form에서 제외시키고

저 두개의 필드만 html에서 직접 구현해 view의 함수로 검증하는 방식이 best

하지만 편한 방식을 택하시면 됩니다.
**요약 끝**
"""
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('user_image', 'nickname', 'phone_number', 'address', 'detailed_address', 'is_seller')

    def save(self, commit=True):
        profile = super().save(commit=commit)
        
        if self.cleaned_data['is_seller']:
            try:
                with transaction.atomic():
                    group = Group.objects.get(name='Sellers')
                    group.user_set.add(self.instance.user)
            except Group.DoesNotExist:
                pass

        return profile