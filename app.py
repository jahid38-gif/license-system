from flask import Flask, request, jsonify

app = Flask(__name__)

def load_keys():
    with open("key.txt", "r") as f:
        return [line.strip() for line in f.readlines()]

@app.route("/")
def home():
    return "License Server Running"

@app.route("/check")
def check():
    key = request.args.get("key")
    keys = load_keys()

    if key in keys:
        return jsonify({"status": "valid"})
    else:
        return jsonify({"status": "invalid"})

@app.route("/all")
def all_keys():
    keys = load_keys()
    return jsonify({"total": len(keys), "keys": keys})
