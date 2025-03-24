from transformers import AutoConfig, AutoModelForSequenceClassification, AutoTokenizer
import numpy as np
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

# สร้าง client สำหรับใช้งาน Gemini API
client = genai.Client(api_key=os.getenv("apikey"))

# กำหนด path ของโมเดลที่เทรนมาแล้ว
model_path = os.getenv("path")

# map ตัวเลขเป็น label อารมณ์
label_map = {
    0: "sadness",
    1: "joy",
    2: "love",
    3: "anger",
    4: "fear",
    5: "surprise"
}

# โหลด configuration ของโมเดลจาก path ที่ระบุ
config = AutoConfig.from_pretrained(model_path)

# โหลด tokenizer ที่บันทึกไว้ (ต้องมีไฟล์ tokenizer ในโฟลเดอร์โมเดล)
tokenizer = AutoTokenizer.from_pretrained(model_path)

# โหลดโมเดลสำหรับการจัดหมวดหมู่อารมณ์จาก path ที่ระบุ
model = AutoModelForSequenceClassification.from_pretrained(model_path, config=config)

# กำหนดข้อความสำหรับทดสอบการพยากรณ์อารมณ์
test_texts = """
I never thought that when you said 'forever,' it would only mean a brief moment—just long enough for me to be someone you once loved… before you walked away like nothing ever happened.
"""

# ทำการ tokenize ข้อความเทส โดยใช้ tokenizer ที่โหลดมาแล้ว
encoding = tokenizer(
    test_texts, 
    truncation=True, 
    padding="max_length", 
    max_length=128, 
    return_tensors="pt"
)

# ทำ inference กับโมเดลโดยส่ง encoder ของข้อความเข้าไป
output = model(**encoding)

# นำ logits ที่ได้จากการเทรนมาแปลงเป็น numpy array และเลือก index ที่มีค่าสูงสุด
logits = output.logits.detach().cpu().numpy()
predicted_index = int(np.argmax(logits, axis=-1))

# map ค่า index ที่ทำนายได้เป็นอารมณ์ตาม label_map
predicted_emotion = label_map.get(predicted_index, "Unknown")

# เรียกใช้ Gemini API เพื่อ generate content โดยนำข้อความทดสอบและอารมณ์ที่ทำนายได้ไปประกอบใน request
response = client.models.generate_content(
    model="tunedModels/advicedataset500-s3qpyzbc1d00",
    contents=f"{test_texts} {predicted_emotion}",
)


print(f"Emotion: {predicted_emotion}")
# แสดงผลลัพธ์จาก Gemini API บน console
# print("*" * 50)
# print(response.text)
# print("*" * 50)