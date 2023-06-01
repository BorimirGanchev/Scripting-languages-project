import nltk
from nltk.collocations import BigramAssocMeasures

def extract_collocations(input_sentence, n, num_collocations):
    # Tokenize the input sentence
    tokens = input_sentence.split()

    # Generate n-grams
    ngrams = list(nltk.ngrams(tokens, n))

    # Create a frequency distribution of the n-grams
    fdist = nltk.FreqDist(ngrams)

    # Extract the top collocations based on frequency
    collocations = fdist.most_common(num_collocations)

    # Join the collocations into a single token if needed
    collocations = [('_'.join(collocation), freq) for collocation, freq in collocations]

    return collocations

# Usage example
input_sentence = "I have a pain in the head"
collocations = extract_collocations(input_sentence, 2, 5)
print(collocations)

