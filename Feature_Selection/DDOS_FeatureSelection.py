import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_selection import RFE
from sklearn.linear_model import LinearRegression

print("Dataset loading")
data = pd.read_csv('APA-DDoS-Dataset.csv')
print("Dataset loaded")


X = data.iloc[:, :-1]
y = data.iloc[:, -1]

# Create linear regression object
lr = LinearRegression()

# Create recursive feature elimination object
rfe = RFE(lr, n_features_to_select=5)

# Fit RFE
print('hello')
rfe.fit(X, y)

# Get selected features
selected_features = X.columns[rfe.support_]

# Get feature importance scores
feature_importance = rfe.estimator_.coef_

# Plot feature importance scores
plt.barh(range(len(selected_features)), feature_importance, align='center')
plt.yticks(range(len(selected_features)), selected_features)
plt.xlabel('Importance Score')
plt.ylabel('Selected Features')
plt.show()


