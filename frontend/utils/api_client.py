import requests
import os

API_URL = "http://127.0.0.1:5000"

def upload_pdf(file):
    try:
        files = {"file": file}
        response = requests.post(f"{API_URL}/upload", files=files)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def get_chart_path(chart_name):
    static_dir = os.path.join(os.path.dirname(__file__), r"D:\Projects\personal-finance-tracker\backend\static")
    chart_path = os.path.join(static_dir, f"{chart_name}.png")
    
    if not os.path.exists(chart_path):
        raise FileNotFoundError(f"{chart_name}.png not found in {static_dir}")
    
    return chart_path
