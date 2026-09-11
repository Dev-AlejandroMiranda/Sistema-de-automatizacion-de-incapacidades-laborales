# ⚙️ Sick Leave Automated Data Extraction System

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Status](https://img.shields.io/badge/Status-In_Development-orange)
![License](https://img.shields.io/badge/License-MIT-green)

A Python-based automation solution designed to extract, validate, and structure data from medical sick leave documents. Built to eliminate manual data entry for HR, Payroll, and Operations teams.

---

## 🎯 The Problem It Solves
Manual transcription of medical certificates is slow, prone to human error, and creates bottlenecks in payroll processing. This system normalizes incoming document data and outputs structured formats (JSON/CSV/Database) ready for ERP and HR system integration.

---

## ✨ Current Features
- 📥 **Document Ingestion:** Automated ingestion and parsing of input files.
- 🔍 **Key Field Extraction:** Automatic parsing of employee IDs, leave duration, start/end dates, and diagnostic codes (ICD-10/CIE-10).
- ⚙️ **Data Validation:** Rule-based verification to ensure date consistency and required field checks.
- 📊 **Structured Output:** Converts unstructured inputs into clean JSON schemas and tabular data.

---

## 🛠️ Tech Stack
- **Core:** Python 3.10+
- **Data Processing:** Pandas, Regex, JSON
- **Architecture:** Modular, extensible data pipeline

---

## 🚀 Roadmap
- [x] Input ingestion and structured parsing engine
- [x] Data validation and normalization rules
- [ ] 🔄 **OCR Engine Integration:** `pytesseract` / `EasyOCR` implementation for scanned PDFs and image processing
- [ ] 🌐 **REST API:** FastAPI endpoint wrapper for seamless system integration
- [ ] 🐳 **Containerization:** Docker container for rapid deployment

---

## 📦 Quick Start

```bash
# 1. Clone repository
git clone [https://github.com/Dev-AlejandroMiranda/Sistema-de-automatizacion-de-incapacidades-laborales.git](https://github.com/Dev-AlejandroMiranda/Sistema-de-automatizacion-de-incapacidades-laborales.git)

# 2. Navigate to directory
cd Sistema-de-automatizacion-de-incapacidades-laborales

# 3. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run execution script
python main.py
