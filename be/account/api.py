from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.contrib.auth.forms import PasswordChangeForm
from .forms import SignupForm, ProfileForm
from .models import User
from .serializers import UserSerializer

@api_view(['GET'])
def me(request):
    return JsonResponse({
        'id': request.user.id,
        'name': request.user.name,
        'email': request.user.email,
        'user_image': request.user.get_userimage(),
    })


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(request):
    data = request.data
    message = 'success'

    form = SignupForm({
        'email': data.get('email'),
        'name': data.get('name'),
        'password1': data.get('password1'),
        'password2': data.get('password2'),
    })

    if form.is_valid():
        form.save()

        # 이메일 확인 로직 추가
    else:
        message = form.errors.as_json()
        
    return JsonResponse({'message': message}, safe=False)


@api_view(['POST'])
def send_follow(request, pk):
    me = request.user
    you = User.objects.get(pk=pk)
    
    if me in you.followers.all(): 
        you.followers.remove(me)
        return JsonResponse({'message': 'unfollow'})
    else:
        you.followers.add(me)
        return JsonResponse({'message': 'follow'})


@api_view(['POST'])
def check_follow(request, pk):
    me = request.user
    you = User.objects.get(pk=pk)
    
    if me in you.followers.all(): 
        return JsonResponse({'isFollowing': True})
    else:
        return JsonResponse({'isFollowing': False})
    
@api_view(['POST'])
def editprofile(request):
    user = request.user
    name = request.data.get('name')
    
    if User.objects.exclude(id=user.id).filter(name=name).exists():
        return JsonResponse({'message': 'nickname already exists'})
    
    else:
        form = ProfileForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()

        serializer = UserSerializer(user)
        
        return JsonResponse({'message': 'information updated', 'user': serializer.data})
    
@api_view(['POST'])
def editpassword(request):
    user = request.user
    
    form = PasswordChangeForm(data=request.POST, user=user)

    if form.is_valid():
        form.save()

        return JsonResponse({'message': 'success'})
    else:
        return JsonResponse({'message': form.errors.as_json()}, safe=False)