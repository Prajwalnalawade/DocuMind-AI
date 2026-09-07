# DocuMind-AI
AI-powered document processing, extraction, validation and summarization platform.

DocuMind AI is an AI-powered document processing platform designed to automatically understand and analyze business documents such as invoices, quotations, receipts, and contracts.

The system combines PDF text extraction, OCR, Large Language Models (LLMs), structured data extraction, business-rule validation, and AI-generated summaries into a single automated pipeline.

Instead of manually reading and checking lengthy business documents, users can upload a document and receive structured information, validation results, financial analysis, important terms, warnings, and an AI-generated summary.

🚀 Features
📤 Document Upload

Upload business documents directly through the web interface.

Supported formats:

PDF
PNG
JPG
JPEG
🔎 Intelligent Text Extraction

DocuMind AI uses a two-stage extraction strategy:

Uploaded PDF
     │
     ▼
Native PDF Text Extraction
     │
     ├── Sufficient text ──► Use extracted text
     │
     └── Insufficient text
                │
                ▼
             OCR
                │
                ▼
          Extracted Text

For normal PDFs, the system extracts text directly.

For scanned/image-based PDFs, the system automatically falls back to Tesseract OCR.

🤖 AI Structured Extraction

The extracted document text is analyzed using an LLM and converted into structured information.

The system can extract:

Document type
Document title
Document number
Document date
Due date
Validity date
Vendor information
Customer information
Products/services
Quantities
Unit prices
Taxes
Discounts
Shipping charges
Subtotal
Total
Currency
Payment terms
Delivery terms
Contract terms
Additional notes
Confidence/uncertainty notes
🔍 Business Rule Validation

DocuMind AI doesn't simply trust the information extracted by the AI.

It performs deterministic validation checks such as:

Required information checks
Line-item calculations
Quantity × unit price validation
Subtotal validation
Tax information checks
Final total validation
Negative financial value detection
Quantity validation
Unit-price validation
Date consistency checks
Quotation validity checks

Example:

Quantity × Unit Price
        │
        ▼
Expected Amount
        │
        ▼
Compare with Document Amount
        │
        ├── Match ──────► PASS
        │
        └── Mismatch ───► ERROR
📊 Validation Score

Each analyzed document receives a validation score from 0–100%.

Possible statuses:

Status	Meaning
✅ VALID	No errors or warnings
⚠️ VALID WITH WARNINGS	No critical errors, but some warnings exist
❌ INVALID	One or more critical validation errors detected
🧠 AI Document Summary

After extraction and validation, DocuMind AI generates a human-readable summary containing:

Document overview
Document type
Parties involved
Key points
Products/services summary
Financial summary
Payment terms
Delivery terms
Important business terms
Warnings
Validation summary
Practical recommendation
🏗️ System Architecture

DocuMind AI follows a modular/layered architecture.

                        ┌──────────────────────┐
                        │      React UI        │
                        │      Frontend        │
                        └──────────┬───────────┘
                                   │
                                   ▼
                        ┌──────────────────────┐
                        │     FastAPI API      │
                        │      REST Layer      │
                        └──────────┬───────────┘
                                   │
                                   ▼
                  ┌────────────────────────────────┐
                  │       Application Services     │
                  │                                │
                  │ Document Service               │
                  │ Processing Service             │
                  │ Extraction Service             │
                  │ Validation Service             │
                  │ Summary Service                │
                  └───────────────┬────────────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    ▼                           ▼
          ┌──────────────────┐       ┌──────────────────┐
          │ Document         │       │ LLM Infrastructure│
          │ Processing       │       │                  │
          │                  │       │ OpenAI Client   │
          │ PyMuPDF          │       │ Structured Output│
          │ Tesseract OCR    │       │ Prompt Layer    │
          └──────────────────┘       └────────┬─────────┘
                                              │
                                              ▼
                                      ┌───────────────┐
                                      │     LLM       │
                                      └───────────────┘

                        Validation
                            │
                            ▼
                  ┌─────────────────────┐
                  │ Business Rule Engine│
                  └─────────────────────┘
🔄 Complete Processing Pipeline
                Upload Document
                       │
                       ▼
              File Validation
                       │
                       ▼
               Store Document
                       │
                       ▼
              Text Extraction
                       │
             ┌─────────┴─────────┐
             │                   │
          PDF Text              OCR
             │                   │
             └─────────┬─────────┘
                       ▼
                Extracted Text
                       │
                       ▼
              LLM Structured
                 Extraction
                       │
                       ▼
             Structured Document
                       │
                       ▼
             Business Validation
                       │
                       ▼
             Validation Results
                       │
                       ▼
               AI Summarization
                       │
                       ▼
              Complete Analysis
                       │
                       ▼
                  React UI
🛠️ Technology Stack
Frontend
React
Vite
JavaScript
Axios
CSS
Backend
Python
FastAPI
Pydantic
Uvicorn
AI / Machine Learning
Large Language Model (LLM)
Structured LLM output
Prompt engineering
AI-powered document understanding
Document Processing
PyMuPDF
Tesseract OCR
pytesseract
Pillow
Development
Git
GitHub
VS Code
REST API
Swagger / OpenAPI


