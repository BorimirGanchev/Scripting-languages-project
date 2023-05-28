from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth.decorators import login_required

from .forms import SignupForm
from item.models import Item, SymptomMatcher

def index(request): 
    return render(request, 'IllnessWeb/index.html')

def search(request):
    
    symptom_matcher = SymptomMatcher()
    symptom_matcher.load_symptoms()
    query = request.GET.get('query', '')
    items = Item.objects.all()

    if query:
        matches = symptom_matcher.match_symptoms(query)
        strings_only = [item[0] for item in matches]

        sorted_items = sorted(items, key=lambda item: strings_only.index(item.name) if item.name in strings_only else len(strings_only))
        
        return render(request, 'IllnessWeb/search.html', {
            'items': sorted_items,
            'query': query, 
        })
    else:
        return render(request, 'IllnessWeb/search.html', {
            'query': query, 
        })

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
