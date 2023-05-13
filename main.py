import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

import pymongo
client = pymongo.MongoClient('mongodb+srv://Borimir:Borimir2007@cluster0.ublc9zj.mongodb.net/?retryWrites=true&w=majority')
db = client['Python-project']
collection = db['Start-new']

data = [doc['name'] for doc in collection.find()]

# Create a TfidfVectorizer object
vectorizer = TfidfVectorizer()

# Fit the vectorizer to the text data
vectorizer.fit(data)

# Transform the text data into a numerical feature matrix
X = vectorizer.transform(data)

# Print the feature matrix shape and the first row
print('Feature matrix shape:', X.shape)
print('First row:', X[0].toarray())