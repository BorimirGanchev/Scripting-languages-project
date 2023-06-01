import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.chunk import ne_chunk
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


# Usage example
sentence = "I have pain in the head, fever and cough."
phrase_extractor = PhraseExtractor(sentence)
phrase_extractor.process()
phrases = phrase_extractor.get_phrases()
print(phrases)  
