import spacy
from nltk.stem import PorterStemmer
from pymongo import MongoClient

class SymptomMatcher:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_md")
        self.stemmer = PorterStemmer()
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

                    for symptom in symptoms:
                        tokens = self.nlp(symptom)
                        tokenized_symptom = [token.text for token in tokens]
                        self.collection_symptoms.append(tokenized_symptom)

    def check_root(self, word1, word2):
        root1 = self.stemmer.stem(word1)
        root2 = self.stemmer.stem(word2)
        
        if root1 in root2 or root2 in root1:
            return True
        else:
            return False

    def check_symptom_with_word(self, input_word):
        input_tokens = self.nlp(input_word)
        input_root = input_tokens[0].lemma_

        for symptom in self.collection_symptoms:
            symptom_tokens = self.nlp(' '.join(symptom))
            symptom_root = symptom_tokens[0].lemma_

            if self.check_root(input_root, symptom_root):
                print(f"Root found: '{input_word}' matches symptom: {' '.join(symptom)}")

# Usage example
symptom_matcher = SymptomMatcher()
symptom_matcher.load_symptoms()
input_word = "head"
symptom_matcher.check_symptom_with_word(input_word)
