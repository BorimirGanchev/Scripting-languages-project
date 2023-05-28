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
                    self.collection_symptoms.append((collection_name, document["_id"], sentence))

    def match_symptoms(self, input_text):
        input_text = self.nlp(input_text)
        max_percentage = -1.0
        max_collection = None
        max_document_id = None
        
        for collection_name, document_id, search in self.collection_symptoms:
            percentage = round((input_text.similarity(search) * 100), 1)
            print(f"{percentage}%")
            
            if percentage > max_percentage:
                max_percentage = percentage
                max_collection = collection_name
                max_document_id = document_id
        
        print("Document ID:", max_document_id)
        return max_collection, max_document_id

# Usage example
symptom_matcher = SymptomMatcher()
symptom_matcher.load_symptoms()
collection_name, document_id = symptom_matcher.match_symptoms("I have a pain in the chest")
