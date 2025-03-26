from fastapi import FastAPI
from transformers import AutoConfig, AutoModelForSequenceClassification, AutoTokenizer
import numpy as np
from google import genai
import torch
import os
from dotenv import load_dotenv
from pydantic import BaseModel
import uvicorn  

# โหลด environment variables
load_dotenv()



# โหลด API Key จาก .env
API_KEY = os.getenv("apikey")
client = genai.Client(api_key=API_KEY)

# โหลดโมเดลจาก Hugging Face Model Hub (Gun555/rightheree)
MODEL_NAME = "Gun555/Righthere"

# Map ตัวเลขเป็นอารมณ์
label_map = {
    0: "sadness",
    1: "joy",
    2: "love",
    3: "anger",
    4: "fear",
    5: "surprise"
}

# โหลดโมเดลและ Tokenizer เพียงครั้งเดียวตอน API เริ่มทำงาน
async def lifespan(app: FastAPI):
    global model, tokenizer, config
    print("Loading model...")  # Debugging  
    config = AutoConfig.from_pretrained(MODEL_NAME,token=os.getenv("HuggingFaceToken"))
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, config=config, torch_dtype=torch.float16,token=os.getenv("HuggingFaceToken"))
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME,token=os.getenv("HuggingFaceToken"))
    print("Model loaded successfully!")  # Debugging
    yield  # รอให้ API รัน
    print("Shutting down API...")  # Cleanup เมื่อ API หยุดทำงาน

# สร้าง FastAPI instance
app = FastAPI(lifespan=lifespan)

# สร้างโครงสร้างรับข้อมูล
class Advice(BaseModel):
    text: str

@app.post("/getadvice")
async def get_advice(data: Advice):
    diary_text = data.text

    # Tokenize ข้อความ
    encoding = tokenizer(
        diary_text, truncation=True, padding="max_length", max_length=128, return_tensors="pt"
    )

    # ทำนายอารมณ์
    output = model(**encoding)
    logits = output.logits.detach().cpu().numpy()
    predicted_index = int(np.argmax(logits, axis=-1))
    predicted_emotion = label_map.get(predicted_index, "Unknown")

    # สร้าง Prompt สำหรับ AI
    prompt = f"""
                    ### Role: System (AI Therapist)
                    You are an empathetic AI therapist trained to analyze users' diary entries. Your goal is to help users understand their emotions through diary analysis and provide compassionate feedback.

                    ### Role: User (Diary Writer)
                    Diary Entry:
                    "{diary_text}"

                    ### Detected Emotion:
                    {predicted_emotion}

                    ### Task:
                    - **Analyze** the user's emotions based on the diary entry.
                    - **Provide** a structured response including:
                        1. **Suggestion**: A supportive and positive message.
                        2. **Emotional Reflection**: Summarize the user's emotions to help them understand their feelings.
                        3. **Mood**: Assign a one-word emotional label.
                        4. **Keyword Extraction**: Identify key topics from the diary entry.

                    ### Response Format:
                    - Suggestion: <Your response>
                    - Emotional Reflection: <Your response>
                    - Mood: <Your response>
                    - Keywords: <Your response>
                    """

    # เรียกใช้ Gemini API
    response = client.models.generate_content(
        model="tunedModels/advicedataset500-s3qpyzbc1d00",
        contents=prompt
    )

    return {"emotion": predicted_emotion, "advice": response.text}

@app.get("/")
async def home():
    return {"message": "Welcome to AI Therapist API"}

uvicorn.run(app, host="127.0.0.1", port=int(os.getenv("PORT", "8000")))
