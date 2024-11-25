import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle
import os

def train_transaction_classifier():
    """
    Train a transaction classifier using labeled transaction data.
    """
    dataset_path = r"D:\Projects\personal-finance-tracker\labeled_transactions.csv"

    # Check if dataset exists
    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"Dataset not found: {dataset_path}. Please ensure the file exists.")

    # Load dataset
    print("Loading dataset...")
    data = pd.read_csv(dataset_path)

    # Validate dataset
    if data.empty:
        raise ValueError("The dataset is empty. Please provide a valid dataset.")
    if "Description" not in data.columns or "Category" not in data.columns:
        raise ValueError("Dataset must contain 'Description' and 'Category' columns.")

    print("Dataset loaded successfully.")
    print(f"Dataset contains {len(data)} records.")

    # Extract features and labels
    vectorizer = TfidfVectorizer(max_features=5000)
    X = vectorizer.fit_transform(data["Description"].astype(str))  # Ensure text is treated as string
    y = data["Category"]

    # Train classifier
    print("Training classifier...")
    model = MultinomialNB()
    model.fit(X, y)

    # Save model and vectorizer
    os.makedirs("static", exist_ok=True)  # Ensure the directory exists

    model_path = "static/categorizer_model.pkl"
    vectorizer_path = "static/vectorizer.pkl"

    with open(model_path, "wb") as model_file:
        pickle.dump(model, model_file)
        print(f"Model saved to {model_path}")

    with open(vectorizer_path, "wb") as vectorizer_file:
        pickle.dump(vectorizer, vectorizer_file)
        print(f"Vectorizer saved to {vectorizer_path}")

if __name__ == "__main__":
    try:
        train_transaction_classifier()
        print("Transaction classifier trained and saved successfully!")
    except Exception as e:
        print(f"Error: {e}")