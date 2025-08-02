from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from data import data
import joblib
from menu import menu

# Split into X, y


def init():
    texts = [text for text, label in data]
    labels = [label for text, label in data]


    # Vectorizer
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(texts)

    # Train model
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X, labels)

    # Save model and vectorizer
    joblib.dump(clf, "intent_classifier.pkl")
    joblib.dump(vectorizer, "vectorizer.pkl")


def classify_intent(user_input: str) -> str:
    
    clf = joblib.load("intent_classifier.pkl")
    vectorizer = joblib.load("vectorizer.pkl")
    X_input = vectorizer.transform([user_input])
    predicted_label = clf.predict(X_input)[0]
    return predicted_label

def combined_classify(user_input: str) -> str:
    input_lower = user_input.lower()

    if any(pizza in input_lower for pizza in menu['pizzas']):
        return "pizza"
    elif "complete" in input_lower:
        return "complete"
    elif any(e in input_lower for e in menu['toppings']):
        return "toppings"
    elif any(word in input_lower for word in menu['extras']):
        return "extras"
    elif any(word in input_lower for word in ["street", "avenue", "road", "apartment", "house number", "address", "location"]):
        return "address"
    else:
        return classify_intent(user_input)
