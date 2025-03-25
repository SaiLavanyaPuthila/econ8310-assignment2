# -*- coding: utf-8 -*-
"""assignment2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1wIxUwYa58xCVXhDS-XMmDG_xPUOI7gaT
"""

import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# Load training data
train_url = "https://github.com/dustywhite7/Econ8310/raw/master/AssignmentData/assignment3.csv"
train_df = pd.read_csv(train_url)

# Define target and features
y = train_df["meal"]
X = train_df.drop(columns=["meal", "id", "DateTime"], errors="ignore")
X = pd.get_dummies(X, drop_first=True)

# Split for validation
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Define and train the model
model = XGBClassifier(
    n_estimators=100,
    max_depth=8,
    learning_rate=0.2,
    objective="binary:logistic",
    use_label_encoder=False,
    eval_metric="logloss",
    random_state=42
)
modelFit = model.fit(X_train, y_train)

# Validation accuracy
val_preds = model.predict(X_val)
val_preds = [int(p.item()) if hasattr(p, 'item') else int(p) for p in val_preds]
val_accuracy = accuracy_score(y_val, val_preds)
print(f"Validation Accuracy: {val_accuracy:.2f}")

# Retrain on full data
modelFit = model.fit(X, y)

# Save the trained model
joblib.dump(modelFit, "modelFit.pkl")

# Load test data
test_url = "https://github.com/dustywhite7/Econ8310/raw/master/AssignmentData/assignment3test.csv"
test_df = pd.read_csv(test_url)

# Preprocess test data
test_features = test_df.drop(columns=["id", "DateTime"], errors="ignore")
test_features = pd.get_dummies(test_features, drop_first=True)
test_features = test_features.reindex(columns=X.columns, fill_value=0)

# Predict for full test set (expected 1000 rows)
raw_pred = modelFit.predict(test_features)

# Convert predictions to native Python int or float
pred = []
for p in raw_pred:
    if isinstance(p, (np.integer, np.int64, np.int32)):
        pred.append(int(p))
    elif isinstance(p, (np.floating, np.float64, np.float32)):
        pred.append(float(p))
    else:
        pred.append(int(p))  # fallback

# Debug info (optional)
print("Number of predictions:", len(pred))
print("First 5 predictions:", pred[:5])
print("Prediction data types:", set(type(p) for p in pred))

# Save predictions
pd.DataFrame(pred, columns=["meal_prediction"]).to_csv("predictions.csv", index=False)

# Final confirmation
if __name__ == "__main__":
    print("Model training and prediction completed successfully.")