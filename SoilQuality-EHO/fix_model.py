import tensorflow as tf

model = tf.keras.models.load_model(
    "soil_image_model/soil_image_model.keras",
    compile=False,
    safe_mode=False
)

model.save("soil_image_model/new_model.keras")

print("Model converted successfully ✅")