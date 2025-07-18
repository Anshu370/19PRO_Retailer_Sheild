# nlp_detector.py

import joblib
import os
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Load model & vectorizer (trained or fallback)
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "phishing_model.pkl"
VECTORIZER_PATH = BASE_DIR / "vectorizer.pkl"

if MODEL_PATH.exists() and VECTORIZER_PATH.exists():
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
else:
    # fallback stub model
    model = LogisticRegression()
    vectorizer = TfidfVectorizer()
    print("⚠️ NLP model not found, using placeholder.")

def predict_phishing(subject: str, body: str):
    combined = subject + " " + body
    features = vectorizer.transform([combined])
    prediction = model.predict(features)[0]
    proba = model.predict_proba(features)[0]

    return {
        "prediction": "phishing" if prediction == 1 else "legitimate",
        "confidence": round(max(proba) * 100, 2)
    }
