from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

def load_keys():
    with open("key.txt", "r") as f:
        return [line.strip() for line in f.readlines()]

def save_keys(keys):
    with open("key.txt", "w") as f:
        for key in keys:
            f.write(key + "\n")

@app.route("/")
def home():
    return "License Server Running"

# 🔥 DASHBOARD PAGE
@app.route("/dashboard")
def dashboard():
    keys = load_keys()
    return render_template_string("""
    <h1>License Dashboard</h1>
    <p>Total Keys: {{total}}</p>

    <h3>Keys:</h3>
    <ul>
    {% for key in keys %}
        <li>{{key}}</li>
    {% endfor %}
    </ul>

    <h3>Add Key</h3>
    <form action="/add" method="post">
        <input name="key">
        <button type="submit">Add</button>
    </form>
    """, keys=keys, total=len(keys))


# 🔥 ADD KEY
@app.route("/add", methods=["POST"])
def add_key():
    new_key = request.form.get("key")
    keys = load_keys()

    if new_key and new_key not in keys:
        keys.append(new_key)
        save_keys(keys)

    return "Added! <a href='/dashboard'>Back</a>"


# 🔥 CHECK API
@app.route("/check")
def check():
    key = request.args.get("key")
    keys = load_keys()

    if key in keys:
        return jsonify({"status": "valid"})
    else:
        return jsonify({"status": "invalid"})


# 🔥 ALL KEYS API
@app.route("/all")
def all_keys():
    keys = load_keys()
    return jsonify({"total": len(keys), "keys": keys})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
