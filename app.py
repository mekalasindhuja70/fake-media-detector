import os
import uuid

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

        if "file" not in request.files:
            return redirect(request.url)


        file = request.files["file"]


        if file.filename == "":
            return redirect(request.url)


        filename = secure_filename(file.filename)


        # Avoid duplicate filenames
        unique_filename = (
            str(uuid.uuid4()) + "_" + filename
        )


        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            unique_filename
        )


        file.save(filepath)



        # ===================================
        # Prediction
        # ===================================

        result = predict_image(filepath)



        # ===================================
        # Dashboard Statistics
        # ===================================

        total_scans += 1


        if result["prediction"] == "Real Human":
            real_count += 1
        else:
            fake_count += 1



        # ===================================
        # Save History
        # ===================================

        history.append({

            "image": unique_filename,

            "prediction": result["prediction"],

            "status": result["status"]

        })



        # ===================================
        # Generate PDF Report
        # ===================================

        pdf_file = generate_pdf(

            result["prediction"],

            result["status"],

            filepath,

            None

        )



        # ===================================
        # Result Page
        # ===================================

        return render_template(

            "result.html",

            prediction=result["prediction"],

            status=result["status"],

            reasons=result["reasons"],

            image=unique_filename,

            heatmap=result["heatmap"],

            pdf=pdf_file

        )


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
# REST API
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

        debug=False

    )