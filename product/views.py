from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
# Create your views here.

"""login_required -> 판매자 인증기능 필요, 개발 후 수정(판매자일 경우에 접근 가능)
판매자 관점의 함수

Returns:
    _type_: _description_
"""
@login_required
def seller_index(request):
    product = Product.objects.all().filter(user__id = request.user.id)
    context = {
        'object_list' : product
    }
    return render(request, 'product/seller_index.html', context)

@login_required
def add_product(request):
    if request.method == "POST":
        
        user = request.user
        product_name = request.POST.get('productname')
        product_price = request.POST['price']
        description = request.POST.get('description')
        
        
        fs=FileSystemStorage()
        uploaded_file = request.FILES['file']
        name = fs.save(uploaded_file.name, uploaded_file)
        url = fs.url(name)

        Product.objects.create(user=user, name=product_name, price =product_price , description=description,image_url=url)        
        return redirect('product:add_product')  # 데이터 저장 후 페이지 재로드
    
    return render(request, 'product/add_product.html')

def product_delete(request, pk):
    object = Product.objects.get(pk=pk)
    object.delete()
    return redirect('product:seller_index')      

"""ProductListView
구매자 관점의 product list

Returns:
    category id가 주어지지 않으면 전체 상품 return
    주어지면 해당 상품만 return
"""
class ProductListView(ListView):
    model = Product
    template_name = 'product/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        if category_id:
            category = get_object_or_404(Category, id=category_id)
            return Product.objects.filter(category=category)
        return Product.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_category_id'] = int(self.kwargs.get('category_id', '0'))
        return context

def product_detail(request, pk):
    object = Product.objects.get(pk=pk)
    context = {
        'object':object
    }
    return render(request, 'product/product_detail.html', context)

