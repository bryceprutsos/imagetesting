from flask import Flask, request, Response
import re
import requests

app = Flask(__name__)

@app.route("/GetImage", methods=["GET"])
def get_image():
    image_id = request.args.get("IMAGE.ID", "")

    if re.fullmatch(r"\d{7}", image_id):
        image_url = "https://chaffeytestblob.blob.core.windows.net/student/0979951.jpeg"
        response = requests.get(image_url)
        if response.status_code == 200:
            return Response(response.content, mimetype="image/jpeg")
        else:
            return "Error fetching image", 500
    else:
        return "Invalid IMAGE.ID. It must be exactly 7 digits.", 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
