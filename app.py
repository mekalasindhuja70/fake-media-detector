import os
import numpy as np
import tensorflow as tf
from flask import Flask, render_template, request, redirect
from keras import models

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load your fine-tuned model
MODEL_PATH = "model/fake_media_detector_finetuned.keras"
if os.path.exists(MODEL_PATH):
    model = models.load_model(MODEL_PATH)
    print("Successfully loaded the fine-tuned model!")
else:
    model = None
    print("Warning: Fine-tuned model not found!")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            
            if model is None:
                return render_template('index.html', result="Model Error: Fine-tuned model missing.")

            # Process image for the model (224x224)
            img = tf.keras.utils.load_img(file_path, target_size=(224, 224))
            img_array = tf.keras.utils.img_to_array(img)
            img_array = tf.expand_dims(img_array, 0)

            # Predict
            predictions = model.predict(img_array, verbose=0)
            classes = ['Fake (AI Generated)', 'Real Human']
            verdict = classes[np.argmax(predictions[0])]
            
            return render_template('index.html', result=verdict)

    return render_template('index.html', result=None)

if __name__ == '__main__':
    app.run(debug=True)