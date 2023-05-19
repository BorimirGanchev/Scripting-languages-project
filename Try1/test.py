

import numpy as np
import pandas as pd
from Try1.model import DecisionTreeClassifier
from sklearn.preprocessing import MinMaxScaler, StandardScaler, LabelEncoder, OneHotEncoder


col_names = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'type']
data = pd.read_csv("iris.csv", skiprows=1, header=None, names=col_names)
data.head(10)

data.drop_duplicates(inplace=True)

# Check for missing values and fill them with the mean value of the column
data.fillna(data.mean(), inplace=True)

# Check for outliers and remove them using z-score method
from scipy import stats
z_scores = stats.zscore(data)
abs_z_scores = abs(z_scores)
filtered_entries = (abs_z_scores < 3).all(axis=1)
data = data[filtered_entries]

# Feature Scaling
scaler = MinMaxScaler() # or StandardScaler()
scaled_data = scaler.fit_transform(data)

# Feature Encoding
categorical_features = ['color', 'size']
label_encoder = LabelEncoder()
for feature in categorical_features:
    data[feature] = label_encoder.fit_transform(data[feature])

one_hot_encoder = OneHotEncoder(sparse=False)
encoded_data = one_hot_encoder.fit_transform(data[categorical_features])
data = pd.concat([data.drop(categorical_features, axis=1), pd.DataFrame(encoded_data)], axis=1)

X = data.iloc[:, :-1].values
Y = data.iloc[:, -1].values.reshape(-1,1)
from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=.2, random_state=41)

classifier = DecisionTreeClassifier(min_samples_split=3, max_depth=3)
classifier.fit(X_train,Y_train)
classifier.print_tree()



Y_pred = classifier.predict(X_test) 
from sklearn.metrics import accuracy_score
print(accuracy_score(Y_test, Y_pred))

