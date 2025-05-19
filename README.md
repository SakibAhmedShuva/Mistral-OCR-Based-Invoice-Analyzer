# 🧾 Mistral OCR-Based Financial Invoice Analyzer

<div align="center">

![Invoice Analyzer Banner](https://via.placeholder.com/1200x300/0078D7/ffffff?text=Mistral+OCR+Invoice+Analyzer)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.0%2B-brightgreen)](https://flask.palletsprojects.com/)
[![Mistral AI](https://img.shields.io/badge/Powered%20by-Mistral_AI-purple)](https://mistral.ai/)

**Turn paper invoices into structured data with the power of AI**

[Features](#-features) • [Installation](#%EF%B8%8F-installation--setup) • [Usage](#-usage) • [API](#-api-endpoints) • [Contributing](#-contributing)

</div>

---

## 📋 Overview

A modern web application that harnesses Mistral AI's OCR and language models to automatically extract structured data from financial invoices. Simply upload a PDF or image of an invoice, and watch as the AI identifies key details like vendor information, invoice numbers, dates, line items, and totals – all presented in a user-friendly format with CSV export functionality.

**Project Repository:** [https://github.com/SakibAhmedShuva/Mistral-OCR-Based-Invoice-Analyzer](https://github.com/SakibAhmedShuva/Mistral-OCR-Based-Invoice-Analyzer)

![image](https://github.com/user-attachments/assets/ca6d2a4d-1576-4766-a1b7-25543a94a7c7)


---

## 🌟 Features

<div align="center">
  <table>
    <tr>
      <td width="50%">
        <h3 align="center">📸 OCR Processing</h3>
        <p>Handles PDFs and images (PNG, JPG, JPEG) with advanced text recognition</p>
      </td>
      <td width="50%">
        <h3 align="center">🤖 AI-Powered Extraction</h3>
        <p>Uses Mistral AI's <code>pixtral-12b-latest</code> model for intelligent parsing</p>
      </td>
    </tr>
    <tr>
      <td width="50%">
        <h3 align="center">📊 Structured Output</h3>
        <p>Extracts vendor details, invoice numbers, dates, line items, and financial totals</p>
      </td>
      <td width="50%">
        <h3 align="center">📤 CSV Export</h3>
        <p>Download extracted data for seamless integration with accounting systems</p>
      </td>
    </tr>
    <tr>
      <td width="50%">
        <h3 align="center">📱 Responsive Design</h3>
        <p>User-friendly interface that works on any device</p>
      </td>
      <td width="50%">
        <h3 align="center">🔄 Error Handling</h3>
        <p>Clear feedback during processing with comprehensive error reporting</p>
      </td>
    </tr>
  </table>
</div>

### Data Extraction Capabilities

The system automatically identifies and extracts:

- **Vendor Information**: Company name and details
- **Invoice Metadata**: Invoice number, dates (issue & due)
- **Currency**: Automatically detects the invoice currency
- **Line Items**: Detailed breakdown with descriptions, quantities, unit prices, and line totals
- **Financial Summary**: Subtotals, tax amounts, and total invoice value

---

## 🛠️ Technology Stack

<div align="center">
  <table>
    <tr>
      <th>Backend</th>
      <th>Frontend</th>
      <th>Libraries & Tools</th>
    </tr>
    <tr>
      <td>
        <ul>
          <li>Python 3.x</li>
          <li>Flask (Web framework)</li>
          <li>Mistral AI Python Client</li>
        </ul>
      </td>
      <td>
        <ul>
          <li>HTML5</li>
          <li>CSS3 with Variables</li>
          <li>Vanilla JavaScript</li>
        </ul>
      </td>
      <td>
        <ul>
          <li><code>python-dotenv</code></li>
          <li><code>Werkzeug</code></li>
          <li><code>flask-cors</code></li>
          <li>Font Awesome</li>
          <li>Google Fonts (Poppins)</li>
        </ul>
      </td>
    </tr>
  </table>
</div>

---

## ⚙️ Prerequisites

Before beginning, please ensure you have:

- **Python**: Version 3.8 or higher
- **pip**: Python package installer
- **Mistral AI API Key**: Register at [Mistral AI](https://mistral.ai/) to obtain your key
- **Git**: For cloning the repository
- *(Optional)* A virtual environment tool like `venv` or `conda`

---

## 🚀 Installation & Setup

<div align="center">
  
### Quick Setup

</div>

1. **Clone the repository**
   ```bash
   git clone https://github.com/SakibAhmedShuva/Mistral-OCR-Based-Invoice-Analyzer.git
   cd Mistral-OCR-Based-Invoice-Analyzer
   ```

2. **Create and activate a virtual environment**
   ```bash
   # Using venv
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```
   
   <details>
   <summary>Using conda instead?</summary>
   
   ```bash
   conda create -n invoice_analyzer python=3.9
   conda activate invoice_analyzer
   ```
   </details>

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your environment**
   
   Create a file named `.env` in the project root:
   ```
   MISTRAL_API_KEY="YOUR_MISTRAL_API_KEY_HERE"
   ```

---

## ▶️ Running the Application

1. Ensure your virtual environment is activated
2. Launch the Flask application:
   ```bash
   python app.py
   ```
3. Access the web interface at [http://localhost:5000](http://localhost:5000)

<div align="center">
  
  ![Terminal Output](https://via.placeholder.com/650x150/f5f5f5/333333?text=Terminal+Output+Preview)
  
  *You should see output similar to this in your terminal*
</div>

---

## 📄 Usage

<div align="center">
  <img src="https://via.placeholder.com/800x400/f1f1f1/333333?text=Application+Interface" alt="Application Interface" width="80%"/>
</div>

### Processing an Invoice

1. **Upload an Invoice**
   - Drag & drop a file onto the upload area, or
   - Click "Select File" to browse for a document (PDF, JPG, PNG)

2. **View Extracted Data**
   - Line items displayed in a structured table
   - Summary section shows vendor details, invoice numbers, and totals

3. **Export & Continue**
   - Download results as CSV for accounting systems
   - Upload another invoice with the "New Upload" button

---

## 🌐 API Endpoints

The application exposes these RESTful endpoints:

<div align="center">
  <table>
    <tr>
      <th>Endpoint</th>
      <th>Method</th>
      <th>Description</th>
    </tr>
    <tr>
      <td><code>/</code></td>
      <td>GET</td>
      <td>Serves the main application interface</td>
    </tr>
    <tr>
      <td><code>/process-report</code></td>
      <td>POST</td>
      <td>Handles file upload, OCR, and data extraction</td>
    </tr>
    <tr>
      <td><code>/download/&lt;filename&gt;</code></td>
      <td>GET</td>
      <td>Downloads the generated CSV file</td>
    </tr>
  </table>
</div>

### Sample Response (Success)

```json
{
    "invoice_details": {
        "vendor_name": "Example Vendor Inc.",
        "invoice_number": "INV-2024-001",
        "invoice_date": "2024-01-15",
        "due_date": "2024-02-14",
        "currency": "USD"
    },
    "line_items": [
        {
            "description": "Product A - Advanced Widget",
            "quantity": 2,
            "unit_price": 75.50,
            "line_total": 151.00
        },
        {
            "description": "Service B - Consultation",
            "quantity": 1,
            "unit_price": 120.00,
            "line_total": 120.00
        }
    ],
    "summary": {
        "subtotal": 271.00,
        "tax_amount": 21.68,
        "total_amount": 292.68
    },
    "csv_filename": "invoice_data_20240315_103045_a1b2c3d4.csv"
}
```

---

## 📁 Project Structure

```
Mistral-OCR-Based-Invoice-Analyzer/
├── app.py                # Main Flask application logic
├── templates/
│   └── index.html        # Frontend HTML, CSS, and JavaScript
├── results/              # Directory for storing generated CSVs
├── .env                  # Environment variables (create manually)
├── requirements.txt      # Python dependencies
└── README.md            # Project documentation
```

---

## 💡 Troubleshooting

<details>
<summary><b>Common Issues & Solutions</b></summary>

### API Key Problems
- **Issue**: `MISTRAL_API_KEY not found` error
- **Solution**: Ensure your `.env` file exists and contains the correct API key

### Server Startup Issues
- **Issue**: Port already in use
- **Solution**: Modify `app.run()` in `app.py` to use a different port:
  ```python
  app.run(debug=True, host='0.0.0.0', port=5001)
  ```

### Dependency Errors
- **Issue**: Module not found errors
- **Solution**: Verify your virtual environment is activated before installing dependencies

### OCR Quality Issues
- **Issue**: Poor extraction results
- **Solution**: Ensure invoice images are clear, well-lit, and properly aligned
</details>

---

## 🤝 Contributing

Contributions are welcome and appreciated! Here's how you can help:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/AmazingFeature`
3. Commit your changes: `git commit -m 'Add some AmazingFeature'`
4. Push to the branch: `git push origin feature/AmazingFeature`
5. Open a Pull Request

<details>
<summary><b>Contribution Guidelines</b></summary>

- Follow the existing code style
- Add comments to explain complex logic
- Update documentation as needed
- Add tests for new features
- Ensure all tests pass before submitting
</details>

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

---

## 🙏 Acknowledgements

- [Mistral AI](https://mistral.ai/) for their powerful OCR and language models
- The Flask community for the excellent web framework
- Font Awesome for the beautiful icons

---

<div align="center">
  <p>
    <b>Created and maintained by <a href="https://github.com/SakibAhmedShuva">Sakib Ahmed Shuva</a></b>
  </p>
  
  <p>
    <a href="#-mistral-ocr-based-financial-invoice-analyzer">Back to top ↑</a>
  </p>
</div>
