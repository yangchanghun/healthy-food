from django.contrib import admin
from django.urls import path
from . import views
from .views import like_content, PostEditView, post_delete

app_name='feed'
urlpatterns = [
    path('', views.ContentListView.as_view(), name='index'),
    path('create/post/', views.ContentCreateView.as_view(), name='post-create'),
    path('create/review/', views.ReviewCreateView.as_view(), name='review-create'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),

    path('like-content/<int:content_id>/', like_content, name='like-content'),
    path('comment/create/<int:pk>/', views.comments_create, name='comments_create'), #추가1
    path('comment/delete/<int:pk>/', views.comments_delete, name='comments_delete'), #추가 2
    path('user/<int:pk>/', views.view_user, name='view_user'),

    path('post/edit/<int:pk>/', PostEditView.as_view(), name='post_edit'),
    path('post/delete/<int:pk>/', post_delete, name='post_delete'),
    ]