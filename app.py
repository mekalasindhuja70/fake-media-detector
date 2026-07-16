import os
import uuid
import traceback

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    send_from_directory
)

from werkzeug.utils import secure_filename

from predict import predict_image
from report_generator import generate_pdf


app = Flask(__name__)

# ===================================================
# Configuration
# ===================================================

UPLOAD_FOLDER = os.path.join("static", "uploads")
HEATMAP_FOLDER = os.path.join("static", "heatmaps")
REPORT_FOLDER = "reports"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(HEATMAP_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# ===================================================
# Dashboard Variables
# ===================================================

total_scans = 0
real_count = 0
fake_count = 0

history = []

# ===================================================
# Home Page
# ===================================================

@app.route("/", methods=["GET", "POST"])
def index():

    global total_scans, real_count, fake_count, history

    if request.method == "POST":

        print("\n========== NEW REQUEST ==========")

        if "file" not in request.files:
            print("ERROR : No file part found")
            return render_template(
                "index.html",
                result="No image selected."
            )

        file = request.files["file"]

        if file.filename == "":
            print("ERROR : Empty filename")
            return render_template(
                "index.html",
                result="Please choose an image."
            )

        filename = secure_filename(file.filename)

        unique_filename = str(uuid.uuid4()) + "_" + filename

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            unique_filename
        )

        file.save(filepath)

        print("Image Saved :", filepath)

        try:

            print("Running Prediction...")

            result = predict_image(filepath)

            print("Prediction Completed")
            print(result)

            total_scans += 1

            if result["prediction"] == "Real Human":
                real_count += 1
            else:
                fake_count += 1

            history.append({
                "image": unique_filename,
                "prediction": result["prediction"],
                "status": result["status"]
            })

            print("Generating PDF...")

            pdf_file = generate_pdf(
                result["prediction"],
                result["status"],
                filepath,
                None
            )

            print("PDF Generated :", pdf_file)

            return render_template(
                "result.html",
                prediction=result["prediction"],
                status=result["status"],
                reasons=result["reasons"],
                image=unique_filename,
                heatmap=result["heatmap"],
                pdf=pdf_file
            )

        except Exception as e:

            print("\n========== ERROR ==========")
            traceback.print_exc()

            return f"""
            <h2>Application Error</h2>
            <pre>{e}</pre>
            """

    return render_template("index.html")

# ===================================================
# Dashboard
# ===================================================

@app.route("/dashboard")
def dashboard():

    return render_template(
        "dashboard.html",
        total_scans=total_scans,
        real_count=real_count,
        fake_count=fake_count,
        history=history
    )

# ===================================================
# History
# ===================================================

@app.route("/history")
def history_page():

    return render_template(
        "history.html",
        history=history
    )

# ===================================================
# Download PDF
# ===================================================

@app.route("/download/<filename>")
def download_report(filename):

    return send_from_directory(
        REPORT_FOLDER,
        filename,
        as_attachment=True
    )

# ===================================================
# API
# ===================================================

@app.route("/api")
def api():

    return {
        "total_scans": total_scans,
        "real_images": real_count,
        "fake_images": fake_count,
        "history": history
    }

# ===================================================
# Run Flask
# ===================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=True
    )