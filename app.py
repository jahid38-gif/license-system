from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Load keys from file
def load_keys():
    try:
        with open("key.txt", "r") as f:
            return [line.strip() for line in f.readlines()]
    except:
        return []

# Save keys to file
def save_keys(keys):
    with open("key.txt", "w") as f:
        for key in keys:
            f.write(key + "\n")

# Home route
@app.route("/")
def home():
    return "License Server Running"

# Check key
@app.route("/check")
def check():
    key = request.args.get("key")
    keys = load_keys()

    if key in keys:
        return jsonify({"status": "valid"})
    else:
        return jsonify({"status": "invalid"})

# Get all keys (API)
@app.route("/all")
def all_keys():
    keys = load_keys()
    return jsonify({"total": len(keys), "keys": keys})

# Dashboard UI
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    keys = load_keys()

    if request.method == "POST":
        new_key = request.form.get("key")
        if new_key and new_key not in keys:
            keys.append(new_key)
            save_keys(keys)

    keys = load_keys()

    html = """
    <html>
    <head>
        <title>License Dashboard</title>
        <style>
            body {
                background: linear-gradient(135deg, #0f2027, #2c5364);
                color: white;
                font-family: Arial;
                text-align: center;
            }
            h1 { margin-top: 20px; }
            .box {
                display: flex;
                justify-content: space-around;
                margin: 20px;
            }
            .card {
                padding: 20px;
                border-radius: 10px;
                width: 40%;
                font-size: 20px;
            }
            .active { background: green; }
            .inactive { background: red; }

            .btn {
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                margin-top: 10px;
                cursor: pointer;
            }
            .input {
                padding: 10px;
                width: 200px;
            }
        </style>
    </head>
    <body>

        <h1>🔥 License Dashboard</h1>

        <div class="box">
            <div class="card inactive">
                <h2>Inactive</h2>
                <p>0</p>
            </div>

            <div class="card active">
                <h2>Active</h2>
                <p>{{ total }}</p>
            </div>
        </div>

        <h2>All Keys ({{ total }})</h2>

        <ul>
        {% for k in keys %}
            <li>{{ k }}</li>
        {% endfor %}
        </ul>

        <h3>Add Key</h3>
        <form method="POST">
            <input class="input" name="key" placeholder="Enter key" required>
            <button class="btn" type="submit">Add</button>
        </form>

    </body>
    </html>
    """

    return render_template_string(html, keys=keys, total=len(keys))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
