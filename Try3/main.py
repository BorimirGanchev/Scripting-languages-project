import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report

# Load the data
df = pd.read_csv('disease-and-symptoms.csv')

# Clean the data
df = df[['name', 'symptoms', '']] # Keep only relevant columns
df['text'] = df['text'].str.lower() # Convert text to lowercase
df['text'] = df['text'].str.replace('[^\w\s]', '') # Remove punctuation
df['text'] = df['text'].str.split() # Tokenize text

# Vectorize the data
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df['text'])
y = df['label']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train the model
clf = DecisionTreeClassifier()
clf.fit(X_train, y_train)

# Evaluate the model
y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))
