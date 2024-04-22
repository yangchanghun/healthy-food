from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Content(models.Model):
    user = models.ForeignKey(User, related_name='contents', on_delete=models.CASCADE)
    body_text = models.TextField(blank=True)
    likes = models.IntegerField()
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class FeedImage(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='feed_images')
    image_url = models.URLField()
    