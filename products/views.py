from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
# Create your views here.
from .models import Product

class Product(ListView):
    model = Product
    template_name = 'products/products.html'