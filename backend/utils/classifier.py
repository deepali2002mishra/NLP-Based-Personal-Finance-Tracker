import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

def categorize_transaction(description):
    """
    Categorize a transaction based on its description.
    """
    try:
        # Load the pre-trained model and vectorizer
        with open("static/transaction_classifier.pkl", "rb") as f:
            model, vectorizer = pickle.load(f)

        # Transform the description and predict category
        description_vectorized = vectorizer.transform([description])
        category = model.predict(description_vectorized)[0]
        return category
    except Exception as e:
        print(f"Error categorizing transaction: {description} -> {e}")
        return "Others"

# Keywords-based fallback (optional, for robustness)
KEYWORDS = {
    "Rent": ["rent", "lease"],
    "Groceries": ["supermarket", "grocery", "vegetables"],
    "Travel": ["flight", "airline", "train", "uber", "taxi"],
    "Utilities": ["electricity", "water", "gas", "utility"],
    "Shopping": ["store", "mall", "shopping", "purchase"],
}

def keywords_based_categorization(description):
    for category, keywords in KEYWORDS.items():
        if any(keyword in description.lower() for keyword in keywords):
            return category
    return "Others"
