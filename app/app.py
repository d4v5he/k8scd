import os
import boto3
from flask import Flask, render_template, send_file
import json
import tempfile

# Flask app
app = Flask(__name__)

# Load welcome message from config file
def load_config(config_path="config.json"):
    try:
        with open(config_path, "r") as file:
            config = json.load(file)
        return config.get("welcome_message", "Welcome to the Photo Viewer!")
    except FileNotFoundError:
        return "Welcome to the Photo Viewer!"

# Get photo file names from S3
def get_s3_photos(bucket_name):
    s3 = boto3.client("s3")
    try:
        objects = s3.list_objects_v2(Bucket=bucket_name)
        if "Contents" in objects:
            return [obj["Key"] for obj in objects["Contents"] if obj["Key"].lower().endswith((".png", ".jpg", ".jpeg"))]
        return []
    except Exception as e:
        print(f"Error retrieving files from S3: {e}")
        return []

# Download photo from S3
def download_photo(bucket_name, key):
    s3 = boto3.client("s3")
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    try:
        s3.download_fileobj(bucket_name, key, temp_file)
        temp_file.close()
        return temp_file.name
    except Exception as e:
        print(f"Error downloading {key}: {e}")
        return None

@app.route("/")
def index():
    bucket_name = os.getenv("S3_BUCKET_NAME")
    if not bucket_name:
        return "Error: S3_BUCKET_NAME environment variable not set."

    welcome_message = load_config()
    photos = get_s3_photos(bucket_name)

    return render_template("index.html", welcome_message=welcome_message, photos=photos)

@app.route("/photo/<path:photo_key>")
def photo(photo_key):
    bucket_name = os.getenv("S3_BUCKET_NAME")
    file_path = download_photo(bucket_name, photo_key)
    if file_path:
        return send_file(file_path, mimetype="image/jpeg")
    return "Error downloading photo.", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
