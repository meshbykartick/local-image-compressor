from flask import Flask, request, send_file, jsonify
from PIL import Image
import io, os

app = Flask(__name__, static_folder="static", static_url_path="")

# -------- Serve the frontend (index.html) --------
@app.route("/")
def home():
    return app.send_static_file("index.html")

# -------- Check server status --------
@app.route("/status")
def status():
    return jsonify({"status": "online"})

# -------- Compress image endpoint --------
@app.route("/compress", methods=["POST"])
def compress_image():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]

    try:
        # Open image
        img = Image.open(file)

        # Convert PNG to JPEG if needed
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        # Compress image
        buf = io.BytesIO()
        img.save(buf, format="JPEG", optimize=True, quality=40)
        buf.seek(0)

        return send_file(
            buf,
            mimetype="image/jpeg",
            as_attachment=True,
            download_name="compressed.jpg",
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
