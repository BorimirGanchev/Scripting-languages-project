import pymongo
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier



client = pymongo.MongoClient('mongodb+srv://Borimir:Borimir2007@cluster0.ublc9zj.mongodb.net/?retryWrites=true&w=majority')
db = client['Python-project']
collection = db['Start-new']

data = collection.find({})
doc_list = list(data)
df = pd.DataFrame(doc_list)

# Extract symptoms and illnesses from data
symptoms = set()
illnesses = set()

num_documents = collection.count_documents({})
print(f"Number of documents in collection: {num_documents}")


for doc in doc_list:
    print(doc['symptoms'])
    symptoms |= set(doc['symptoms'])
    illnesses.add(doc['description']) 

# Create matrix of symptoms and illnesses
num_patients = len(df)
num_symptoms = len(symptoms)
num_illnesses = len(illnesses)

if num_symptoms > 0:
    symptom_matrix = np.zeros((num_patients, num_symptoms))
    illness_labels = []

    for i, doc in enumerate(data):
        illness_labels.append(doc['description'])
        for symptom in doc['symptoms']:
            j = list(symptoms).index(symptom)
            symptom_matrix[i, j] = 1


    # Fit decision tree classifier to data
    tree = DecisionTreeClassifier()
    tree.fit(symptom_matrix, illness_labels)
else:
    print("No symptoms found in the data")


# Predict illness for new patient
new_patient_symptoms = ['headache', 'fever', 'cough']
new_patient_symptom_vector = np.zeros((1, num_symptoms))

for symptom in new_patient_symptoms:
    if symptom not in symptoms:
        print(f"{symptom} not in list of symptoms: {symptoms}")
    j = list(symptoms).index(symptom)
    new_patient_symptom_vector[0, j] = 1

predicted_illness = tree.predict(new_patient_symptom_vector)[0]

print("Predicted illness for new patient: ", predicted_illness)