
# Righthere - AI-Powered Diary Analysis App

Righthere is a .NET MAUI application that leverages artificial intelligence to analyze diary entries and provide mental health advice. It combines machine learning and AI technologies for emotion detection and therapeutic feedback.

## 🤖 AI Features

### 1. Emotion Detection
- **Model**: Custom fine-tuned model on Hugging Face Hub
- **Model Repository**: [`Gun555/Righthere`](https://huggingface.co/Gun555/Righthere)
- **Base Model**: Pre-trained transformer for emotion classification
- **Capabilities**: Detects 6 emotion types
  - 😢 Sadness
  - 😊 Joy
  - ❤️ Love
  - 😠 Anger
  - 😨 Fear
  - 😲 Surprise

### 2. AI Therapist
- **AI Engine**: Google Gemini 2.0 Flash
- **Role**: AI Therapist for emotional analysis and advice
- **Response Structure**:
  - **Suggestion**: Positive and supportive advice
  - **Emotional Reflection**: Summarizes and analyzes user emotions
  - **Mood**: Assigns a primary emotion in one word
  - **Keywords**: Extracts key topics from the diary entry

## 🚀 Setup Instructions

### Prerequisites
- .NET 9.0 SDK
- Python 3.8+ (for API backend)
- Google AI Studio API Key
- Hugging Face Token (for model access)
- Internet connection (for downloading model from Hugging Face Hub)

### 1. AI Model Setup
The model will be automatically downloaded from Hugging Face Hub on first run:
- **Model Repository**: https://huggingface.co/Gun555/Righthere
- **Auto-download**: Model will be cached locally after the first download
- **No manual download required**

### 2. Environment Configuration
Create a `.env` file in the `api/` folder with the following variables:

```env
# Google Gemini API Key (get from Google AI Studio)
apikey=your_google_ai_studio_api_key_here

# Model path (if using a local model)
MODEL_PATH=path/to/your/model/folder

# Hugging Face Token (for accessing Gun555/Righthere model)
HuggingFaceToken=your_huggingface_token_here

# Server Port (optional)
PORT=8000
```

### 3. Technical Architecture
```
User Input (Diary) → Hugging Face Model Hub → Emotion Detection → AI Analysis → Therapeutic Response
                             ↓                       ↓                ↓
                    Gun555/Righthere      →  Transformers Pipeline  →  Google Gemini API  →  Structured Advice
```

### 4. Model Details
- **Model Type**: Sequence Classification (Text → Emotion Labels)
- **Framework**: PyTorch + Transformers
- **Input**: Thai/English text
- **Output**: Probability distribution over 6 emotion classes
- **Performance**: Optimized for diary/personal text analysis

### 5. Install Python Dependencies
```bash
cd api
pip install -r requirements.txt
```

### 6. Run the Application

#### Start AI API Backend:
```bash
cd api
python app.py
```

## 🛠️ API Endpoints

### `/getadvice` (POST)
```json
{
  "text": "Your diary entry text"
}
```

**Response:**
```json
{
  "emotion": "joy",
  "advice": "AI-generated advice and emotional analysis"
}
```

### `/` (GET)
Health check endpoint

## 🎯 Model Information

### Hugging Face Model: Gun555/Righthere
- **Model Card**: https://huggingface.co/Gun555/Righthere
- **Model Type**: AutoModelForSequenceClassification
- **Tokenizer**: Compatible with Transformers AutoTokenizer
- **Input Format**: Text sequences (Thai/English)
- **Output**: 6-class emotion classification

### Model Performance
- **Classes**: 6 emotion categories (sadness, joy, love, anger, fear, surprise)
- **Optimized for**: Personal diary and emotional text analysis

### Using the Model Directly
```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Load model and tokenizer
model_name = "Gun555/Righthere"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# Predict emotion
text = "I feel great today!"
inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=128)
outputs = model(**inputs)
predicted_class = torch.argmax(outputs.logits, dim=-1)
```

## 🔧 Development

### Technology Stack
- **Frontend**: .NET MAUI (C#)
- **Backend**: FastAPI (Python)
- **ML Framework**: Transformers (Hugging Face)
- **AI Model**: Custom model hosted on Hugging Face Hub (`Gun555/Righthere`)
- **AI Service**: Google Gemini API
- **Model Hosting**: Hugging Face Model Hub
- **Database**: Local storage with Models/

### Project Structure
```
Righthere/
├── api/                 # AI Backend API
├── Models/             # Data models (C#)
├── Services/           # API services (C#)
├── Views/              # MAUI pages
├── Platforms/          # Platform-specific code
└── Resources/          # App resources
```

