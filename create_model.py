"""
Train and save a KNN model for mental health prediction.
Generates a synthetic dataset and saves the trained model.
"""
import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import pickle
import os

np.random.seed(42)
n = 2000

age = np.random.randint(16, 65, n)
gender = np.random.randint(0, 2, n)
sleep_hours = np.random.uniform(3, 10, n)
work_hours = np.random.uniform(2, 14, n)
physical_activity = np.random.randint(0, 8, n)
social_interaction = np.random.randint(0, 11, n)
stress_level = np.random.randint(1, 11, n)
screen_time = np.random.uniform(1, 12, n)
caffeine = np.random.randint(0, 6, n)
alcohol = np.random.randint(0, 6, n)
family_history = np.random.randint(0, 2, n)
therapy_history = np.random.randint(0, 2, n)
anxiety_score = np.random.randint(0, 22, n)
depression_score = np.random.randint(0, 28, n)

# Label logic
def get_label(row):
    a, d, s, sl, pa = row
    risk = 0
    if a >= 15: risk += 3
    elif a >= 10: risk += 2
    elif a >= 5: risk += 1
    if d >= 20: risk += 3
    elif d >= 15: risk += 2
    elif d >= 10: risk += 1
    if s >= 8: risk += 2
    elif s >= 6: risk += 1
    if sl < 5: risk += 2
    elif sl < 6: risk += 1
    if pa == 0: risk += 1
    if risk >= 6: return 2  # High Risk
    elif risk >= 3: return 1  # Moderate
    else: return 0  # Healthy

labels_input = np.stack([anxiety_score, depression_score, stress_level, sleep_hours, physical_activity], axis=1)
labels = np.array([get_label(r) for r in labels_input])

df = pd.DataFrame({
    'age': age, 'gender': gender, 'sleep_hours': sleep_hours,
    'work_hours': work_hours, 'physical_activity': physical_activity,
    'social_interaction': social_interaction, 'stress_level': stress_level,
    'screen_time': screen_time, 'caffeine': caffeine, 'alcohol': alcohol,
    'family_history': family_history, 'therapy_history': therapy_history,
    'anxiety_score': anxiety_score, 'depression_score': depression_score,
    'label': labels
})
df.to_csv('dataset/mental_health_dataset.csv', index=False)

X = df.drop('label', axis=1)
y = df['label']

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('knn', KNeighborsClassifier(n_neighbors=7))
])
pipeline.fit(X, y)

with open('model/model.pkl', 'wb') as f:
    pickle.dump(pipeline, f)

print("Model trained and saved successfully!")
print(f"Label distribution: {dict(zip(*np.unique(y, return_counts=True)))}")
