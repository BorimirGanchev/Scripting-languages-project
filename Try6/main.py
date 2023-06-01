from sklearn.feature_extraction.text import CountVectorizer

vectorizer = CountVectorizer()
raw_documents = ["I have a pain in the head", "I have a headache", "I have a pain in the head, but not fever", "I have a pain in the head, but don't have fever"]
vectors = vectorizer.fit_transform(raw_documents)

print(vectorizer.get_feature_names_out())
print(vectors.toarray())