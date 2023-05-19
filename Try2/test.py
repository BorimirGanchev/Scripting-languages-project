import pymongo
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier

client = pymongo.MongoClient('mongodb+srv://Borimir:Borimir2007@cluster0.ublc9zj.mongodb.net/?retryWrites=true&w=majority')
db = client['Python-project']
collection = db['Start-new']

data = collection.find({})
df = pd.DataFrame(list(data))

# Extract symptoms from data
symptoms = set()
print(len(data))
for doc in data:
    symptoms |= set(doc['symptoms'])

# Create matrix of symptoms and illnesses
num_patients = len(df)
num_symptoms = len(symptoms)

if num_symptoms > 0:
    symptom_matrix = np.zeros((num_patients, num_symptoms))

    for i, doc in enumerate(df):
        for symptom in doc['symptoms']:
            j = list(symptoms).index(symptom)
            symptom_matrix[i, j] = 1

    # Create labels for each document
    labels = [doc['description'] for doc in data]

    # Fit decision tree classifier to data
    tree = DecisionTreeClassifier()
    tree.fit(symptom_matrix, labels)
else:
    print("No symptoms found in the data")

# Preprocess input from user
input_str = "I have a headache and fever"
input_str = input_str.lower().replace(",", "").replace(".", "")
input_list = input_str.split()
symptoms_list = []

for symptom in symptoms:
    if symptom in input_list:
        symptoms_list.append(1)
    else:
        symptoms_list.append(0)

# Predict illness for new patient
new_patient_symptom_vector = np.array(symptoms_list).reshape(1, -1)
predicted_illness = tree.predict(new_patient_symptom_vector)[0]

print("Predicted illness for new patient: ", predicted_illness)
