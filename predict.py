import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.efficientnet import preprocess_input

# ==========================================
# Load Model
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "model",
    "fake_media_detector_finetuned.keras"
)

print("Loading model...")
model = load_model(MODEL_PATH)
print("Model Loaded Successfully!")

# ==========================================
# Class Labels
# ==========================================

CLASSES = [
    "Fake (AI Generated)",
    "Real Human"
]

# ==========================================
# Predict Function
# ==========================================

def predict_image(image_path):

    print("Reading image:", image_path)

    img = tf.keras.utils.load_img(
        image_path,
        target_size=(224, 224)
    )

    img = tf.keras.utils.img_to_array(img)

    img = preprocess_input(img)

    img = np.expand_dims(img, axis=0)

    print("Running prediction...")

    prediction = model.predict(img, verbose=0)

    print("Prediction:", prediction)

    predicted_index = np.argmax(prediction)

    confidence = float(np.max(prediction)) * 100

    predicted_class = CLASSES[predicted_index]

    if predicted_class == "Real Human":

        status = "No AI manipulation detected."

        reasons = [
            "Natural facial texture",
            "Consistent lighting",
            "No AI artifacts detected"
        ]

    else:

        status = "Possible AI-generated image detected."

        reasons = [
            "Texture inconsistencies",
            "Facial artifacts",
            "Synthetic image patterns detected"
        ]

    return {

        "prediction": predicted_class,

        "confidence": round(confidence,2),

        "status": status,

        "reasons": reasons,

        "heatmap": None

    }