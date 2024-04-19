# import pandas as pd
# import numpy as np
# import pickle
#
# df = pd.read_csv('iris.data')
#
# X = np.array(df.iloc[:, 0:4])
# y = np.array(df.iloc[:, 4:])
#
# from sklearn.preprocessing import LabelEncoder
# le = LabelEncoder()
# y = le.fit_transform(y.reshape(-1))
#
# from sklearn.model_selection import train_test_split
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
#
# from sklearn.svm import SVC
# sv = SVC(kernel='linear').fit(X_train,y_train)
#
#
# pickle.dump(sv, open('iri.pkl', 'wb'))



import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
import pickle
# Load the dataset
df = pd.read_csv('Prostate_cancer.csv')

# Preprocess the dataset
df['diagnosis_result'] = df['diagnosis_result'].replace(['B'],'0')
df['diagnosis_result'] = df['diagnosis_result'].replace(['M'],'1')
df[['diagnosis_result']] = df[['diagnosis_result']].apply(pd.to_numeric, errors='ignore')

# Select features and target variable
X = df[['radius', 'texture', 'perimeter', 'area', 'smoothness']]
Y = df['diagnosis_result']

# Split the data into training and testing sets
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=9)


# Create and train the KNN model
knncla = KNeighborsClassifier(n_neighbors=5, n_jobs=-1)
knncla.fit(X_train, Y_train)

# Make predictions on the test set
Y_predict = knncla.predict(X_test)


pickle.dump(knncla, open('final.pkl', 'wb'))