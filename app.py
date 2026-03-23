@app.route("/dashboard")
def dashboard():
    keys = load_keys()
    total = len(keys)

    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>License Dashboard</title>
        <style>
            body {
                background: #0f172a;
                color: white;
                font-family: Arial;
                padding: 20px;
            }
            .box {
                padding: 20px;
                border-radius: 10px;
                margin: 10px;
                display: inline-block;
                width: 45%;
                text-align: center;
                font-size: 20px;
            }
            .red { background: linear-gradient(to right, red, orange); }
            .green { background: linear-gradient(to right, green, lime); }
            .blue { background: linear-gradient(to right, blue, cyan); }
            .teal { background: linear-gradient(to right, teal, lightgreen); }

            .btn {
                display: block;
                padding: 15px;
                margin: 10px 0;
                border-radius: 8px;
                text-align: center;
                background: #1e293b;
                color: white;
                text-decoration: none;
            }

            input {
                padding: 10px;
                width: 70%;
            }

            button {
                padding: 10px;
            }
        </style>
    </head>
    <body>

    <h1>🔥 License Dashboard</h1>

    <div class="box red">0 Inactive</div>
    <div class="box green">{{total}} Active</div>

    <div class="box blue">Manage Key</div>
    <div class="box teal">Generate Key</div>

    <h2>All Keys ({{total}})</h2>
    <ul>
        {% for key in keys %}
        <li>{{key}}</li>
        {% endfor %}
    </ul>

    <h3>Add Key</h3>
    <form action="/add" method="post">
        <input name="key" placeholder="Enter key">
        <button>Add</button>
    </form>

    </body>
    </html>
    """, keys=keys, total=total)
