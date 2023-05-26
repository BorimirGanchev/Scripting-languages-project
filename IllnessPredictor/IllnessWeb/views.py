from django.shortcuts import render

# Create your views here.

def index(request): 
    return render(request, 'IllnessWeb/index.html')

def search(request):
    return render(request, 'IllnessWeb/search.html')