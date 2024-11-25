import pandas as pd
import pickle
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import os

def evaluate_model():
    """
    Evaluate the transaction classifier with a test dataset.
    Generate a confusion matrix heatmap for better visualization.
    """
    model_path = r"D:\Projects\personal-finance-tracker\static\categorizer_model.pkl"
    vectorizer_path = r"D:\Projects\personal-finance-tracker\static\vectorizer.pkl"
    test_data_path = r"D:\Projects\personal-finance-tracker\labeled_transactions.csv"  # Replace with your test dataset path

    # Load the model and vectorizer
    try:
        with open(model_path, "rb") as model_file:
            model = pickle.load(model_file)
        print("Model loaded successfully.")

        with open(vectorizer_path, "rb") as vectorizer_file:
            vectorizer = pickle.load(vectorizer_file)
        print("Vectorizer loaded successfully.")
    except Exception as e:
        print(f"Error loading pickle file: {e}")
        return

    # Load the test dataset
    try:
        test_data = pd.read_csv(test_data_path)
        print("Test data loaded successfully.")
    except Exception as e:
        print(f"Error loading test dataset: {e}")
        return

    # Check required columns
    if "Description" not in test_data.columns or "Category" not in test_data.columns:
        print("Test dataset must contain 'Description' and 'Category' columns.")
        return

    # Prepare test data
    X_test = vectorizer.transform(test_data["Description"].astype(str))
    y_test = test_data["Category"]

    # Predict and evaluate
    try:
        y_pred = model.predict(X_test)

        # Confusion Matrix
        cm = confusion_matrix(y_test, y_pred, labels=model.classes_)
        print("\nConfusion Matrix:")
        print(cm)

        # Classification Report
        report = classification_report(y_test, y_pred, target_names=model.classes_, zero_division=0)
        print("\nClassification Report:")
        print(report)

        # Plot Confusion Matrix Heatmap
        plt.figure(figsize=(10, 7))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=model.classes_, yticklabels=model.classes_)
        plt.title("Confusion Matrix Heatmap")
        plt.xlabel("Predicted Labels")
        plt.ylabel("True Labels")
        plt.tight_layout()

        # Save Heatmap
        os.makedirs("static", exist_ok=True)
        heatmap_path = "static/confusion_matrix_heatmap.png"
        plt.savefig(heatmap_path)
        print(f"Confusion matrix heatmap saved to {heatmap_path}.")
        plt.close()

    except Exception as e:
        print(f"Error evaluating the model: {e}")

if __name__ == "__main__":
    evaluate_model()
