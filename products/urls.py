from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = "products"

urlpatterns = [
    path("", views.HomePageView.as_view(), name="product"),  
    path('shop/', views.ShopView.as_view(), name='shop'),
    path('product/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
]