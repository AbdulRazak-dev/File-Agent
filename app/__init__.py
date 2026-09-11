from flask import Flask, render_template, request, jsonify
import os


def create_app():
    app = Flask(__name__)

    upload_folder = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "uploads"
    )

    os.makedirs(upload_folder, exist_ok=True)

    app.config["UPLOAD_FOLDER"] = upload_folder

    @app.route("/")
    def home():
        return render_template("index.html")

    @app.route("/upload", methods=["POST"])
    def upload_document():

        if "document" not in request.files:
            return jsonify({
                "success": False,
                "message": "No document uploaded"
            }), 400

        file = request.files["document"]

        if file.filename == "":
            return jsonify({
                "success": False,
                "message": "No file selected"
            }), 400

        allowed_extensions = {"pdf", "doc", "docx"}

        extension = file.filename.rsplit(".", 1)[-1].lower()

        if extension not in allowed_extensions:
            return jsonify({
                "success": False,
                "message": "Only PDF and Word documents are allowed"
            }), 400

        file_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            file.filename
        )

        file.save(file_path)

        return jsonify({
            "success": True,
            "message": "Document uploaded successfully",
            "filename": file.filename
        })

    return app
