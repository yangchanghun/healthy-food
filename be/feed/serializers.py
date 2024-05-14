from rest_framework import serializers
from .models import Content, Like, FeedImage, Comment
from product.models import Product
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ContentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    likes = UserSerializer(read_only=True, many=True)
    product = ProductSerializer(read_only=True)
    seller = UserSerializer(read_only=True)
    feed_images = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='image'
    )
    
    class Meta:
        model = Content
        fields = ['id', 'user', 'body_text', 'title', 'created_at', 'updated_at', 'likes', 'content_type', 'product', 'seller', 'feed_images']

class LikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    content = serializers.PrimaryKeyRelatedField(queryset=Content.objects.all())

    class Meta:
        model = Like
        fields = ['user', 'content']

class FeedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedImage
        fields = ['content', 'image']
        
class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    likes = UserSerializer(read_only=True, many=True)
    
    class Meta:
        model = Comment
        fields = ['content', 'user', 'comment_text', 'created_at', 'updated_at', 'likes']
