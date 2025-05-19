from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import base64
from pathlib import Path
import tempfile
import json
import csv
import uuid
from datetime import datetime

from mistralai import Mistral
from mistralai import DocumentURLChunk, ImageURLChunk, TextChunk # Corrected import
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("MISTRAL_API_KEY")
if not api_key:
    raise ValueError("MISTRAL_API_KEY not found in .env file")

# Initialize Mistral client
client = Mistral(api_key=api_key)

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True) # Added supports_credentials

# Configure upload settings
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
TEMP_FOLDER = tempfile.gettempdir()
RESULTS_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")

# Create results folder if it doesn't exist
if not os.path.exists(RESULTS_FOLDER):
    os.makedirs(RESULTS_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_pdf(file_path):
    """Process a PDF file with OCR"""
    pdf_file = Path(file_path)
    
    uploaded_file = client.files.upload(
        file={
            "file_name": pdf_file.stem,
            "content": pdf_file.read_bytes(),
        },
        purpose="ocr",
    )
    
    signed_url = client.files.get_signed_url(file_id=uploaded_file.id, expiry=1)
    
    pdf_response = client.ocr.process(
        document=DocumentURLChunk(document_url=signed_url.url),
        model="mistral-ocr-latest"
    )
    
    all_markdown = ""
    for page in pdf_response.pages:
        all_markdown += page.markdown + "\n\n"
    
    return all_markdown

def process_image(file_path):
    """Process an image file with OCR"""
    image_file = Path(file_path)
    
    encoded = base64.b64encode(image_file.read_bytes()).decode()
    base64_data_url = f"data:image/jpeg;base64,{encoded}" # Assuming jpeg, could be more dynamic
    
    image_response = client.ocr.process(
        document=ImageURLChunk(image_url=base64_data_url),
        model="mistral-ocr-latest"
    )
    
    return image_response.pages[0].markdown

def extract_structured_data(ocr_markdown):
    """Extract structured financial invoice data from OCR results"""
    
    chat_response = client.chat.complete(
        model="pixtral-12b-latest",
        messages=[
            {
                "role": "user",
                "content": [
                    TextChunk(
                        text=(
                            f"This is a financial invoice's OCR in markdown:\n\n{ocr_markdown}\n\n"
                            "Extract all financial information in a structured JSON format. "
                            "The JSON should include these top-level keys: 'invoice_details', 'line_items', and 'summary'.\n"
                            "1. 'invoice_details': an object with 'vendor_name' (string), 'invoice_number' (string), 'invoice_date' (string, ideally YYYY-MM-DD), 'due_date' (string, ideally YYYY-MM-DD, null if not found), and 'currency' (string, e.g., USD, EUR). \n"
                            "2. 'line_items': an array of objects. Each object represents a line item and must include 'description' (string), 'quantity' (number), 'unit_price' (number), and 'line_total' (number). If a numeric field cannot be determined, use null.\n"
                            "3. 'summary': an object with 'subtotal' (number), 'tax_amount' (number, could be a sum of multiple taxes), and 'total_amount' (number). If a numeric field cannot be determined, use null.\n"
                            "If any string field is missing, use null or an empty string. "
                            "The output should be strictly JSON with no extra commentary or explanations."
                        )
                    ),
                ],
            }
        ],
        response_format={"type": "json_object"},
        temperature=0,
    )
    
    try:
        response_dict = json.loads(chat_response.choices[0].message.content)
        
        # Standardize the response structure to ensure all keys are present
        standardized_response = {
            "invoice_details": response_dict.get("invoice_details", {}),
            "line_items": response_dict.get("line_items", []),
            "summary": response_dict.get("summary", {})
        }

        # Ensure default keys for invoice_details
        details_defaults = {"vendor_name": None, "invoice_number": None, "invoice_date": None, "due_date": None, "currency": None}
        for key, default_val in details_defaults.items():
            standardized_response["invoice_details"].setdefault(key, default_val)

        # Ensure default keys for summary
        summary_defaults = {"subtotal": None, "tax_amount": None, "total_amount": None}
        for key, default_val in summary_defaults.items():
            standardized_response["summary"].setdefault(key, default_val)
            
        # Ensure default keys for each line item
        sanitized_line_items = []
        item_defaults = {"description": None, "quantity": None, "unit_price": None, "line_total": None}
        if isinstance(standardized_response["line_items"], list):
            for item in standardized_response["line_items"]:
                if isinstance(item, dict):
                    new_item = {}
                    for key, default_val in item_defaults.items():
                        new_item[key] = item.get(key, default_val)
                    sanitized_line_items.append(new_item)
        standardized_response["line_items"] = sanitized_line_items
        
        return standardized_response
        
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        print(f"LLM Response: {chat_response.choices[0].message.content}")
        return {"error": "Failed to parse structured data from AI. The format might be incorrect.", 
                "invoice_details": {}, "line_items": [], "summary": {}}
    except Exception as e:
        print(f"General Error in extract_structured_data: {e}")
        return {"error": str(e), "invoice_details": {}, "line_items": [], "summary": {}}


def save_to_csv(data, filename):
    """Save invoice data to CSV file"""
    filepath = os.path.join(RESULTS_FOLDER, filename)
    
    invoice_details = data.get("invoice_details", {})
    line_items = data.get("line_items", [])
    summary = data.get("summary", {})

    fieldnames = [
        'invoice_number', 'invoice_date', 'due_date', 'vendor_name', 'currency',
        'item_description', 'item_quantity', 'item_unit_price', 'item_line_total',
        'subtotal', 'tax_amount', 'grand_total'
    ]
    
    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        if not line_items: # Handle case with no line items, but potentially summary data
            row_data = {
                'invoice_number': invoice_details.get('invoice_number', ''),
                'invoice_date': invoice_details.get('invoice_date', ''),
                'due_date': invoice_details.get('due_date', ''),
                'vendor_name': invoice_details.get('vendor_name', ''),
                'currency': invoice_details.get('currency', ''),
                'item_description': '', 
                'item_quantity': '',
                'item_unit_price': '',
                'item_line_total': '',
                'subtotal': summary.get('subtotal', ''),
                'tax_amount': summary.get('tax_amount', ''),
                'grand_total': summary.get('total_amount', '')
            }
            writer.writerow(row_data)
        else:
            for item in line_items:
                row_data = {
                    'invoice_number': invoice_details.get('invoice_number', ''),
                    'invoice_date': invoice_details.get('invoice_date', ''),
                    'due_date': invoice_details.get('due_date', ''),
                    'vendor_name': invoice_details.get('vendor_name', ''),
                    'currency': invoice_details.get('currency', ''),
                    'item_description': item.get('description', ''),
                    'item_quantity': item.get('quantity', ''),
                    'item_unit_price': item.get('unit_price', ''),
                    'item_line_total': item.get('line_total', ''),
                    'subtotal': summary.get('subtotal', ''),
                    'tax_amount': summary.get('tax_amount', ''),
                    'grand_total': summary.get('total_amount', '')
                }
                writer.writerow(row_data)
    
    return filepath

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process-report', methods=['POST'])
def process_report():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    if not allowed_file(file.filename):
        return jsonify({"error": f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"}), 400
    
    file_path = None # Initialize to ensure it's defined for finally block
    try:
        filename = secure_filename(file.filename)
        file_path = os.path.join(TEMP_FOLDER, filename)
        file.save(file_path)
        
        file_extension = filename.rsplit('.', 1)[1].lower()
        
        if file_extension == 'pdf':
            ocr_markdown = process_pdf(file_path)
        else:
            ocr_markdown = process_image(file_path)
        
        if not ocr_markdown:
             return jsonify({"error": "OCR processing failed to extract any text."}), 500

        structured_data = extract_structured_data(ocr_markdown)
        
        if "error" in structured_data and structured_data["error"]: # Check if extraction itself returned an error message
             return jsonify({"error": structured_data["error"]}), 500

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        csv_filename = f"invoice_data_{timestamp}_{unique_id}.csv"
        
        save_to_csv(structured_data, csv_filename) # Save the full structured data
        
        structured_data["csv_filename"] = csv_filename
        
        return jsonify(structured_data)
    
    except Exception as e:
        app.logger.error(f"Error processing report: {str(e)}", exc_info=True)
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
    finally:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)


@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        safe_filename = secure_filename(filename) # Sanitize filename
        file_to_send = os.path.join(RESULTS_FOLDER, safe_filename)
        if not os.path.exists(file_to_send) or not os.path.isfile(file_to_send): # Security check
            return jsonify({"error": "File not found or invalid."}), 404

        return send_file(file_to_send,
                         mimetype='text/csv',
                         as_attachment=True,
                         download_name=safe_filename) # Use sanitized name for download
    except Exception as e:
        app.logger.error(f"Error downloading file {filename}: {str(e)}", exc_info=True)
        return jsonify({"error": "Could not download file."}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)