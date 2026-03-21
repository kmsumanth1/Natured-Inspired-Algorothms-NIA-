import os
from fastapi import FastAPI, UploadFile, File, Form
import tensorflow as tf
import numpy as np
from PIL import Image

app = FastAPI()

# ✅ Fix model path (important for deployment)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "../soil_image_model/soil_image_model.keras")

model = tf.keras.models.load_model(model_path, compile=False)

@app.get("/")
def home():
    return {"message": "ML API running"}

@app.post("/predict")
async def predict(
    file: UploadFile = File(...),
    npk: str = Form(...)   # ✅ Added this to match backend
):
    image = Image.open(file.file).resize((224, 224))
    img_array = np.array(image) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)

    # ✅ Example processing (you can customize)
    predicted_class = int(np.argmax(prediction))

    return {
        "prediction": prediction.tolist(),
        "soil_type": f"Class {predicted_class}",
        "fertility": "Medium",  # you can improve this logic later
        "npk_received": npk
    }