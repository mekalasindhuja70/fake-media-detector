import os
import tensorflow as tf
from tensorflow import keras
from keras import layers, models

# ==========================================
# 1. SET CONFIGURATION & PATHS
# ==========================================
IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 15  
DATASET_DIR = "dataset"  

print("Loading dataset from folders...")

# ==========================================
# 2. LOAD AND SPLIT DATASET AUTOMATICALLY
# ==========================================
train_ds = tf.keras.utils.image_dataset_from_directory(
    DATASET_DIR,
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE
)

val_ds = tf.keras.utils.image_dataset_from_directory(
    DATASET_DIR,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE
)

AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.prefetch(buffer_size=AUTOTUNE)

print("Dataset loaded successfully!")

# ==========================================
# 3. BUILD THE MODEL WITH DATA AUGMENTATION
# ==========================================
print("Building the model using EfficientNetB0 backbone + Data Augmentation...")

data_augmentation = models.Sequential([
    layers.RandomFlip("horizontal"),       
    layers.RandomRotation(0.1),            
    layers.RandomZoom(0.1),                
])

base_model = tf.keras.applications.EfficientNetB0(
    weights='imagenet', 
    include_top=False, 
    input_shape=(224, 224, 3)
)

base_model.trainable = False

model = models.Sequential([
    layers.Input(shape=(224, 224, 3)),
    data_augmentation,  
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dropout(0.4), 
    layers.Dense(2, activation='softmax')
])

model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.001),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# ==========================================
# 4. TRAIN THE MODEL
# ==========================================
print("Starting training loop...")

checkpoint_cb = tf.keras.callbacks.ModelCheckpoint(
    "model/fake_media_detector.keras",
    save_best_only=True,
    monitor="val_accuracy",
    mode="max"
)

history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=EPOCHS,
    callbacks=[checkpoint_cb]
)

# ==========================================
# 5. SAVE FINAL RUN MODEL
# ==========================================
os.makedirs("model", exist_ok=True)
model.save("model/fake_media_detector_final.keras")

print("\nTraining Completed Successfully!")
print("Best Model Saved to: model/fake_media_detector.keras")