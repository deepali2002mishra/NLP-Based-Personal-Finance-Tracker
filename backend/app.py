import os
import logging
import pandas as pd 
from flask import Flask, request, jsonify, send_from_directory
from utils.insights import generate_charts, spending_analysis
from parsers.pdf_parser import parse_pdf

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Static directory for serving generated charts
STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static')
os.makedirs(STATIC_DIR, exist_ok=True)

@app.route('/static/<path:filename>')
def static_files(filename):
    """
    Serves static files like generated charts.
    """
    return send_from_directory(STATIC_DIR, filename)

@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Endpoint to upload a PDF file and generate transaction insights.
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file.content_length > 10 * 1024 * 1024:  # Limit file size to 10MB
        return jsonify({"error": "File too large"}), 413

    try:
        logger.info("Parsing PDF file...")
        # Consume generator and convert to DataFrame
        transactions = list(parse_pdf(file))
        transactions_df = pd.DataFrame(transactions)

        if transactions_df.empty:
            return jsonify({"error": "No valid transactions found"}), 400

        # Generate charts and insights
        generate_charts(transactions_df, output_dir=STATIC_DIR)
        insights = spending_analysis(transactions_df)
        return jsonify({
            "analysis": insights,
            "charts": {
                "bar_chart": "/static/bar_chart.png",
                "line_chart": "/static/line_chart.png"
            }
        })
    except Exception as e:
        logger.error(f"Error processing file: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint to verify server status.
    """
    return jsonify({"status": "Server is running!"}), 200

if __name__ == '__main__':
    app.run(debug=True)
