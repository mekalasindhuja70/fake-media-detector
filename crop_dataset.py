import cv2
import os

# Load the built-in face detector from OpenCV
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def crop_faces_in_folder(folder_path):
    print(f"Cropping faces in: {folder_path}")
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(folder_path, filename)
            img = cv2.imread(img_path)
            
            if img is None:
                continue
                
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            
            # If a face is found, crop it and overwrite the original image
            for (x, y, w, h) in faces:
                # Add a little padding around the face so it's not too tight
                padding = int(w * 0.1)
                y_start = max(0, y - padding)
                y_end = min(img.shape[0], y + h + padding)
                x_start = max(0, x - padding)
                x_end = min(img.shape[1], x + w + padding)
                
                cropped_face = img[y_start:y_end, x_start:x_end]
                cv2.imwrite(img_path, cropped_face)
                break # Only take the first face found

# Run the cropper on both of your dataset folders
crop_faces_in_folder("dataset/real")
crop_faces_in_folder("dataset/fake")
print("All backgrounds removed! Your dataset now contains ONLY faces.")