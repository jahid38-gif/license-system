from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# 🔹 Load keys from file
def load_keys():
    with open("key.txt", "r") as f:
        return [line.strip() for line in f.readlines()]

# 🔹 Home route
@app.route("/")
def home():
    return "License Server Running"

# 🔹 Check key
@app.route("/check")
def check():
    key = request.args.get("key")
    keys = load_keys()

    if key in keys:
        return jsonify({"status": "valid"})
    else:
        return jsonify({"status": "invalid"})

# 🔹 Get all keys
@app.route("/all")
def all_keys():
    keys = load_keys()
    return jsonify({
        "total": len(keys),
        "keys": keys
    })

# 🔥 IMPORTANT (Render fix)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
