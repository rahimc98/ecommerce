from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = "products"

urlpatterns = [
    path("", views.Product.as_view(), name="product"),  
]