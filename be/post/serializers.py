from rest_framework import serializers

from account.serializers import UserSerializer

from .models import Post, Comment, Trend, PostAttachment


class PostAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostAttachment
        fields = ('id', 'get_image',)


# post list
class PostSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    attachments = PostAttachmentSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = ('id', 'body', 'likes_count', 'created_by', 'created_at_formatted', 'attachments')

# 댓글
class CommentSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'body', 'created_by', 'created_at_formatted',)

# post detail
class PostDetailSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    comments = CommentSerializer(read_only=True, many=True)
    comments_count = serializers.IntegerField(read_only=True) 
    attachments = PostAttachmentSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = ('id', 'body', 'likes_count', 'created_by', 'created_at_formatted', 'comments', 'comments_count', 'attachments')
        
# 우측 trend
class TrendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trend
        fields = ('id', 'hashtag', 'occurences',)