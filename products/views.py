from django.shortcuts import render
from django.views.generic import TemplateView,DetailView
from django.views import View
#models
from .models import Category,SubCategory, Product,Brand,Tag,ProductSize,Color
#forms


class HomePageView(TemplateView):
    template_name = 'web/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['categories'] = Category.objects.all()
        context['subcategories'] = SubCategory.objects.filter(is_popular=True)
        context['best_sellers'] = Product.objects.filter(is_best_seller=True)[:8]
        context['new_arrivals'] = Product.objects.filter(is_new_arrival=True)[:8]
        context['top_rated'] = Product.objects.filter(is_top_rated=True)[:8]
        return context


class ShopView(View):
    def get(self, request):
        category = request.GET.get('category', '')
        department = request.GET.get('department', '')
        color = request.GET.get('color', '')
        size = request.GET.get('size', '')
        amount = request.GET.get('amount', '')
        brand = request.GET.getlist('brand', '')
        tag = request.GET.get('tag', '')
        products = Product.objects.all()

        if department:
            products = products.filter(subcategory__category__slug=department)
        if category:
            products = products.filter(subcategory__slug=category)
        if color:
            products = products.filter(productimage__color__name=color)
        if size:
            products = products.filter(availablesize__size__code=size)
        if amount:
            # Parse the amount parameter into minimum and maximum values
            amount = amount.replace('$', '')
            try:
                min_amount, max_amount = map(int, amount.split('-'))
                # Filter products within the specified price range
                products = products.filter(availablesize__sale_price__gte=min_amount, availablesize__sale_price__lte=max_amount).distinct()
            except ValueError:
                # Handle invalid input if needed
                print("ValueError")
        if brand:
            products = products.filter(brand__slug__in=brand)
        if tag:
            products = products.filter(tag__slug=tag)
        
        context = {
            'categories': Category.objects.all(),
            'subcategories': SubCategory.objects.filter(is_popular=True),
            'products': products,
            'brands': Brand.objects.all(),
            'tags': Tag.objects.all(),
            'sizes': ProductSize.objects.all(),
            'colors': Color.objects.all()
        }
        return render(request, 'web/shop.html', context)
    
    
class ProductDetailView(DetailView):
    model = Product
    template_name = "web/product_detail.html"
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['request'] = self.request
        return context