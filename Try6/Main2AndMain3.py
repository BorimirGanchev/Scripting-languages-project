import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.chunk import ne_chunk
import spacy
from pymongo import MongoClient
from spacy.lang.en.stop_words import STOP_WORDS

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

    def calculate_similarity(self, phrase, symptom):
        doc1 = self.nlp(phrase)
        doc2 = self.nlp(' '.join(symptom))
        similarity_score = doc1.similarity(doc2)
        return similarity_score

    def match_symptoms(self, phrases):
        for phrase in phrases:
            for symptom in self.collection_symptoms:
                similarity = self.calculate_similarity(phrase, symptom)
                print(f"Phrase: {phrase}, Symptom: {' '.join(symptom)}, Similarity: {similarity}")

# Usage example
sentence = "I have a pain in the head, fever and cough."
phrase_extractor = PhraseExtractor(sentence)
phrase_extractor.process()
phrases = phrase_extractor.get_phrases()

symptom_matcher = SymptomMatcher()
symptom_matcher.load_symptoms()
symptom_matcher.match_symptoms(phrases)
