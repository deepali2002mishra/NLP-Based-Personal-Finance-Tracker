# Personal Finance Tracker 📊💰

A comprehensive web-based tool for managing and analyzing personal finances. This project allows users to upload bank statement PDFs, categorize transactions using machine learning, and visualize spending habits through charts and insights. It is designed to help users better understand their financial patterns and improve budgeting.

---

## **Features**
- **PDF Parsing**: Extracts transaction data (date, description, amount) from uploaded PDF bank statements.
- **Transaction Categorization**: Automatically categorizes transactions into predefined categories using a trained machine learning model.
- **Visual Insights**: Generates bar and line charts for spending by category and over time, respectively.
- **Spending Insights**:
  - Total spending
  - Average spending
  - Monthly breakdown of expenditures
  - Highest transaction details
- **Scalable Backend**: Modular design for efficient data processing, model training, and evaluation.
- **Frontend Interface**: Simple and intuitive web-based interface for user interaction.

---

## Getting Started

### Prerequisites

- Python 3.8 or above
- Required Python libraries (install using `pip install -r requirements.txt`):
  - `pandas`
  - `pdfplumber`
  - `scikit-learn`
  - `matplotlib`
  - `python-dateutil`

### Installation and Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/personal-finance-tracker.git
   cd personal-finance-tracker
