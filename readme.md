# AI-Powered Legal Documentation Assistant

## Overview

AI-Powered Legal Documentation Assistant is an AI-driven web application designed to simplify the analysis, understanding, and generation of legal documents. It enables users to upload legal contracts, automatically summarize content, identify important legal clauses, detect potential risks, receive AI-powered improvement suggestions, interact with a legal chatbot, generate downloadable reports, and create new legal documents with ease.

The application is built using **Python**, **Flask**, **SQLite**, and the **Groq API** with the **Llama 3.1 8B Instant** model.

---

## Features

- 🔐 User Registration and Secure Login
- 👤 User Authentication & Session Management
- 📄 Upload Legal Documents (PDF)
- 🤖 AI-Powered Document Summarization
- 📑 Automatic Legal Clause Detection
- ⚠️ Risk Analysis and Identification
- 💡 AI-Based Improvement Suggestions
- 💬 Legal AI Chat Assistant
- 📥 PDF Report Generation
- 📝 Automatic Legal Document Generation
- 📊 Interactive User Dashboard
- 📂 Document Management

---

## Technologies Used

### Frontend
- HTML5
- CSS3
- JavaScript
- Tailwind CSS
- Jinja2 Templates

### Backend
- Python
- Flask
- Flask-SQLAlchemy
- Flask-Login

### Database
- SQLite

### Artificial Intelligence
- Groq API
- Llama 3.1 8B Instant

### PDF Processing
- PyPDF2
- ReportLab

### Security
- Werkzeug Password Hashing
- Flask Session Management

---

## Project Structure

```
AI-Powered-Legal-Documentation-Assistant/
│
├── app.py
├── config.py
├── requirements.txt
├── .env
├── README.md
│
├── static/
│   ├── css/
│   ├── js/
│   └── uploads/
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── upload.html
│   ├── chatbot.html
│   └── report.html
│
├── utils/
│   ├── pdf_extractor.py
│   ├── summarizer.py
│   ├── clause_detector.py
│   ├── risk_analyzer.py
│   ├── chatbot.py
│   ├── document_generator.py
│   ├── improvement_suggester.py
│   └── report_generator.py
│
├── instance/
│   └── users.db
│
└── generated_reports/
```

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/your-username/AI-Powered-Legal-Documentation-Assistant.git
```

### Navigate to the Project

```bash
cd AI-Powered-Legal-Documentation-Assistant
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file and add your Groq API key:

```env
GROQ_API_KEY=your_api_key_here
SECRET_KEY=your_secret_key
```

### Run the Application

```bash
python app.py
```

Open your browser and visit:

```
http://127.0.0.1:5000
```

---

## Workflow

1. Register or log in to the system.
2. Upload a legal PDF document.
3. Extract text from the document.
4. Generate an AI-powered summary.
5. Detect legal clauses automatically.
6. Analyze risks in the document.
7. Receive AI-based improvement suggestions.
8. Chat with the Legal AI Assistant.
9. Generate and download a PDF report.
10. Create new legal documents using AI.

---

## Future Enhancements

- Support for DOCX and TXT files
- OCR for scanned legal documents
- Multi-language legal document support
- Voice-based legal assistant
- Advanced legal analytics dashboard
- Cloud storage integration
- Role-based access control
- Digital signature support

---

## Security Features

- Password Hashing using Werkzeug
- Secure User Authentication
- Session Management
- Protected User Routes
- Secure File Upload Validation
- API Key Protection using Environment Variables

---

## Author

**Developed by:** Wootla Jaya sri

---

## License

This project is developed for educational and academic purposes.
