from django.shortcuts import render, redirect

from .forms import SignupForm

def index(request): 
    return render(request, 'IllnessWeb/index.html')

def search(request):
    return render(request, 'IllnessWeb/search.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/login/')
    else:
        form = SignupForm()

    return render(request, 'IllnessWeb/signup.html', {
        'form': form
    })