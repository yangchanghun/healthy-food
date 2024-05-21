from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .forms import SignupForm, ProfileForm
from .models import User

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
        message = 'error'

    return JsonResponse({'message': message})


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
        print(request.FILES)
        print(request.POST)

        form = ProfileForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()

        return JsonResponse({'message': 'information updated'})