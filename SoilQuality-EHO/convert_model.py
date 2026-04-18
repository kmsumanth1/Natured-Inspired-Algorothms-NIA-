import tensorflow as tf

# Force load ignoring config
model = tf.keras.models.load_model(
    "best_soil_image_model.keras",
    compile=False,
    safe_mode=False
)

# Save in old stable format
model.save("fixed_model.h5")

print("✅ Converted and saved!")