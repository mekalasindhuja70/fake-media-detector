# 🛡️ Fake Media Detector

An AI-powered web application that detects whether an uploaded image is **Real** or **Fake (AI-generated/Manipulated)** using **EfficientNetB0**, **TensorFlow**, **Flask**, and **Grad-CAM** for explainable AI.

---

## 📌 Features

- Upload image through a modern web interface
- Detect Real or Fake images
- Confidence score for each prediction
- Grad-CAM heatmap visualization
- Prediction history stored in SQLite
- Dashboard with scan statistics
- Downloadable PDF prediction reports
- REST API for predictions
- Responsive UI

---

## 🏗️ Project Architecture

```
User
   │
   ▼
Flask Web Interface
   │
   ▼
Image Preprocessing
   │
   ▼
EfficientNetB0 Model
   │
   ├────────► Prediction Module
   │                │
   │                ▼
   │         Confidence Score
   │
   └────────► Grad-CAM
                    │
                    ▼
            Heatmap Generation
                    │
                    ▼
          Flask Backend Processing
                    │
      ┌─────────────┴─────────────┐
      ▼                           ▼
SQLite Database             PDF Report
      │                           │
      └─────────────┬─────────────┘
                    ▼
              Result Dashboard
```

---

## 🛠️ Tech Stack

### Frontend

- HTML5
- CSS3
- JavaScript
- Bootstrap

### Backend

- Flask
- Python

### Machine Learning

- TensorFlow
- Keras
- EfficientNetB0
- OpenCV
- NumPy
- Pillow

### Explainable AI

- Grad-CAM

### Database

- SQLite

### Report Generation

- ReportLab

---

## 📂 Project Structure

```
fake_media_detector/
│
├── app.py
├── train_model.py
├── predict.py
├── gradcam.py
├── requirements.txt
├── README.md
│
├── model/
│   └── fake_media_detector.keras
│
├── uploads/
├── reports/
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── result.html
│   └── dashboard.html
│
└── history.db
```

---

## 📁 Dataset Structure

```
dataset/
│
├── train/
│   ├── real/
│   └── fake/
│
└── val/
    ├── real/
    └── fake/
```

---

## 🚀 Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/fake_media_detector.git

cd fake_media_detector
```

---

### Create Virtual Environment

```bash
python -m venv venv
```

Windows

```bash
venv\Scripts\activate
```

Linux/Mac

```bash
source venv/bin/activate
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🧠 Train the Model

```bash
python train_model.py --data-dir dataset --epochs 15 --fine-tune-epochs 8
```

The trained model will be saved in:

```
model/fake_media_detector.keras
```

---

## ▶️ Run the Application

```bash
python app.py
```

Open your browser:

```
http://127.0.0.1:5000
```

---

## 📊 Workflow

1. Upload an image.
2. Image is preprocessed.
3. EfficientNetB0 predicts Real or Fake.
4. Confidence score is calculated.
5. Grad-CAM generates a heatmap.
6. Prediction is stored in SQLite.
7. PDF report is generated.
8. Result is displayed on the dashboard.

---

## 📄 API Endpoint

### Predict Image

```
POST /predict
```

Input

```
Image File
```

Output

```json
{
    "prediction": "Fake",
    "confidence": 96.82
}
```

---

## 📈 Future Enhancements

- Deepfake video detection
- AI-generated image detection
- Multi-class media classification
- Cloud deployment
- User authentication
- Batch image processing
- Mobile application
- Explainable AI improvements

---

## 📚 Technologies Used

- Python
- Flask
- TensorFlow
- Keras
- EfficientNetB0
- OpenCV
- NumPy
- Pillow
- SQLite
- ReportLab
- HTML
- CSS
- JavaScript
- Bootstrap

---

## 👩‍💻 Author

**M.Sindhuja**
**B.rishitha**
**m.priyambica**

BE – Computer Science and Engineering

Stanley College of Engineering & Technology for Women

---

## 📜 License

This project is developed for educational and academic purposes.
