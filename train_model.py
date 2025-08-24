import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import pickle

# Load CSV (state-level rainfall)
df = pd.read_csv("daily-rainfall-at-state-level.csv")

# Fill missing rainfall values
df['actual'] = df['actual'].fillna(0)

# Feature engineering
df['month'] = pd.to_datetime(df['date']).dt.month
df['day'] = pd.to_datetime(df['date']).dt.day

# Encode state_name
le = LabelEncoder()
df['state_encoded'] = le.fit_transform(df['state_name'])

# Features and target
X = df[['state_encoded', 'month', 'day']]
y = df['actual']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest model
model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# Save model and encoder
pickle.dump(model, open("rainfall_model.pkl", "wb"))
pickle.dump(le, open("state_encoder.pkl", "wb"))

print("Model trained and saved successfully!")
print("R^2 score on test set:", model.score(X_test, y_test))

