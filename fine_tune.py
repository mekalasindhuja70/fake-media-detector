import os
import tensorflow as tf
from tensorflow import keras
from keras import models

# ==========================================
# 1. SETUP DATA AND CONFIGURATION
# ==========================================
IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32
FINE_TUNE_EPOCHS = 10
DATASET_DIR = "dataset"

print("Loading dataset for fine-tuning...")
train_ds = tf.keras.utils.image_dataset_from_directory(
    DATASET_DIR, validation_split=0.2, subset="training", seed=123,
    image_size=IMAGE_SIZE, batch_size=BATCH_SIZE
)
val_ds = tf.keras.utils.image_dataset_from_directory(
    DATASET_DIR, validation_split=0.2, subset="validation", seed=123,
    image_size=IMAGE_SIZE, batch_size=BATCH_SIZE
)

AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.prefetch(buffer_size=AUTOTUNE)

# ==========================================
# 2. LOAD SAVED MODEL & UNFREEZE TOP LAYERS
# ==========================================
print("\nLoading your best trained model...")
model = models.load_model("model/fake_media_detector.keras")

base_model = model.layers[1] 
base_model.trainable = True

# Refreeze all layers EXCEPT the last 20 layers
for layer in base_model.layers[:-20]:
    layer.trainable = False

# ==========================================
# 3. RECOMPILE WITH A MICRO LEARNING RATE
# ==========================================
model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.00001), 
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# ==========================================
# 4. RUN FINE-TUNING
# ==========================================
print("\nStarting Fine-Tuning Loop...")
checkpoint_cb = tf.keras.callbacks.ModelCheckpoint(
    "model/fake_media_detector_finetuned.keras",
    save_best_only=True,
    monitor="val_accuracy",
    mode="max"
)

history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=FINE_TUNE_EPOCHS,
    callbacks=[checkpoint_cb]
)

print("\nFine-Tuning Finished! Optimized model saved to: model/fake_media_detector_finetuned.keras")