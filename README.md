# Righthere - AI-Powered Diary Analysis App

Righthere เป็นแอปพลิเคชัน .NET MAUI ที่ใช้ปัญญาประดิษฐ์ในการวิเคราะห์ไดอารี่และให้คำแนะนำด้านจิตใจ โดยผสมผสานเทคโนโลยี Machine Learning และ AI สำหรับการตรวจจับอารมณ์และการให้คำปรึกษา

## 🤖 AI Features

### 1. Emotion Detection
- **โมเดล**: Custom fine-tuned model บน Hugging Face Hub
- **Model Repository**: [`Gun555/Righthere`](https://huggingface.co/Gun555/Righthere)
- **Base Model**: Pre-trained transformer สำหรับการจำแนกอารมณ์
- **ความสามารถ**: ตรวจจับอารมณ์ 6 ประเภท
  - 😢 Sadness (ความเศร้า)
  - 😊 Joy (ความสุข)
  - ❤️ Love (ความรัก)
  - 😠 Anger (ความโกรธ)
  - 😨 Fear (ความกลัว)
  - 😲 Surprise (ความประหลาดใจ)


### 2. AI Therapist
- **AI Engine**: Google Gemini 2.0 Flash
- **บทบาท**: AI Therapist ที่ให้คำปรึกษาและช่วยวิเคราะห์อารมณ์
- **การตอบสนอง**:
  - **Suggestion**: คำแนะนำเชิงบวกและข้อเสนอแนะ
  - **Emotional Reflection**: สรุปและวิเคราะห์อารมณ์ของผู้ใช้
  - **Mood**: การกำหนดอารมณ์หลักในคำเดียว
  - **Keywords**: การสกัดคำสำคัญจากเนื้อหาไดอารี่


## 🚀 Setup Instructions

### Prerequisites
- .NET 9.0 SDK
- Python 3.8+ (สำหรับ API backend)
- Google AI Studio API Key
- Hugging Face Token (สำหรับการเข้าถึง model)
- Internet connection (สำหรับดาวน์โหลด model จาก Hugging Face Hub)

### 1. AI Model Setup
โมเดลจะถูกดาวน์โหลดอัตโนมัติจาก Hugging Face Hub ในครั้งแรกที่รันแอป:
- **Model Repository**: https://huggingface.co/Gun555/Righthere
- **Auto-download**: โมเดลจะถูกแคชไว้ใน local หลังจากดาวน์โหลดครั้งแรก
- **No manual download required**: ไม่ต้องดาวน์โหลดไฟล์ model เอง

### 2. Environment Configuration
สร้างไฟล์ `.env` ในโฟเดอร์ api/ พร้อมตัวแปรต่อไปนี้:

```env
# Google Gemini API Key (รับจาก Google AI Studio)
apikey=your_google_ai_studio_api_key_here

# เส้นทางโฟเดอร์โมเดล (ถ้าใช้ local model)
MODEL_PATH=path/to/your/model/folder

# Hugging Face Token (สำหรับการเข้าถึง model Gun555/Righthere)
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
```bash
cd api
pip install -r requirements.txt
```

### 4. Run the Application

#### Start AI API Backend:
```bash
cd api
python app.py
```

## 🛠️ API Endpoints

### `/getadvice` (POST)
```json
{
  "text": "เนื้อหาไดอารี่ของผู้ใช้"
}
```

**Response:**
```json
{
  "emotion": "joy",
  "advice": "คำแนะนำจาก AI พร้อมการวิเคราะห์อารมณ์"
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
text = "วันนี้ฉันรู้สึกดีมาก"
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

