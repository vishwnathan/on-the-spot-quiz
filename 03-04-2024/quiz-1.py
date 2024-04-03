# -*- coding: utf-8 -*-
"""Untitled7.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1VrcOUa3RFIYWaOqUNxAHWyobeayWsh9m
"""

#importing necessary modules
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
import matplotlib.pyplot as plt
import seaborn as sns

#Loading dataset
data = pd.read_csv('/content/DSAI-LVA-DATASET for Quiz.csv')

label_encoder = LabelEncoder()
data['ParentEducation'] = label_encoder.fit_transform(data['ParentEducation'])
data['Pass'] = label_encoder.fit_transform(data['Pass'])
X = data.drop('Pass', axis=1)
y = data['Pass']
scaler = StandardScaler()
X[['StudyTime', 'PreviousTestScore']] = scaler.fit_transform(X[['StudyTime', 'PreviousTestScore']])

#Spliting data into training and testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#Saving it into separate csv files as asked
X_train.to_csv('train_data.csv', index=False)
X_test.to_csv('test_data.csv', index=False)

#function for performance categories
def determine_performance(probabilities):
    if probabilities[0] >= 0.5:
        return 'Fail'
    elif probabilities[1] >= 0.5:
        return 'Pass with Low Grade'
    else:
        return 'Pass with High Grade'

#Decision Tree
clf_dt = DecisionTreeClassifier()
clf_dt.fit(X_train, y_train)
y_pred_dt = clf_dt.predict(X_test)
y_pred_prob_dt = clf_dt.predict_proba(X_test)

#Random Forest
clf_rf = RandomForestClassifier()
clf_rf.fit(X_train, y_train)
y_pred_rf = clf_rf.predict(X_test)
y_pred_prob_rf = clf_rf.predict_proba(X_test)

#XGBoost
clf_xgb = XGBClassifier()
clf_xgb.fit(X_train, y_train)
y_pred_xgb = clf_xgb.predict(X_test)
y_pred_prob_xgb = clf_xgb.predict_proba(X_test)

#Determine performance categories for individual students
performance_categories_dt = [determine_performance(probs) for probs in y_pred_prob_dt]
performance_categories_rf = [determine_performance(probs) for probs in y_pred_prob_rf]
performance_categories_xgb = [determine_performance(probs) for probs in y_pred_prob_xgb]

performance_df = pd.DataFrame({
    'Decision Tree': performance_categories_dt,
    'Random Forest': performance_categories_rf,
    'XGBoost': performance_categories_xgb
})

#saving the result into a csv file as asked
performance_df.to_csv('performance_categories.csv', index=False)