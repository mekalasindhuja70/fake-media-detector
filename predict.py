import tensorflow as tf
import numpy as np
import os

# 1. Configuration Paths
MODEL_PATH = "model/fake_media_detector_finetuned.keras"
TEST_IMAGE = "test_face.jpg"

if not os.path.exists(MODEL_PATH):
    print(f"Error: Could not find '{MODEL_PATH}'. Wait for fine-tuning to finish!")
elif not os.path.exists(TEST_IMAGE):
    print(f"Error: Could not find '{TEST_IMAGE}'. Make sure you saved a test image!")
else:
    # Load the trained network
    model = tf.keras.models.load_model(MODEL_PATH)
    
    # Process the test photo
    img = tf.keras.utils.load_img(TEST_IMAGE, target_size=(224, 224))
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0) 

    # Run the prediction
    predictions = model.predict(img_array, verbose=0) # verbose=0 hides loading bars
    
    # Map the calculation directly to your text classes
    classes = ['Fake (AI Generated)', 'Real Human']
    predicted_class = classes[np.argmax(predictions[0])]

    # 2. Print Only the Clean Result
    print("\n" + "="*40)
    print(f" FINAL VERDICT: {predicted_class}")
    print("="*40 + "\n")