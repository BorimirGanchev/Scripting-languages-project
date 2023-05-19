import spacy
from pymongo import MongoClient
from bson.objectid import ObjectId

nlp = spacy.load("en_core_web_md")

client = MongoClient('mongodb+srv://Borimir:Borimir2007@cluster0.ublc9zj.mongodb.net/?retryWrites=true&w=majority')
db = client['Python-project']
collection = db['Start-new']

collection_symptoms = []

# Get a list of all collection names in the database
collection_names = db.list_collection_names()

for collection_name in collection_names:
    current_collection = db[collection_name]
    documents = current_collection.find()
    for document in documents:
        if "symptoms" in document:
            symptoms = document["symptoms"]
            my_string = ' '.join(symptoms)
            doc = nlp(my_string)
            sentence = list(doc.sents)[0]
            collection_symptoms.append((collection_name, document["_id"], sentence))


input_text = nlp("I have a pain in the chest")

max_percentage = -1.0
max_collection = None
max_document_id = None

for collection_name, document_id, search in collection_symptoms:
    percentage = round((input_text.similarity(search) * 100), 1)
    print(f"{percentage}%")
    
    if percentage > max_percentage:
        max_percentage = percentage
        max_collection = collection_name
        max_document_id = document_id

print("Document ID:", max_document_id)

