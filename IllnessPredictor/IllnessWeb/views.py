from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth.decorators import login_required

from .forms import SignupForm
from item.models import Item, SymptomMatcher, PhraseExtractor

def index(request): 
    return render(request, 'IllnessWeb/index.html')

def search(request):
    symptom_matcher = SymptomMatcher()
    symptom_matcher.load_symptoms()
    query = request.GET.get('query', '')
    items = Item.objects.all()

    if query:
        phrase_extractor = PhraseExtractor(query)
        phrase_extractor.process()
        phrases = phrase_extractor.get_phrases()

        matched_symptoms = symptom_matcher.check_symptom_with_word(phrases)

        combined_descriptions = []
        for symptom in matched_symptoms:
            descriptions = symptom_matcher.get_symptom_description(symptom)
            combined_descriptions.extend(descriptions)

        combined_descriptions = list(set(combined_descriptions))

        matched_symptoms_combined = list(set(matched_symptoms))

        filtered_items = items.filter(name__in=combined_descriptions)

        illness_percentages = {}
        for description in combined_descriptions:
            collection_names = symptom_matcher.db.list_collection_names()

            for collection_name in collection_names:
                current_collection = symptom_matcher.db[collection_name]
                documents = current_collection.find({"description": description}, {"symptoms": 1})

                for document in documents:
                    document_symptoms = document.get("symptoms", [])
                    matched_percentage = (len(set(matched_symptoms_combined) & set(document_symptoms)) / len(document_symptoms)) * 100
                    illness_percentages[description] = matched_percentage

        return render(request, 'IllnessWeb/search.html', {
            'items': filtered_items,
            'query': query, 
            'illness_percentages': illness_percentages,
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
