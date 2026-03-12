from fastapi import FastAPI, UploadFile, File
import tensorflow as tf
import numpy as np
from PIL import Image

app = FastAPI()

# Load model once
model = tf.keras.models.load_model("soil_image_model.keras")

@app.get("/")
def home():
    return {"message": "Soil Image ML API running"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    
    image = Image.open(file.file).resize((224,224))
    img_array = np.array(image)/255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)

    return {"prediction": prediction.tolist()}