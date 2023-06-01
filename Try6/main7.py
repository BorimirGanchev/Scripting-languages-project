import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.chunk import ne_chunk
from spacy.lang.en.stop_words import STOP_WORDS
import spacy
from nltk.stem import PorterStemmer
from pymongo import MongoClient

class PhraseExtractor:
    def __init__(self, sentence):
        self.sentence = sentence
        self.tokens = None
        self.pos_tags = None
        self.chunked = None
        self.phrases = None

    def tokenize(self):
        self.tokens = word_tokenize(self.sentence)

    def pos_tagging(self):
        self.pos_tags = pos_tag(self.tokens)

    def chunking(self):
        grammar = r"NP: {<DT>?<JJ>*<NN.*>}"
        chunk_parser = nltk.RegexpParser(grammar)
        self.chunked = chunk_parser.parse(self.pos_tags)

    def extract_phrases(self):
        self.phrases = [' '.join([token for token, pos in chunk.leaves()]) for chunk in self.chunked.subtrees() if
                        chunk.label() == 'NP']

    def split_combined_phrases(self):
        split_phrases = []
        for phrase in self.phrases:
            split_phrases.extend(phrase.split(' and '))
        self.phrases = split_phrases

    def remove_stop_words(self):
        self.phrases = [' '.join([token for token in phrase.split() if token.lower() not in STOP_WORDS]) for phrase in self.phrases]

    def process(self):
        self.tokenize()
        self.pos_tagging()
        self.chunking()
        self.extract_phrases()
        self.split_combined_phrases()
        self.remove_stop_words()

    def get_phrases(self):
        return self.phrases

class SymptomMatcher:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_md")
        self.stemmer = PorterStemmer()
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

    def check_root(self, word1, word2):
        root1 = self.stemmer.stem(word1)
        root2 = self.stemmer.stem(word2)
        
        if root1 in root2 or root2 in root1:
            return True
        else:
            return False

    def get_symptom_description(self, symptom):
        query = {"symptoms": symptom}
        collection_names = self.db.list_collection_names()

        descriptions = []
        for collection_name in collection_names:
            current_collection = self.db[collection_name]
            documents = current_collection.find(query, {"description": 1})

            for document in documents:
                description = document.get("description")
                if description:
                    descriptions.append(description)

        return descriptions

    def get_symptom_percentage(self, matched_symptoms, document_symptoms):
        total_matched = len(set(matched_symptoms) & set(document_symptoms))
        total_symptoms = len(set(document_symptoms))
        
        if total_symptoms > 0:
            percentage = (total_matched / total_symptoms) * 100
        else:
            percentage = 0
        
        return percentage

    def check_symptom_with_word(self, phrases):
        matched_symptoms = []

        for input_word in phrases:
            input_tokens = self.nlp(input_word)
            input_root = input_tokens[0].lemma_

            matches = []
            for symptom in self.collection_symptoms:
                symptom_tokens = self.nlp(' '.join(symptom))
                symptom_root = symptom_tokens[0].lemma_

                if self.check_root(input_root, symptom_root):
                    matches.append(symptom)

            if len(matches) > 0:
                similarities = []
                for symptom in matches:
                    symptom_tokens = self.nlp(' '.join(symptom))
                    similarity = input_tokens.similarity(symptom_tokens)
                    similarities.append(similarity)

                max_similarity = max(similarities)
                max_similarity_index = similarities.index(max_similarity)
                matched_symptom = matches[max_similarity_index]
                print(f"Root found: '{input_word}' matches symptom: {' '.join(matched_symptom)}")
                matched_symptoms.append(' '.join(matched_symptom))

        return matched_symptoms


symptom_matcher = SymptomMatcher()
symptom_matcher.load_symptoms()

sentence = "I have pain in the head, fever and cough."
phrase_extractor = PhraseExtractor(sentence)
phrase_extractor.process()
phrases = phrase_extractor.get_phrases()

matched_symptoms = symptom_matcher.check_symptom_with_word(phrases)

combined_descriptions = []
for symptom in matched_symptoms:
    descriptions = symptom_matcher.get_symptom_description(symptom)
    combined_descriptions.extend(descriptions)

combined_descriptions = list(set(combined_descriptions))

for description in combined_descriptions:
    print(f"Description: {description}")

matched_symptoms_combined = list(set(matched_symptoms))

for description in combined_descriptions:
    collection_names = symptom_matcher.db.list_collection_names()

    for collection_name in collection_names:
        current_collection = symptom_matcher.db[collection_name]
        documents = current_collection.find({"description": description}, {"symptoms": 1})

        for document in documents:
            document_symptoms = document.get("symptoms", [])
            matched_percentage = (len(set(matched_symptoms_combined) & set(document_symptoms)) / len(document_symptoms)) * 100
            print(f"Symptom Percentage in Document: {matched_percentage}%")