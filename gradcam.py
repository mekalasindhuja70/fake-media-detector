import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model

# ==========================================
# Generate Grad-CAM Heatmap
# ==========================================

def generate_gradcam(model, image_path, save_path):

    # Load Image
    img = tf.keras.utils.load_img(image_path, target_size=(224,224))

    img_array = tf.keras.utils.img_to_array(img)

    img_array = np.expand_dims(img_array, axis=0)

    # --------------------------------------
    # Find Last Convolution Layer
    # --------------------------------------

    last_conv_layer = None

    for layer in reversed(model.layers):
        if len(layer.output.shape) == 4:
            last_conv_layer = layer.name
            break

    if last_conv_layer is None:
        raise ValueError("No convolution layer found.")

    # --------------------------------------
    # Create GradCAM Model
    # --------------------------------------

    grad_model = Model(
        inputs=model.inputs,
        outputs=[
            model.get_layer(last_conv_layer).output,
            model.output
        ]
    )

    # --------------------------------------
    # Compute Gradient
    # --------------------------------------

    with tf.GradientTape() as tape:

        conv_outputs, predictions = grad_model(img_array)

        predicted_class = tf.argmax(predictions[0])

        loss = predictions[:, predicted_class]

    gradients = tape.gradient(loss, conv_outputs)

    pooled_gradients = tf.reduce_mean(
        gradients,
        axis=(0,1,2)
    )

    conv_outputs = conv_outputs[0]

    heatmap = conv_outputs @ pooled_gradients[..., tf.newaxis]

    heatmap = tf.squeeze(heatmap)

    heatmap = tf.maximum(heatmap,0)

    heatmap /= tf.reduce_max(heatmap)

    heatmap = heatmap.numpy()

    # --------------------------------------
    # Resize Heatmap
    # --------------------------------------

    original = cv2.imread(image_path)

    heatmap = cv2.resize(
        heatmap,
        (original.shape[1], original.shape[0])
    )

    heatmap = np.uint8(255 * heatmap)

    heatmap = cv2.applyColorMap(
        heatmap,
        cv2.COLORMAP_JET
    )

    superimposed = cv2.addWeighted(
        original,
        0.6,
        heatmap,
        0.4,
        0
    )

    cv2.imwrite(save_path, superimposed)

    return os.path.basename(save_path)