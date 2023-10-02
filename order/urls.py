from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = "order"

urlpatterns = [
    path("order/", TemplateView.as_view(template_name="order/order.html")),  
]