import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import text
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import pymongo
import pickle
from sklearn.model_selection import GridSearchCV

client = pymongo.MongoClient('mongodb+srv://Borimir:Borimir2007@cluster0.ublc9zj.mongodb.net/?retryWrites=true&w=majority')
db = client['Python-project']
collection = db['Start-new']

my_stop_words = text.ENGLISH_STOP_WORDS.union(["patient", "symptom", "disease"])

porter = PorterStemmer()

docs = []
labels = []
for doc in collection.find():
    text = doc['text']
    description = doc['description']
    symptoms = ', '.join(doc['symptoms'])
    combined = word_tokenize(f'{text} {description}')
    stemmed = [porter.stem(word.lower()) for word in combined if word.lower() not in my_stop_words]
    preprocessed = ' '.join(stemmed)
    docs.append(preprocessed)
    labels.append(doc['label'])

df = pd.DataFrame({'text': docs, 'label': labels})
X_train, X_test, y_train, y_test = train_test_split(df['text'], df['label'], test_size=0.2, random_state=42)

vectorizer = TfidfVectorizer()
vectorizer.fit(X_train)
X_train = vectorizer.transform(X_train)
X_test = vectorizer.transform(X_test)

print('Training feature matrix shape:', X_train.shape)
print('Test feature matrix shape:', X_test.shape)
print('First training row:', X_train[0].toarray())

dtc = DecisionTreeClassifier(max_depth=10, min_samples_leaf=1, min_samples_split=2)
dtc.fit(X_train, y_train)

# save the model to disk
filename = 'dtc_model.sav'
pickle.dump(dtc, open(filename, 'wb'))
loaded_model = pickle.load(open(filename, 'rb'))


# use the loaded model to make predictions on the test set
y_pred_loaded = loaded_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred_loaded)
precision = precision_score(y_test, y_pred_loaded, average='weighted')
recall = recall_score(y_test, y_pred_loaded, average='weighted')
f1 = f1_score(y_test, y_pred_loaded, average='weighted')
# print the metrics
print('Accuracy:', accuracy)
print('Precision:', precision)
print('Recall:', recall)
print('F1-score:', f1)


# use the trained classifier to make predictions on the training set
y_pred_train = dtc.predict(X_train)
accuracy_train = accuracy_score(y_train, y_pred_train)
y_pred_test = dtc.predict(X_test)
accuracy_test = accuracy_score(y_test, y_pred_test)

# print the accuracies
print('Desired training accuracy:', 0.95)
print('Actual training accuracy:', accuracy_train)
print('Desired test accuracy:', 0.90)
print('Actual test accuracy:', accuracy_test)



# define the hyperparameters and their values to test
param_grid = {
    'max_depth': [10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}
grid_search = GridSearchCV(dtc, param_grid, cv=5)
grid_search.fit(X_train, y_train)

# print the best hyperparameters and the corresponding accuracy score
print('Best hyperparameters:', grid_search.best_params_)
print('Accuracy:', grid_search.best_score_)
