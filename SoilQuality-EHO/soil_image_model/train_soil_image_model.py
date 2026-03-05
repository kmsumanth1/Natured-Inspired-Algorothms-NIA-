import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from sklearn.utils.class_weight import compute_class_weight

# ======================
# SETTINGS
# ======================
img_size = 150   # Back to 150 (your best performing size)
batch_size = 32
epochs_phase1 = 20
epochs_phase2 = 8

# ======================
# DATA AUGMENTATION
# ======================
datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2,
    rotation_range=15,
    zoom_range=0.2,
    horizontal_flip=True,
    brightness_range=[0.8, 1.2]
)

train_data = datagen.flow_from_directory(
    "dataset",
    target_size=(img_size, img_size),
    batch_size=batch_size,
    class_mode="categorical",
    subset="training"
)

val_data = datagen.flow_from_directory(
    "dataset",
    target_size=(img_size, img_size),
    batch_size=batch_size,
    class_mode="categorical",
    subset="validation"
)

# ======================
# CLASS WEIGHTS
# ======================
labels = train_data.classes
class_weights = compute_class_weight(
    class_weight="balanced",
    classes=np.unique(labels),
    y=labels
)
class_weights = dict(enumerate(class_weights))

print("Class Weights:", class_weights)

# ======================
# MODEL BUILDING
# ======================
base_model = MobileNetV2(
    input_shape=(img_size, img_size, 3),
    include_top=False,
    weights="imagenet"
)

base_model.trainable = False  # Phase 1

model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(train_data.num_classes, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# ======================
# CALLBACKS
# ======================
early_stop = EarlyStopping(
    monitor="val_loss",
    patience=5,
    restore_best_weights=True
)

reduce_lr = ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.3,
    patience=3,
    min_lr=1e-6,
    verbose=1
)

checkpoint = ModelCheckpoint(
    "best_soil_image_model.keras",
    monitor="val_accuracy",
    save_best_only=True,
    verbose=1
)

# ======================
# PHASE 1 TRAINING
# ======================
print("\nPhase 1: Training classifier head...\n")

model.fit(
    train_data,
    validation_data=val_data,
    epochs=epochs_phase1,
    class_weight=class_weights,
    callbacks=[early_stop, reduce_lr, checkpoint]
)

# ======================
# PHASE 2 FINE-TUNING
# ======================
print("\nPhase 2: Fine-tuning MobileNet...\n")

base_model.trainable = True

# Freeze first 100 layers (stable fine-tuning)
for layer in base_model.layers[:100]:
    layer.trainable = False

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

model.fit(
    train_data,
    validation_data=val_data,
    epochs=epochs_phase2,
    class_weight=class_weights,
    callbacks=[early_stop, reduce_lr, checkpoint]
)

# ======================
# SAVE FINAL MODEL
# ======================
model.save("soil_image_model.keras")

print("\nTraining Completed Successfully!")