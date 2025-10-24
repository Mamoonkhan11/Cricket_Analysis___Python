# Train Match Predictor Model

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pickle
import os

# Load dataset
matches = pd.read_csv("data/Match.csv")  # make sure path is correct
# Features and target
features = ['Team_Name_Id', 'Opponent_Team_Id', 'Toss_Winner_Id', 'Venue_Name']
target = 'winner'

# Drop missing values
matches = matches.dropna(subset=features + [target])

# Encode categorical columns
encoders = {}
for col in features + [target]:
    le = LabelEncoder()
    matches[col] = le.fit_transform(matches[col])
    encoders[col] = le

# Split features and target
X = matches[features]
y = matches[target]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = LogisticRegression(max_iter=200)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"\n Model trained with accuracy: {acc*100:.2f}% \n")

# Save model and encoders
os.makedirs("models", exist_ok=True)
with open("models/match_predictor.pkl", "wb") as f:
    pickle.dump(model, f)

with open("models/encoders.pkl", "wb") as f:
    pickle.dump(encoders, f)

print("\n Model and encoders saved to models \n")