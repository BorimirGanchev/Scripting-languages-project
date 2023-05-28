import spacy
from pymongo import MongoClient
from bson.objectid import ObjectId

class SymptomMatcher:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_md")
        self.client = MongoClient('mongodb+srv://Borimir:Borimir2007@cluster0.ublc9zj.mongodb.net/?retryWrites=true&w=majority')
        self.db = self.client['Python-project']
        self.collection_symptoms = []

    def load_symptoms(self):
        collection_names = self.db.list_collection_names()
        
        for collection_name in collection_names:
            current_collection = self.db[collection_name]
            documents = current_collection.find()
            
            for document in documents:
                if "symptoms" in document:
                    symptoms = document["symptoms"]
                    my_string = ' '.join(symptoms)
                    doc = self.nlp(my_string)
                    sentence = list(doc.sents)[0]
                    self.collection_symptoms.append(( document["description"], sentence))

    def match_symptoms(self, input_text):
        input_text = self.nlp(input_text)
        matches = []
        
        for description, search in self.collection_symptoms:
            percentage = round((input_text.similarity(search) * 100), 1)
            print(f"{percentage}%")
            
            matches.append((description, percentage))
        
        # Sort matches in descending order based on percentage
        sorted_matches = sorted(matches, key=lambda x: x[1], reverse=True)
        
        for match in sorted_matches:
            description, percentage = match
            print(f"{description}, Percentage: {percentage}%")
        
        return sorted_matches

# Usage example
symptom_matcher = SymptomMatcher()
symptom_matcher.load_symptoms()
matches = symptom_matcher.match_symptoms("I have a cat")
