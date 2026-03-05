import numpy as np
import tensorflow as tf
import joblib
from sklearn.preprocessing import LabelEncoder, StandardScaler

scaler = joblib.load("scaler.pkl")
label_encoder = joblib.load("label_encoder.pkl")
selected_features = joblib.load("selected_features.pkl")
# Load models
image_model = tf.keras.models.load_model("soil_image_model.keras")
tabular_model = joblib.load("../ml/model.pkl")

# Class names (must match folder names exactly)
class_names = [
    "Alluvial_Soil",
    "Arid_Soil",
    "Black_Soil",
    "Laterite_Soil",
    "Mountain_Soil",
    "Red_Soil",
    "Yellow_Soil"
]

def predict_soil_type(image_path):
    img = tf.keras.preprocessing.image.load_img(image_path, target_size=(150,150))
    img_array = tf.keras.preprocessing.image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    preds = image_model.predict(img_array)
    return class_names[np.argmax(preds)]

def predict_fertility(npk_features, soil_type):
    # encode soil type
    soil_encoded = label_encoder.transform([soil_type])[0]

    features = np.append(npk_features, soil_encoded)
    features = features.reshape(1, -1)

    features_scaled = scaler.transform(features)
    features_selected = features_scaled[:, selected_features]

    prediction = tabular_model.predict(features_selected)
    return prediction[0]

# Example usage
image_path = "test_image.jpg"
soil_type = predict_soil_type(image_path)
print("Predicted Soil Type:", soil_type)

npk = np.array([120, 45, 300, 7.2, 0.6, 0.8, 10, 0.3, 0.5, 0.7, 2.1, 0.2])
fertility = predict_fertility(npk, soil_type)
print("Predicted Fertility:", fertility)