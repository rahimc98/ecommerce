from django.views.generic import TemplateView
from .models import SubCategory, Product

class HomePageView(TemplateView):
    template_name = 'web/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = SubCategory.objects.all()
        context['products'] = Product.objects.all()
        return context