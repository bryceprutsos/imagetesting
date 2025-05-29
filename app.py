from flask import Flask, request, Response
import re
import requests
import base64

app = Flask(__name__)

# Set your Basic Auth username and password here update here
USERNAME = "admin"
PASSWORD = "Qz8#xLp2!vTa9wRf3*B7dPfH6sMkG5jLq"

def check_auth(auth_header):
    if not auth_header or not auth_header.startswith("Basic "):
        return False
    try:
        auth_decoded = base64.b64decode(auth_header.split(" ")[1]).decode("utf-8")
        username, password = auth_decoded.split(":", 1)
        return username == USERNAME and password == PASSWORD
    except Exception:
        return False

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        "Could not verify your access level for that URL.\n"
        "You have to login with proper credentials", 401,
        {"WWW-Authenticate": 'Basic realm="Login Required"'}
    )

@app.route("/GetImage", methods=["GET"])
def get_image():
    # Basic Auth check
    auth = request.headers.get("Authorization")
    if not check_auth(auth):
        return authenticate()

    image_id = request.args.get("IMAGE.ID", "")

    if re.fullmatch(r"\d{7}", image_id):
        image_url = f"https://chaffeytestblob.blob.core.windows.net/student/{image_id}.jpeg"
        response = requests.get(image_url)
        if response.status_code == 200:
            return Response(response.content, mimetype="image/jpeg")
        else:
            return "Error fetching image", 500
    else:
        return "Invalid IMAGE.ID. It must be exactly 7 digits.", 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
