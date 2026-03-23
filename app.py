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
    margin: 0;
    font-family: Arial;
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}

.container {
    padding: 20px;
}

h1 {
    margin-bottom: 20px;
}

.grid {
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
}

.card {
    flex: 1;
    min-width: 250px;
    padding: 30px;
    border-radius: 12px;
    text-align: center;
    font-size: 22px;
    font-weight: bold;
}

.red {
    background: linear-gradient(45deg, #ff416c, #ff4b2b);
}

.green {
    background: linear-gradient(45deg, #00b09b, #96c93d);
}

.blue {
    background: linear-gradient(45deg, #2193b0, #6dd5ed);
}

.purple {
    background: linear-gradient(45deg, #7b2ff7, #f107a3);
}

.section {
    margin-top: 30px;
}

ul {
    background: #111;
    padding: 15px;
    border-radius: 10px;
}

li {
    padding: 5px;
}

input {
    padding: 10px;
    width: 250px;
    border-radius: 5px;
    border: none;
}

button {
    padding: 10px 15px;
    border: none;
    border-radius: 5px;
    background: #00c6ff;
    color: white;
    cursor: pointer;
}
</style>

</head>

<body>

<div class="container">

<h1>🔥 License Dashboard</h1>

<div class="grid">
    <div class="card red">0<br>Inactive</div>
    <div class="card green">{{total}}<br>Active</div>
</div>

<div class="grid">
    <div class="card blue">Manage Key</div>
    <div class="card purple">Generate Key</div>
</div>

<div class="section">
<h2>All Keys ({{total}})</h2>
<ul>
{% for key in keys %}
<li>{{key}}</li>
{% endfor %}
</ul>
</div>

<div class="section">
<h3>Add Key</h3>
<form action="/add" method="post">
<input name="key" placeholder="Enter key">
<button>Add</button>
</form>
</div>

</div>

</body>
</html>
""", keys=keys, total=total)
