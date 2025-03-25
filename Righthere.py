from transformers import AutoConfig, AutoModelForSequenceClassification, AutoTokenizer
import numpy as np
from google import genai
from dotenv import load_dotenv
import os
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel

# โหลด environment variables จากไฟล์ .env
load_dotenv()

# สร้าง instance ของ FastAPI สำหรับสร้าง API server
app = FastAPI()

# กำหนด model สำหรับรับข้อมูลคำขอ advice ผ่าน endpoint
class Advice(BaseModel):
    text: str  # ข้อความอินพุตสำหรับพยากรณ์อารมณ์และ generate คำแนะนำ

# กำหนด endpoint สำหรับ POST request ที่ /getadvice
@app.post("/getadvice")
async def get_advice(data: Advice):
    # สร้าง client สำหรับใช้งาน Gemini API 
    # โดยใช้ api_key ที่เก็บไว้ใน environment variable
    client = genai.Client(api_key=os.getenv("apikey"))

    # กำหนด path ของโมเดลที่เทรนมาแล้ว โดยอ่านจาก environment variable
    model_path = os.getenv("model_path")

    # map ตัวเลขที่ได้จาก model ให้เป็นอารมณ์ในรูปแบบข้อความ
    label_map = {
        0: "sadness",   # เศร้า
        1: "joy",       # สุข
        2: "love",      # รัก
        3: "anger",     # โกรธ
        4: "fear",      # กลัว
        5: "surprise"   # ประหลาดใจ
    }

    # โหลด configuration ของโมเดลจาก path ที่ระบุ
    config = AutoConfig.from_pretrained(model_path)

    # โหลด tokenizer ที่บันทึกไว้ในโฟลเดอร์ของโมเดล
    # หมายเหตุ: ต้องมีไฟล์ tokenizer ที่จำเป็น (เช่น tokenizer_config.json, vocab.txt ฯลฯ)
    tokenizer = AutoTokenizer.from_pretrained(model_path)

    # โหลดโมเดลสำหรับจัดหมวดหมู่อารมณ์จาก path ที่ระบุ โดยใช้ configuration ที่โหลดมาแล้ว
    model = AutoModelForSequenceClassification.from_pretrained(model_path, config=config)

    # อ่านข้อความ diary จากข้อมูลที่ส่งเข้ามาใน request
    diary_text = data.text

    # ทำการ tokenize ข้อความ โดยใช้ tokenizer ที่โหลดมาจากโมเดลที่เทรนแล้ว
    encoding = tokenizer(
        diary_text, 
        truncation=True,          # ตัดข้อความให้สั้นลงตาม max_length ถ้ามากกว่า
        padding="max_length",       # เติมข้อความให้อยู่ในความยาว max_length
        max_length=128,             # กำหนดความยาวสูงสุดของ input 
        return_tensors="pt"         # แปลงผลลัพธ์เป็น tensors ของ PyTorch
    )

    # ทำ inference โดยส่ง encoded input เข้าไปในโมเดล
    output = model(**encoding)

    # แปลงผลลัพธ์ logits เป็น numpy array และหาดัชนีที่มีค่าสูงสุด
    logits = output.logits.detach().cpu().numpy()
    predicted_index = int(np.argmax(logits, axis=-1))

    # ใช้ label_map เพื่อแปลง index ที่ทำนายได้เป็นข้อความอารมณ์
    predicted_emotion = label_map.get(predicted_index, "Unknown")

    # เรียกใช้ Gemini API เพื่อ generate content โดยรวมข้อความ diary และอารมณ์ที่ทำนายได้เข้าไปใน request
    response = client.models.generate_content(
        model="tunedModels/advicedataset500-s3qpyzbc1d00",
        contents=f"{diary_text} {predicted_emotion}",
    )

    # แสดงผลลัพธ์ทาง console สำหรับตรวจสอบค่าอารมณ์ที่ทำนายและคำตอบจาก Gemini API
    print(f"Emotion: {predicted_emotion}")
    print("*" * 50)
    print(response.text)
    print("*" * 50)

    # ส่งกลับผลลัพธ์เป็น tuple ที่ประกอบไปด้วยอารมณ์ที่ทำนายได้และข้อความที่ถูก generate
    return predicted_emotion, response.text

port = os.getenv("port")
if port == "":
    port = 8000
else:
    port = int(port)

# รัน API server ด้วย uvicorn บน localhost ที่ port 8000
uvicorn.run(app, host="127.0.0.1", port=port)
    