# write a KNN algorithm in easy code logic without classes and custom functions  from scratch in python
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier

# 1. Read data (collect data)
# Replace "data.csv" with your dataset file.
try:
    df = pd.read_csv("data.csv")
except FileNotFoundError:
    # Sample data for direct run
    df = pd.DataFrame({
        "feature1": [1, 2, 3, 6, 7, 8, 2, 5, 4, 9],
        "feature2": [2, 3, 1, 5, 8, 6, 2, 5, 4, 7],
        "target":   ["A", "A", "A", "B", "B", "B", "A", "B", "A", "B"]
    })

# 2. Clean data
df = df.dropna().reset_index(drop=True)

# Separate features and target
X = df.drop(columns=["target"]).to_numpy(dtype=float)
y = df["target"]

# Encode target if needed
# if y_raw.dtype == object:
#     y, class_names = pd.factorize(y_raw)
# else:
#     y = y_raw.to_numpy(dtype=int)
#     class_names = None

# 3. Feature engineering
# Standardization using training statistics
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

mean = X_train.mean(axis=0)
std = X_train.std(axis=0)
std[std == 0] = 1

X_train = (X_train - mean) / std
X_test = (X_test - mean) / std

# 4. Select model
# K-Nearest Neighbors (KNN)
k = 3

# 5. Train model
# KNN is a lazy learner, so training is storing the prepared data
# X_train and y_train are the trained model memory

# 6. Test and predict
y_pred = []
for i in range(len(X_test)):
    distances = np.linalg.norm(X_train - X_test[i], axis=1)
    nearest_neighbors = np.argsort(distances)[:k]
    nearest_labels = y_train[nearest_neighbors]
    prediction = np.bincount(nearest_labels).argmax()
    y_pred.append(prediction)

y_pred = np.array(y_pred)

# 7. Evaluate results
accuracy = accuracy_score(y_test, y_pred)

print("Predictions:", y_pred)
print("Actual     :", y_test)
print("Accuracy   :", accuracy)
k = 3
model = KNeighborsClassifier(n_neighbors=k)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("Predictions:", y_pred)
print("Actual     :", y_test.to_numpy() if hasattr(y_test, "to_numpy") else y_test)
print("Accuracy   :", accuracy)