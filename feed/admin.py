from django.contrib import admin
from .models import Content, FeedImage, Comment
# Register your models here.

admin.site.register(Content)
admin.site.register(FeedImage)
admin.site.register(Comment)