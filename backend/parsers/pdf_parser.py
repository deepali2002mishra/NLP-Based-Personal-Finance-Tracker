import pdfplumber
import pandas as pd
from dateutil.parser import parse
from utils.classifier import categorize_transaction

def extract_table_row(row):
    """
    Extract transaction details from a table row.
    Handles missing or malformed rows gracefully.
    """
    try:
        date, description, amount = row[0], row[2], row[3]
        amount = float(amount.replace(",", "").strip()) if amount else None
        return date, description, amount
    except Exception as e:
        print(f"Error parsing row: {row} -> {e}")
        return None, None, None

def parse_pdf(file):
    """
    Process the PDF file in a memory-efficient manner.
    """
    transactions = []
    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                yield from process_page(page)
    except Exception as e:
        print(f"Error parsing PDF: {e}")
        raise e

def process_page(page):
    """
    Parse a single page of a PDF.
    """
    table = page.extract_table()
    if table:
        for row in table[1:]:  # Skip header
            try:
                date, description, amount = extract_table_row(row)
                if not date or not amount:
                    continue
                category = categorize_transaction(description)
                yield {
                    "Date": parse_date(date),
                    "Description": description,
                    "Amount": amount,
                    "Category": category,
                }
            except Exception as e:
                print(f"Error processing row: {row} -> {e}")

def parse_date(date_str):
    """
    Parse the date string into a proper date object.
    """
    try:
        return parse(date_str, dayfirst=True)
    except Exception as e:
        raise ValueError(f"Invalid date format: {date_str} -> {e}")
