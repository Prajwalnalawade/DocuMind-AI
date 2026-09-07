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



🔤 Tesseract OCR Setup

DocuMind AI uses Tesseract for scanned documents.

Install Tesseract OCR on your system and make sure the executable path matches:

C:\Program Files\Tesseract-OCR\tesseract.exe

You can change the path using:

TESSERACT_CMD=your_tesseract_path
▶️ Run the Backend

From the backend directory:

uvicorn app.main:app --reload

The API will normally be available at:

http://127.0.0.1:8000

Swagger API documentation:

http://127.0.0.1:8000/docs
⚛️ Frontend Setup

Open another terminal.

cd frontend

Install dependencies:

npm install

Start the development server:

npm run dev

The frontend will normally be available at:

http://localhost:5173
🔌 API Endpoints
Method	Endpoint	Purpose
POST	/api/documents/upload	Upload document
GET	/api/documents/{id}/text	Extract document text
POST	/api/documents/{id}/extract	Extract structured information
POST	/api/documents/{id}/validate	Validate extracted information
POST	/api/documents/{id}/summary	Complete AI document analysis
🧪 Example Workflow
Step 1 — Upload
POST /api/documents/upload

The API returns a document ID.

Step 2 — Analyze
POST /api/documents/{document_id}/summary

The system then performs:

PDF/OCR
   ↓
Text Extraction
   ↓
LLM Extraction
   ↓
Validation
   ↓
AI Summary
📊 Example Output

A document analysis can contain:

{
  "document_type": "quotation",
  "document_number": "QT-1024",
  "document_date": "2026-08-20",

  "vendor": {
    "name": "Example Technologies"
  },

  "totals": {
    "subtotal": 50000,
    "tax": 9000,
    "total": 59000,
    "currency": "INR"
  },

  "validation": {
    "status": "valid",
    "score": 100
  }
}
💡 Why DocuMind AI?

Traditional document processing often requires employees to manually:

Read documents
Find important information
Enter data into systems
Verify calculations
Check dates
Review terms
Prepare summaries

DocuMind AI aims to automate these repetitive tasks.

Traditional Process
Document
   ↓
Manual Reading
   ↓
Manual Data Entry
   ↓
Manual Verification
   ↓
Manual Summary
DocuMind AI
Document
   ↓
AI Processing
   ↓
Structured Data
   ↓
Automated Validation
   ↓
AI Summary
🎯 Use Cases

DocuMind AI can be useful for:

Accounts payable automation
Invoice processing
Procurement workflows
Vendor document analysis
Quotation comparison
Contract document review
Business document digitization
Document compliance workflows
Internal document processing systems
🔐 Security Considerations

DocuMind AI is designed with basic security considerations such as:

Environment-based API key configuration
.env excluded from Git
Uploaded documents excluded from Git
File extension validation
Maximum upload size configuration
Structured LLM output
Deterministic business-rule validation

For production deployment, additional security measures should be implemented, including:

Authentication and authorization
Rate limiting
Secure file storage
Malware scanning
Encryption
Database access controls
Audit logging
Secret management
🔮 Future Enhancements

Planned improvements include:

 Document history
 Database persistence
 User authentication
 Multiple document comparison
 Advanced contract analysis
 Table extraction
 Multi-language OCR
 Confidence scoring for extracted fields
 Document search
 Export analysis to PDF/Excel
 Analytics dashboard
 Cloud deployment
 Role-based access control
 Audit logs
 Docker-based deployment
 Automated testing
 CI/CD pipeline
🧩 Project Architecture Principles

The project follows a modular architecture where responsibilities are separated into different layers.

API Layer

Handles HTTP requests and responses.

Service Layer

Contains application/business workflows.

Schema Layer

Defines structured data models using Pydantic.

Infrastructure Layer

Handles external technologies such as:

PDF processing
OCR
LLM providers

This separation makes the system easier to:

Maintain
Test
Extend
Debug
Replace individual technologies

For example, the LLM infrastructure can be changed without requiring the entire application to be rewritten.

🧑‍💻 Development

Create a new branch for major features:

git checkout -b feature/document-history

After making changes:

git add .
git commit -m "Add document history"
git push -u origin feature/document-history

For normal updates to main:

git add .
git commit -m "Update document analysis"
git push
📜 License

This project is currently intended for educational, portfolio, and academic purposes.

A formal open-source license can be added later if the project is intended for public reuse.

👨‍💻 Author

Prajwal Nalawade

GitHub: Prajwalnalawade

⭐ Project Highlights

DocuMind AI combines:

OCR + PDF Processing + LLM + Structured Extraction + Business Validation + AI Summarization

into a single document intelligence pipeline.
