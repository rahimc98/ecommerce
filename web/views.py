from django.shortcuts import render

# Create your views here.

def index(request):
    # return render(request, 'index.html')
    return render(request, 'web/includes/base.html')