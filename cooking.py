import os
import cloudinary
import cloudinary.api
from flask import Flask, jsonify, request

app = Flask(__name__)
cloudinary.config(
	cloud_name = "gooseterv",
	api_key = os.getenv("CLOUDINARY_API_KEY"),
	api_secret = os.getenv("CLOUDINARY_API_SECRET"),
	secure = True
)
@app.route('/upload')
def index():
	galleryUrlHtml = "<pre>"
	for resource in cloudinary.api.resources(type="upload", prefix="cooking", max_results=500)["resources"]:
		galleryUrlHtml += f"<a href=\"{resource['secure_url']}\"> {resource['public_id']}.{resource['format']} </a>\n"
	galleryUrlHtml += "</pre>"
	print(galleryUrlHtml)
	return open("cooking.html").read().replace("\"{0}\"", os.getenv("CLOUDINARY_API_KEY")).replace("\"{1}\"", galleryUrlHtml)


if __name__ == "__main__":
	app.run(debug=True)