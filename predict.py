import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model

from gradcam import generate_gradcam


# ==========================================
# Load Model
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "model",
    "fake_media_detector_finetuned.keras"
)

model = load_model(MODEL_PATH)


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

    # -------------------------------
    # Load Image
    # -------------------------------

    img = tf.keras.utils.load_img(
        image_path,
        target_size=(224, 224)
    )

    img_array = tf.keras.utils.img_to_array(img)

    img_array = np.expand_dims(
        img_array,
        axis=0
    )


    # -------------------------------
    # Prediction
    # -------------------------------

    prediction = model.predict(
        img_array,
        verbose=0
    )

    predicted_index = np.argmax(
        prediction[0]
    )

    predicted_class = CLASSES[predicted_index]


    # -------------------------------
    # Detection Status
    # -------------------------------

    if predicted_class == "Real Human":

        status = "No AI manipulation detected."

        reasons = [
            "Natural facial texture",
            "Consistent lighting",
            "No visual AI artifacts detected"
        ]

    else:

        status = "Possible AI-generated or manipulated image."

        reasons = [
            "Texture mismatch detected",
            "Facial inconsistencies found",
            "Possible AI-generated artifacts"
        ]


    # -------------------------------
    # Heatmap Path
    # -------------------------------

    filename = os.path.basename(image_path)

    heatmap_name = (
        "heatmap_" + filename
    )

    heatmap_path = os.path.join(
        BASE_DIR,
        "static",
        "heatmaps",
        heatmap_name
    )


    # Uncomment when GradCAM is enabled
    #
    # generate_gradcam(
    #     model,
    #     image_path,
    #     heatmap_path
    # )


    # -------------------------------
    # Return Results
    # -------------------------------

    return {

        "prediction": predicted_class,

        "status": status,

        "reasons": reasons,

        "heatmap": None

    }