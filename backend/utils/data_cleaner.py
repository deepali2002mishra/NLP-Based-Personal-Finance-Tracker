# Script: data_cleaning_validation.py

import pandas as pd
import re

def preprocess_bank_statement(data):
    """
    Function to preprocess a bank statement.
    Add your cleaning and processing logic here.
    """
    # Example processing logic
    data = data.dropna()
    return data


def clean_and_validate_data(file_path, output_path):
    """
    Cleans and validates the input CSV data file.
    
    Args:
        file_path (str): Path to the input CSV file.
        output_path (str): Path to save the cleaned and validated output CSV file.
    """
    try:
        # Load data
        print("Loading data...")
        data = pd.read_csv(file_path, delimiter=",", encoding="utf-8")

        # Step 1: Clean numerical columns
        print("Cleaning data...")

        def clean_numeric(value):
            try:
                # Remove any non-numeric characters except for '.' and convert to float
                clean_value = re.sub(r"[^\d.]", "", str(value)).strip()
                return float(clean_value) if clean_value else None
            except ValueError:
                return None

        # Apply cleaning to specific columns
        for col in ["Credit Amount", "Debit Amount", "Balance"]:
            if col in data.columns:
                data[col] = data[col].apply(clean_numeric)

        # Step 2: Validate required columns
        print("Validating data...")
        required_columns = ["Date", "Transaction Details", "Credit Amount", "Debit Amount", "Balance"]

        # Check if all required columns are present
        for column in required_columns:
            if column not in data.columns:
                raise ValueError(f"Required column '{column}' is missing!")

        # Remove rows with missing critical data
        data.dropna(subset=["Date", "Transaction Details", "Balance"], inplace=True)

        # Ensure at least one of 'Credit Amount' or 'Debit Amount' has data
        data = data.dropna(how="all", subset=["Credit Amount", "Debit Amount"])

        # Step 3: Save cleaned and validated data
        print("Saving cleaned and validated data...")
        data.to_csv(output_path, index=False)
        print(f"Data cleaning and validation completed. Output saved to {output_path}")

    except Exception as e:
        print(f"Error during data cleaning and validation: {e}")

if __name__ == "__main__":
    # Define input and output file paths
    input_file_path = "path_to_your_input_file.csv"  # Replace with your input file path
    output_file_path = "path_to_save_cleaned_validated_file.csv"  # Replace with your output file path

    # Run the cleaning and validation process
    clean_and_validate_data(input_file_path, output_file_path)
