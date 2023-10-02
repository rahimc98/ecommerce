from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = "web"

urlpatterns = [
    path("web/", TemplateView.as_view(template_name="web/web.html")),  
]