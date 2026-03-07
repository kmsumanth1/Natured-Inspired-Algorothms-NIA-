from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import tensorflow as tf
import numpy as np
import joblib
from PIL import Image
import io
import os

# Create FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base directory of this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Models will be loaded lazily
image_model = None
fertility_model = None

# Soil classes
class_names = [
    "Alluvial_Soil",
    "Arid_Soil",
    "Black_Soil",
    "Laterite_Soil",
    "Mountain_Soil",
    "Red_Soil",
    "Yellow_Soil"
]

# Fertility mapping
fertility_map = {
    0: "Low",
    1: "Medium",
    2: "High"
}

# Function to load models only once
def load_models():
    global image_model, fertility_model

    if image_model is None:
        image_model = tf.keras.models.load_model(
            os.path.join(BASE_DIR, "../soil_image_model/soil_image_model.keras")
        )

    if fertility_model is None:
        fertility_model = joblib.load(
            os.path.join(BASE_DIR, "../ml/model.pkl")
        )

# Prediction API
@app.post("/predict")
async def predict(
    file: UploadFile = File(...),
    npk: str = Form(...)
):

    # Load models when first request arrives
    load_models()

    contents = await file.read()

    image = Image.open(io.BytesIO(contents)).resize((150,150))
    img_array = np.array(image) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    preds = image_model.predict(img_array)
    soil_type = class_names[np.argmax(preds)]

    npk_values = list(map(float, npk.split(",")))
    npk_array = np.array(npk_values).reshape(1, -1)

    fertility = fertility_model.predict(npk_array)[0]

    return {
        "soil_type": soil_type,
        "fertility": fertility_map[fertility]
    }