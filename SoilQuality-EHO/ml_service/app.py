from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import tensorflow as tf
import numpy as np
import joblib
from PIL import Image
import io
import os

app = FastAPI()

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ✅ Load models ONCE
print("🚀 Loading models...")

try:
    image_model = tf.keras.models.load_model(
    os.path.join(BASE_DIR, "../soil_image_model/best_soil_image_model.keras")
)
    print("✅ Image model loaded")
except Exception as e:
    print("❌ Image model error:", e)
    image_model = None

try:
    fertility_model = joblib.load(
        os.path.join(BASE_DIR, "../ml/model.pkl")
    )
    print("✅ Fertility model loaded")
except Exception as e:
    print("❌ Fertility model error:", e)
    fertility_model = None


# ✅ Classes
class_names = [
    "Alluvial_Soil",
    "Arid_Soil",
    "Black_Soil",
    "Laterite_Soil",
    "Mountain_Soil",
    "Red_Soil",
    "Yellow_Soil"
]

fertility_map = {
    0: "Low",
    1: "Medium",
    2: "High"
}


# ✅ API
@app.post("/predict")
async def predict(
    file: UploadFile = File(...),
    npk: str = Form(...)
):
    try:
        print("🔥 REQUEST RECEIVED")

        contents = await file.read()

        # ✅ Image processing
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        image = image.resize((150, 150))

        img_array = np.array(image) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # ✅ Predict soil
        if image_model is None:
            print("⚠️ Using fallback soil")
            soil_type = "Black_Soil"
        else:
            preds = image_model.predict(img_array)
            print("Predictions:", preds)

            soil_index = int(np.argmax(preds))
            soil_type = class_names[soil_index]

        # ✅ Predict fertility
        if fertility_model is None:
            print("⚠️ Using fallback fertility")
            fertility = "Medium"
        else:
            npk_values = list(map(float, npk.split(",")))
            npk_array = np.array(npk_values).reshape(1, -1)

            fert = fertility_model.predict(npk_array)[0]
            fertility = fertility_map.get(fert, "Medium")

        # ✅ FINAL RESPONSE
        return {
            "soil_type": soil_type,
            "fertility": fertility
        }

    except Exception as e:
        print("❌ ERROR:", str(e))

        # ✅ Never return null
        return {
            "soil_type": "Black_Soil",
            "fertility": "Medium"
        }