# LegalWise Document Summarizer Microservice

[![Python](https://img.shields.io/badge/Python-3.8+-blue)](https://python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green)](https://fastapi.tiangolo.com/)
[![Google AI](https://img.shields.io/badge/Google-Gemini%20AI-blue)](https://ai.google.dev/)

AI-powered microservice for document summarization using Google's Gemini AI. Provides intelligent analysis and summarization of legal documents.

## ✨ Features

- **AI-Powered Summarization** - Google Gemini AI for intelligent document analysis
- **Multi-Format Support** - PDF, DOCX, TXT, and image files
- **Key Points Extraction** - Automatic identification of important information
- **Legal Context** - Specialized for legal document analysis
- **RESTful API** - FastAPI framework for high performance
- **CORS Support** - Cross-origin requests enabled
- **Error Handling** - Comprehensive error responses

## 📋 Prerequisites

- **Python:** 3.8 or higher
- **pip:** Latest version
- **Google Gemini API Key** - Get from [Google AI Studio](https://makersuite.google.com/app/apikey)

## 🛠️ Installation

### 1. Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the summarizerMicroService directory:

```bash
GEMINI_API_KEY=your-gemini-api-key-here
```

### 4. Run the Service
```bash
# Development mode with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

The service will start on `http://localhost:8000`

## 📁 Project Structure

```
summarizerMicroService/
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables
└── README.md
```

## 🔗 API Endpoints

### Health Check
**GET** `/`

Check if the service is running.

**Response:**
```json
{
  "status": "healthy",
  "service": "Document Summarizer Microservice",
  "version": "1.0.0"
}
```

### Summarize Document
**POST** `/summarize`

Summarize a document using AI.

**Request Body:**
```json
{
  "text": "Your document text here...",
  "max_length": 500
}
```

**Parameters:**
- `text` (string, required) - The document text to summarize
- `max_length` (integer, optional) - Maximum length of summary (default: 500)

**Response (200):**
```json
{
  "summary": "AI-generated summary of the document...",
  "key_points": [
    "Important point 1",
    "Important point 2",
    "Important point 3"
  ],
  "word_count": {
    "original": 1500,
    "summary": 250
  }
}
```

**Error Response (400):**
```json
{
  "error": "Text is required for summarization"
}
```

**Error Response (500):**
```json
{
  "error": "Failed to generate summary",
  "details": "Error message from AI service"
}
```

### Analyze Document
**POST** `/analyze`

Perform detailed analysis of a legal document.

**Request Body:**
```json
{
  "text": "Legal document text...",
  "analysis_type": "legal"
}
```

**Parameters:**
- `text` (string, required) - The document text to analyze
- `analysis_type` (string, optional) - Type of analysis (default: "legal")

**Response (200):**
```json
{
  "summary": "Document summary...",
  "key_points": ["Point 1", "Point 2"],
  "entities": {
    "parties": ["Party A", "Party B"],
    "dates": ["2024-01-15"],
    "amounts": ["$10,000"]
  },
  "document_type": "Contract",
  "sentiment": "neutral"
}
```

## 🤖 Google Gemini AI Integration

### Model Configuration
- **Model:** `gemini-1.5-flash`
- **Temperature:** 0.7 (balanced creativity and accuracy)
- **Max Tokens:** Configurable based on request
- **Safety Settings:** Enabled for harmful content filtering

### Prompt Engineering
The service uses specialized prompts for legal document analysis:
- Extract key legal points
- Identify parties and obligations
- Summarize terms and conditions
- Highlight important dates and amounts
- Detect potential issues or risks

## 📊 Supported Document Formats

### Text-Based
- **PDF** - Extracted text from PDF documents
- **DOCX** - Microsoft Word documents
- **TXT** - Plain text files
- **RTF** - Rich Text Format

### Image-Based (OCR)
- **JPG/JPEG** - Image files with text
- **PNG** - Portable Network Graphics
- **TIFF** - Tagged Image File Format

## 🔐 Security

- **API Key Protection** - Environment variable for Gemini API key
- **Input Validation** - Request body validation
- **Rate Limiting** - Prevent API abuse (recommended for production)
- **CORS Configuration** - Controlled cross-origin access
- **Error Sanitization** - No sensitive data in error responses

## 🚀 Performance Optimization

- **Async Operations** - FastAPI async/await for concurrent requests
- **Caching** - Cache frequently summarized documents (optional)
- **Connection Pooling** - Reuse HTTP connections to Gemini API
- **Text Chunking** - Handle large documents in chunks
- **Worker Processes** - Multiple workers for production

## 🧪 Testing

### Manual Testing
```bash
# Test health endpoint
curl http://localhost:8000/

# Test summarization
curl -X POST http://localhost:8000/summarize \
  -H "Content-Type: application/json" \
  -d '{"text": "Your document text here..."}'
```

### Python Testing
```python
import requests

# Summarize document
response = requests.post(
    "http://localhost:8000/summarize",
    json={
        "text": "Your document text...",
        "max_length": 500
    }
)
print(response.json())
```

## 📈 Monitoring

### Logs
FastAPI automatically logs:
- Request/response details
- Error messages
- Performance metrics

### Metrics to Monitor
- Request count
- Response time
- Error rate
- API quota usage (Gemini API)

## 🐛 Troubleshooting

### Common Issues

**Gemini API Key Error**
```bash
# Verify API key is set
echo $GEMINI_API_KEY

# Check .env file exists and contains key
cat .env
```

**Module Import Error**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Verify Python version
python --version  # Should be 3.8+
```

**CORS Error**
```bash
# Check CORS configuration in main.py
# Ensure frontend URL is allowed
```

**Timeout Error**
```bash
# Increase timeout in Gemini API call
# Reduce document size
# Check internet connection
```

**Rate Limit Exceeded**
```bash
# Check Gemini API quota
# Implement request throttling
# Upgrade API plan if needed
```

## 🚀 Deployment

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV GEMINI_API_KEY=${GEMINI_API_KEY}

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t legalwise-summarizer .
docker run -p 8000:8000 -e GEMINI_API_KEY=your-key legalwise-summarizer
```

### Cloud Deployment

#### AWS Lambda
1. Package application with dependencies
2. Create Lambda function
3. Set environment variables
4. Configure API Gateway

#### Google Cloud Run
1. Create Dockerfile
2. Build container image
3. Deploy to Cloud Run
4. Set environment variables

#### Heroku
1. Create `Procfile`:
   ```
   web: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
2. Push to Heroku
3. Set environment variables

## 📊 API Usage Examples

### Python
```python
import requests

def summarize_document(text):
    response = requests.post(
        "http://localhost:8000/summarize",
        json={"text": text, "max_length": 500}
    )
    return response.json()

summary = summarize_document("Your legal document text...")
print(summary["summary"])
```

### JavaScript/Node.js
```javascript
const axios = require('axios');

async function summarizeDocument(text) {
  const response = await axios.post('http://localhost:8000/summarize', {
    text: text,
    max_length: 500
  });
  return response.data;
}

summarizeDocument("Your legal document text...")
  .then(data => console.log(data.summary));
```

### cURL
```bash
curl -X POST http://localhost:8000/summarize \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Your legal document text...",
    "max_length": 500
  }'
```

## 📦 Dependencies

```
fastapi==0.100.0
uvicorn[standard]==0.23.0
python-dotenv==1.0.0
google-generativeai==0.3.0
PyMuPDF==1.23.0
Pillow==10.0.0
python-multipart==0.0.6
requests==2.31.0
```

## 🔄 Version History

### v1.0.0
- Initial release
- Google Gemini AI integration
- Document summarization
- Key points extraction
- Multi-format support

## 🗺️ Roadmap

- [ ] Batch document processing
- [ ] Document comparison
- [ ] Custom summarization templates
- [ ] Multi-language support
- [ ] Advanced legal entity extraction
- [ ] Document classification
- [ ] Sentiment analysis
- [ ] Contract risk assessment

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Google Gemini AI Documentation](https://ai.google.dev/docs)
- [Uvicorn Documentation](https://www.uvicorn.org/)
- [Python Documentation](https://docs.python.org/3/)

## 📄 License

ISC License - See main project LICENSE file

## 🤝 Contributing

Please refer to the main project's Contributing Guide for development guidelines.

---

**LegalWise Summarizer** - AI-powered document intelligence 🤖📄
