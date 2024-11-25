import requests
import os
import pandas as pd
from utils.insights import generate_charts

def test_health_check():
    """
    Test the health check endpoint.
    """
    url = "http://127.0.0.1:5000/health"
    response = requests.get(url)
    if response.status_code == 200 and response.json().get("status") == "Server is running!":
        print("Health check test passed!")
    else:
        print("Health check test failed!")
        print("Response:", response.text)

def test_upload_file():
    """
    Test the file upload endpoint with a sample PDF.
    """
    url = "http://127.0.0.1:5000/upload"
    file_path = os.path.join(os.path.dirname(__file__), "test_data", r"C:\Users\Deepali Mishra\Downloads\920010035775074 (2).pdf")
    
    if not os.path.exists(file_path):
        print(f"Test file not found: {file_path}")
        return
    
    with open(file_path, "rb") as file:
        files = {"file": file}
        response = requests.post(url, files=files)

    if response.status_code == 200:
        data = response.json()
        print("File upload test passed!")
        print("Response:")
        print(data)
    else:
        print("File upload test failed!")
        print("Response:", response.text)

def test_chart_generation():
    """
    Test if the chart files are being generated and saved correctly in the static directory.
    """
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    os.makedirs(static_dir, exist_ok=True)

    charts = ["pie_chart.png", "bar_chart.png", "line_chart.png"]
    for chart in charts:
        chart_path = os.path.join(static_dir, chart)
        if os.path.exists(chart_path):
            os.remove(chart_path)  # Clear pre-existing charts

    # Dummy data for testing
    dummy_data = pd.DataFrame({
        "Category": ["Food", "Shopping", "Utilities"],
        "Amount": [100, 200, 150],
        "Date": pd.date_range(start="2024-01-01", periods=3)
    })
    generate_charts(dummy_data, output_dir=static_dir)

    # Check if charts are generated
    all_exist = all(os.path.exists(os.path.join(static_dir, chart)) for chart in charts)
    if all_exist:
        print("Chart generation test passed!")
    else:
        print("Chart generation test failed!")

def run_tests():
    """
    Run all backend tests.
    """
    print("Running health check test...")
    test_health_check()
    
    print("\nRunning file upload test...")
    test_upload_file()
    
    print("\nChecking chart generation...")
    test_chart_generation()

if __name__ == "__main__":
    run_tests()
