from fastapi import FastAPI, UploadFile, File, Form
import tensorflow as tf
import numpy as np
import joblib
from PIL import Image
import io

app = FastAPI()

image_model = tf.keras.models.load_model("../soil_image_model/soil_image_model.keras")
fertility_model = joblib.load("../ml/model.pkl")

class_names = [
    "Alluvial_Soil",
    "Arid_Soil",
    "Black_Soil",
    "Laterite_Soil",
    "Mountain_Soil",
    "Red_Soil",
    "Yellow_Soil"
]

fertility_map = {0:"Low",1:"Medium",2:"High"}

@app.post("/predict")
async def predict(
    file: UploadFile = File(...),
    npk: str = Form(...)
):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).resize((150,150))
    img_array = np.array(image)/255.0
    img_array = np.expand_dims(img_array, axis=0)

    preds = image_model.predict(img_array)
    soil_type = class_names[np.argmax(preds)]

    npk_values = list(map(float, npk.split(",")))
    npk_array = np.array(npk_values).reshape(1,-1)

    fertility = fertility_model.predict(npk_array)[0]

    return {
        "soil_type": soil_type,
        "fertility": fertility_map[fertility]
    }