import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

stop_words = set(stopwords.words('english'))
ps = PorterStemmer()

def preprocess(text):
    # Tokenize the text
    tokens = nltk.word_tokenize(text.lower())
    
    # Remove stop words
    tokens = [token for token in tokens if token not in stop_words]
    
    # Apply stemming
    tokens = [ps.stem(token) for token in tokens]
    
    # Join the tokens back into a string
    preprocessed_text = ' '.join(tokens)
    
    return preprocessed_text


# Load the trained model
model = joblib.load('dtc_model.sav')

# Load the vectorizer
vectorizer = joblib.load('vectorizer.sav')

# Store the input sentence in a variable
input_sentence = "I have a headache and cough"

# Preprocess the input sentence
# This might include things like tokenizing, removing stop words, etc.
preprocessed_sentence = preprocess(input_sentence)
print('Preprocessed sentence:', preprocessed_sentence)


# Vectorize the preprocessed sentence
# This should use the same vectorizer that was used during training
vectorized_sentence = vectorizer.transform([preprocessed_sentence])
print('Vectorized sentence:', vectorized_sentence)
print(vectorized_sentence.shape)

print("----------------")
print(model.classes_)

# Make a prediction using the trained model
predicted_illness = model.predict(vectorized_sentence)

# Print the predicted illness
print("hello")
print(predicted_illness)
