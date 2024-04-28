from django.shortcuts import render, get_object_or_404
from .models import Content, FeedImage
from django.contrib.auth.models import User
from userprofile.models import UserProfile
from django.views.generic import ListView, CreateView
from .models import *
from .forms import ContentForm, ReviewContentForm, FeedImageFormSet
from django.urls import reverse_lazy

class ContentListView(ListView):
    model = Content
    template_name = "feed/post_all.html"
    context_object_name = 'posts'
    paginate_by = 8

# 일반 게시물 작성에 라우팅
class ContentCreateView(CreateView):
    model = Content
    form_class = ContentForm
    template_name = 'feed/post_create.html' 
    success_url = reverse_lazy('feed:post-create')  # 생성 성공 후 리다이렉트

    def get_context_data(self, **kwargs):
        data = super(ContentCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['images'] = FeedImageFormSet(self.request.POST, self.request.FILES)  # 파일 데이터 추가
        else:
            data['images'] = FeedImageFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        images = context['images']
        form.instance.user = self.request.user
        form.instance.content_type = 'post'
        self.object = form.save()
        
        if images.is_valid():
            images.instance = self.object
            images.save()

        return super(ContentCreateView, self).form_valid(form)
    
# 구매기록에서 라우팅
class ReviewCreateView(CreateView):
    model = Content
    form_class = ReviewContentForm
    template_name = 'feed/review_create.html' 
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.content_type = 'review'
        return super().form_valid(form)

def post_detail(request, pk):
    post = get_object_or_404(Content, pk=pk)
    return render(request, 'feed/post_detail.html', {'post': post})