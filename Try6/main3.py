import spacy
from pymongo import MongoClient

class SymptomMatcher:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_md")
        self.client = MongoClient('mongodb+srv://Borimir:Borimir2007@cluster0.ublc9zj.mongodb.net/?retryWrites=true&w=majority')
        self.db = self.client['Python-project']
        self.collection_symptoms = set()

    def load_symptoms(self):
        collection_names = self.db.list_collection_names()

        for collection_name in collection_names:
            current_collection = self.db[collection_name]
            documents = current_collection.find()

            for document in documents:
                if "symptoms" in document:
                    symptoms = document["symptoms"]

                    for symptom in symptoms:
                        tokens = self.nlp(symptom)
                        tokenized_symptom = [token.text for token in tokens]
                        self.collection_symptoms.add(tuple(tokenized_symptom))

    def print_tokenized_symptoms(self):
        for symptom in self.collection_symptoms:
            print(symptom)

# Usage example
symptom_matcher = SymptomMatcher()
symptom_matcher.load_symptoms()
symptom_matcher.print_tokenized_symptoms()
