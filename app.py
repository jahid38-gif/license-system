from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

GITHUB_RAW_URL = "https://raw.githubusercontent.com/jahid38-gif/license-system/main/key.txt"

@app.route("/")
def home():
    return "License Server Running"

@app.route("/check")
def check():
    key = request.args.get("key")

    try:
        res = requests.get(GITHUB_RAW_URL)
        keys = res.text.splitlines()

        if key in keys:
            return jsonify({"status": "valid"})
        else:
            return jsonify({"status": "invalid"})
    except:
        return jsonify({"status": "error"})

app.run(host="0.0.0.0", port=10000)
