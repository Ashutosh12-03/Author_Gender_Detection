import pandas as pd
from matplotlib import *
import numpy as np
import sklearn
from sklearn import preprocessing
from matplotlib import pyplot
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
final_dataset = pd.read_csv("Final_combined_normalized_dataset.csv")
X=final_dataset.iloc[:,0:len(final_dataset.columns)-1]
Y=final_dataset.iloc[:,-1]
X_train=final_dataset.values
X_test=X_train
Y_train=Y
Y_test=Y
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.05, random_state=1)
X_test=X_test.fillna(0)
X_train=X_train.fillna(0)
#kfold = StratifiedKFold(n_splits=10, random_state=1, shuffle=True)
#cv_results = cross_val_score(model, X_train, Y_train, cv=kfold, scoring='accuracy')
model=SVC(C=3,gamma=0.5,kernel='rbf')
model.fit(X_train,Y_train)
y_pred=model.predict(X_test)
print(accuracy_score(Y_test, y_pred)) 
# result = 0.9891911586106388
print(confusion_matrix(Y_test, y_pred))
'''result
    [[ 3384   170]
    [    8 12906]]'''
print(classification_report(Y_test, y_pred))
''' result
             precision    recall  f1-score   support

     female       1.00      0.95      0.97      3554
       male       0.99      1.00      0.99     12914

avg / total       0.99      0.99      0.99     16468
'''