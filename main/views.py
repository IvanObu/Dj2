
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import Product, Category
from cart.forms import CartAddProductForm
# Create your views here.
def popular_list(requset):
    products = Product.objects.filter(available=True)[:4]
    return render(requset, 'main/index/index.html', {'products':products})

def product_datail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    cart_product_form = CartAddProductForm
    return render(request, 'main/product/detail.html', {'product':product, 'cart_product_form':cart_product_form})

def product_list(request, category_slug=None):
    page = request.GET.get('page', 1)
    category=None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    paginator = Paginator(products, 2)
    current_page = paginator.page(int(page))
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        paginator = Paginator(products.filter(category=category))
        current_page = paginator.page(int(page))

    return render(request, 'main/product/list.html', {'category':category, 'categories': categories, 'products':current_page, 'slug_url': category_slug})