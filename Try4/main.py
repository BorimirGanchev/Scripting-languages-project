import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.tree import DecisionTreeClassifier
import pymongo

# connect to MongoDB
client = pymongo.MongoClient('mongodb+srv://Borimir:Borimir2007@cluster0.ublc9zj.mongodb.net/?retryWrites=true&w=majority')
db = client['Python-project']
collection = db['Start-new']
cursor = collection.find()
df = pd.DataFrame(list(cursor))

# data cleaning
df['clean_text'] = df['text'].apply(lambda x: x.lower())
df['clean_text'] = df['clean_text'].str.replace('[^\w\s]','')
stop = stopwords.words('english')
df['clean_text'] = df['clean_text'].apply(lambda x: " ".join(x for x in x.split() if x not in stop))
stemmer = SnowballStemmer("english")
df['clean_text'] = df['clean_text'].apply(lambda x: " ".join([stemmer.stem(word) for word in x.split()]))

# or simply 
df['clean_text'] = df['clean_text'].apply(lambda x: x.lower().replace('[^\w\s]',''))
df['clean_text'] = df['clean_text'].apply(lambda x: " ".join(x for x in x.split() if x not in stop))
df['clean_text'] = df['clean_text'].apply(lambda x: " ".join([stemmer.stem(word) for word in x.split()]))


# feature extraction
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df['clean_text']).toarray()
y = df['label']

# training the decision tree
clf = DecisionTreeClassifier()
clf.fit(X, y)

# testing the model
test_symptoms = "I have a pain in the head and fever also i have a pain in the chest too"
cleaned_symptoms = test_symptoms.lower().replace('[^\w\s]','')
cleaned_symptoms = " ".join([word for word in cleaned_symptoms.split() if word not in stop])
cleaned_symptoms = " ".join([stemmer.stem(word) for word in cleaned_symptoms.split()])
test_X = vectorizer.transform([cleaned_symptoms]).toarray()
predicted_illness = clf.predict(test_X)[0]
print(cleaned_symptoms)
print(vectorizer.vocabulary_)


print("The predicted illness for symptoms '%s' is '%s'" % (test_symptoms, predicted_illness))

