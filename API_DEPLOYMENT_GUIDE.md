# Security Model API - Deployment Guide

## 📋 Overview

Enterprise-grade FastAPI backend for real-time malicious prompt detection using a fine-tuned BERT transformer model. This API provides:

- ✅ Automatic GPU/CPU detection
- ✅ Production-ready error handling  
- ✅ Comprehensive request/response validation
- ✅ CORS support for frontend integration
- ✅ Interactive API documentation (Swagger UI)
- ✅ Model loaded once at startup (no disk I/O per request)

---

## 🚀 Quick Start

### Step 1: Install Dependencies

```powershell
# From the SecurePrompt-Core directory
pip install -r requirements.txt
```

### Step 2: Start the API Server

```powershell
# Option A: Direct Python execution
python app.py

# Option B: Using Uvicorn directly (recommended for production)
uvicorn app:app --host 0.0.0.0 --port 5000 --reload
```

### Step 3: Verify the API is Running

Open your browser and visit:
- **Interactive Docs (Swagger UI):** http://localhost:5000/docs
- **Health Check:** http://localhost:5000/health
- **ReDoc Docs:** http://localhost:5000/redoc

---

## 📡 API Endpoints

### 1. Health Check
**Endpoint:** `GET /health`

**Purpose:** Verify API and model status

**Response:**
```json
{
  "status": "operational",
  "model_loaded": true,
  "device": "cuda",
  "timestamp": "2026-05-10T19:30:00.123456"
}
```

**cURL Example:**
```bash
curl http://localhost:5000/health
```

---

### 2. Scan Prompt (Main Endpoint)
**Endpoint:** `POST /api/v1/scan-prompt`

**Purpose:** Analyze text for malicious content

**Request Body:**
```json
{
  "promptText": "Is this a safe message?"
}
```

**Response:**
```json
{
  "is_malicious": false,
  "confidence_score": 0.9412,
  "processing_time_ms": 52.34,
  "version": "1.0.0"
}
```

**cURL Example (GET style):**
```bash
curl -X POST http://localhost:5000/api/v1/scan-prompt \
  -H "Content-Type: application/json" \
  -d '{"promptText": "Normal message here"}'
```

**cURL Example (Complex text):**
```bash
curl -X POST http://localhost:5000/api/v1/scan-prompt \
  -H "Content-Type: application/json" \
  -d '{"promptText": "'; DROP TABLE users; --"}'
```

---

## 🔌 Frontend Integration (React/Vite)

### JavaScript Fetch Example

```javascript
async function scanPrompt(promptText) {
  try {
    const response = await fetch('http://localhost:5000/api/v1/scan-prompt', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ promptText })
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    const data = await response.json();
    console.log('Classification:', data);
    
    return {
      isMalicious: data.is_malicious,
      confidence: data.confidence_score,
      time: data.processing_time_ms
    };
  } catch (error) {
    console.error('Error scanning prompt:', error);
    return null;
  }
}

// Usage
scanPrompt("Is this safe?").then(result => {
  if (result) {
    console.log(`Malicious: ${result.isMalicious}, Confidence: ${result.confidence}`);
  }
});
```

### React Hook Example

```javascript
import { useState } from 'react';

export function usePromptScanner() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);

  const scan = async (promptText) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch('http://localhost:5000/api/v1/scan-prompt', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ promptText })
      });

      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      
      const data = await response.json();
      setResult(data);
      return data;
    } catch (err) {
      setError(err.message);
      return null;
    } finally {
      setLoading(false);
    }
  };

  return { scan, loading, error, result };
}
```

---

## 🛠️ Architecture Overview

### `SecurityInferenceEngine` Class

The core inference engine encapsulating all PyTorch logic:

```python
engine = SecurityInferenceEngine(
    model_path="./training_env/compiled_security_model",
    max_token_length=512,
    threshold_score=0.5
)
engine.initialize_model()  # Called at startup
result = engine.run_inference("user input text")
```

**Key Features:**
- Automatic GPU/CPU detection
- Model loaded exactly once
- All parameters frozen (inference-only)
- Gradient computation disabled
- Softmax probability conversion
- Exception safety

---

## 📊 Request/Response Models

### `AnalysisRequest` (Pydantic)
- `promptText` (str): Input text (1-10,000 characters)
- Automatic whitespace trimming
- Empty validation

### `AnalysisResponse` (Pydantic)
- `is_malicious` (bool): Classification result
- `confidence_score` (float): 0.0-1.0 with 4 decimal precision
- `processing_time_ms` (float): Execution duration
- `version` (str): API version

---

## 🔒 Security & Production Settings

### CORS Configuration
Currently allows all origins. For production, restrict to specific domains:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourfrontend.com"],
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["Content-Type"],
)
```

### Production Deployment

Use `gunicorn` for production instead of `uvicorn` directly:

```bash
pip install gunicorn

gunicorn app:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:5000
```

### Environment Variables (Optional)

```powershell
# Disable debug logging
$env:LOG_LEVEL = "INFO"

# Use specific GPU
$env:CUDA_VISIBLE_DEVICES = "0"
```

---

## 📝 Logging

The API logs:
- Model loading on startup
- Each inference request
- Processing time
- Any errors or exceptions

**Log Output Example:**
```
INFO - Loading model from: ./training_env/compiled_security_model
INFO - Detected compute device: cuda
INFO - ✓ Model successfully loaded in 2.34s on cuda
INFO - Processing prompt (length: 42 chars)
INFO - ✓ Inference complete: Safe_Content (confidence: 0.9412, time: 45.23ms)
```

---

## ⚙️ Configuration

Edit these constants in `app.py`:

```python
MODEL_DIRECTORY_PATH = "./training_env/compiled_security_model"  # Model location
TOKEN_LENGTH_LIMIT = 512                                          # Max token length
SOFTMAX_TEMPERATURE = 1.0                                         # Temperature for softmax
API_VERSION_TAG = "1.0.0"                                        # API version
```

---

## 🐛 Troubleshooting

### "Model is not initialized"
- Check model files exist in `compiled_security_model/`
- Verify `config.json`, `model.safetensors`, `tokenizer.json` are present

### "CUDA out of memory"
- Fallback to CPU: Remove GPU or set `CUDA_VISIBLE_DEVICES=""`
- Reduce batch size in code

### "Connection refused"
- Ensure API is running: Check console output
- Check port 5000 is not in use: `netstat -ano | findstr :5000`

### CORS errors on frontend
- Verify origin is in `allow_origins` list
- Check browser console for exact error message
- Use http://localhost (not 127.0.0.1) for local development

---

## 📚 API Documentation

Automatic interactive docs available at: **http://localhost:5000/docs**

This provides:
- Request/response schemas
- Try-it-out functionality
- Parameter descriptions
- Example payloads

---

## 🔄 Model Information

- **Base Model:** `prajjwal1/bert-tiny`
- **Task:** Binary text classification
- **Classes:** 
  - 0 = Safe_Content
  - 1 = Malicious_Injection
- **Max Input Length:** 512 tokens
- **Inference Device:** Auto-detected (GPU/CPU)

---

## ✅ Checklist for Deployment

- [ ] Model files in `compiled_security_model/`
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] API starts without errors: `python app.py`
- [ ] Health endpoint responds: `GET /health`
- [ ] Can scan prompts: `POST /api/v1/scan-prompt`
- [ ] Frontend can connect (CORS working)
- [ ] Model inference time < 100ms
- [ ] GPU detection working (if GPU available)

---

**Version:** 1.0.0  
**Last Updated:** May 10, 2026  
**Status:** Production-Ready ✅
