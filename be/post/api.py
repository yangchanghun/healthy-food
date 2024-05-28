from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count

from account.models import User
from account.serializers import UserSerializer
from .serializers import PostSerializer, PostDetailSerializer, CommentSerializer, TrendSerializer
from .models import Post, Like, Comment, Trend
from .forms import PostForm, AttachmentForm

from rest_framework.decorators import api_view, authentication_classes, permission_classes


@api_view(['GET'])
# @permission_classes([])
def post_list(request):
    posts = Post.objects.all()
    
    trend = request.GET.get('trend', '')

    if trend:
        posts = posts.filter(body__icontains='#' + trend)
        
    serializer = PostSerializer(posts, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def post_detail(request, pk):
    post = Post.objects.annotate(comments_count=Count('comments')).get(pk=pk)

    return JsonResponse({
        'post': PostDetailSerializer(post).data
    })


@api_view(['GET'])
def post_list_profile(request, id):
    user = User.objects.annotate(posts_count=Count('posts')).get(pk=id)
    posts = Post.objects.filter(created_by_id=id)

    posts_serializer = PostSerializer(posts, many=True)
    user_serializer = UserSerializer(user)

    return JsonResponse({
        'posts': posts_serializer.data,
        'user': user_serializer.data
    }, safe=False)


@api_view(['POST'])
def post_create(request):
    form = PostForm(request.POST)
    attachment_form = AttachmentForm(request.POST, request.FILES)
    
    if attachment_form.is_valid():
        attachment = attachment_form.save(commit=False)
        attachment.created_by = request.user
        attachment.save()
    
    if form.is_valid() and attachment_form.is_valid():
        post = form.save(commit=False)
        post.created_by = request.user
        post.save()
        post.attachments.add(attachment)
        
        serializer = PostSerializer(post)

        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'add somehting here later!...'})
    
@api_view(['POST'])
def post_like(request, pk):   
    post = Post.objects.get(pk=pk)

    if not post.likes.filter(created_by=request.user):
        like = Like.objects.create(created_by=request.user)
        post = Post.objects.get(pk=pk)
        post.likes_count = post.likes_count + 1
        post.likes.add(like)
        post.save()

        return JsonResponse({'message': 'like created'})
    else:
        like = Like.objects.filter(created_by=request.user, post=pk).first()
        post = Post.objects.get(pk=pk)
        post.likes.remove(like)
        post.likes_count = post.likes_count - 1
        post.save()
        like.delete()

        return JsonResponse({'message': 'like canceled'})
    

@api_view(['POST'])
def check_liked(request, pk):
    post = Post.objects.get(pk=pk)    
    me = request.user
    is_liked = Like.objects.filter(created_by=me, post=post).exists()
    return JsonResponse({'isLiked': is_liked})
    
    
@api_view(['POST'])
def post_create_comment(request, pk):
    comment = Comment.objects.create(body=request.data.get('body'), created_by=request.user, post=Post.objects.get(pk=pk))
    serializer = CommentSerializer(comment)

    return JsonResponse(serializer.data, safe=False)


@api_view(['DELETE'])
def post_delete(request, pk):
    post = Post.objects.filter(created_by=request.user).get(pk=pk)
    post.delete()

    return JsonResponse({'message': 'post deleted'})

@api_view(['GET'])
def get_trends(request):
    serializer = TrendSerializer(Trend.objects.all(), many=True)

    return JsonResponse(serializer.data, safe=False)