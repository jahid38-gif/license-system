from flask import Flask, request, redirect, render_template_string, jsonify, session
import os

app = Flask(__name__)
app.secret_key = "secret123"

# 🔐 LOGIN (PHP STYLE)
USERNAME = "Jahid"
PASSWORD = "@Jahid.Hasan20034#"

FILE = "keys.txt"

# ================= LOAD =================
def load_keys():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r") as f:
        return [line.strip() for line in f.readlines() if "|" in line]

def save_keys(keys):
    with open(FILE, "w") as f:
        f.write("\n".join(keys))

# ================= LOGIN =================
@app.route("/login", methods=["GET", "POST"])
def login():
    error = ""

    if request.method == "POST":
        user = request.form.get("username")
        pw = request.form.get("password")

        if user == USERNAME and pw == PASSWORD:
            session["logged_in"] = True
            return redirect("/dashboard")
        else:
            error = "Wrong Login!"

    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
<title>Login</title>

<style>
body{
    background:#0f172a;
    color:white;
    font-family:Arial;
    display:flex;
    justify-content:center;
    align-items:center;
    height:100vh;
    margin:0;
}

.box{
    background:#1e293b;
    padding:40px;
    border-radius:15px;
    text-align:center;
    width:350px;
    box-shadow:0 0 30px rgba(0,0,0,0.5);
}

input{
    width:100%;
    padding:12px;
    margin:10px 0;
    border:none;
    border-radius:8px;
}

button{
    width:100%;
    padding:12px;
    background:#22c55e;
    border:none;
    color:white;
    border-radius:8px;
    cursor:pointer;
}

.error{
    color:red;
    margin-top:10px;
}
</style>

</head>

<body>

<div class="box">
<h2>🔐 Admin Login</h2>

<form method="POST">
<input type="text" name="username" placeholder="Username">
<input type="password" name="password" placeholder="Password">
<button>Login</button>
</form>

<p class="error">{{error}}</p>

</div>

</body>
</html>
""", error=error)

# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ================= ROOT FIX =================
@app.route("/")
def home():
    return redirect("/dashboard")

# ================= ADD =================
@app.route("/add", methods=["POST"])
def add():
    key = request.form.get("new_key", "").strip().upper()
    if key:
        with open(FILE, "a") as f:
            f.write(f"{key}|active\n")
    return redirect("/dashboard")

# ================= TOGGLE =================
@app.route("/toggle")
def toggle():
    key = request.args.get("toggle")
    set_status = request.args.get("set")

    keys = load_keys()
    new_keys = []

    for line in keys:
        parts = line.split("|")
        if len(parts) != 2:
            continue
        k, s = parts

        if k == key:
            new_keys.append(f"{k}|{set_status}")
        else:
            new_keys.append(line)

    save_keys(new_keys)
    return redirect("/dashboard")

# ================= DELETE =================
@app.route("/delete")
def delete():
    key = request.args.get("delete")

    keys = load_keys()
    keys = [line for line in keys if "|" in line and line.split("|")[0] != key]

    save_keys(keys)
    return redirect("/dashboard")

# ================= CHECK API =================
@app.route("/check/<key>")
def check_key(key):

    device = request.args.get("device")  # 🔥 NEW
    keys = load_keys()

    new_keys = []
    found = False

    for line in keys:
        parts = line.split("|")

        if len(parts) < 2:
            continue

        k = parts[0]
        s = parts[1]

        saved_device = parts[2] if len(parts) >= 3 else ""

        if k == key:
            found = True

            # ❌ inactive
            if s != "active":
                return jsonify({
                    "key": k,
                    "status": s,
                    "valid": False
                })

            # 🔥 first time bind
            if saved_device == "":
                new_line = f"{k}|{s}|{device}"
                
                for l in keys:
                    if l.startswith(k + "|"):
                        continue
                    new_keys.append(l)
                new_keys.append(new_line)

                save_keys(new_keys)

                return jsonify({
                    "key": k,
                    "status": "active",
                    "valid": True
                })

            # ✅ same device
            if saved_device == device:
                return jsonify({
                    "key": k,
                    "status": "active",
                    "valid": True
                })

            # ❌ other device
            else:
                return jsonify({
                    "key": k,
                    "status": "used_on_other_device",
                    "valid": False
                })

    return jsonify({
        "key": key,
        "status": "not_found",
        "valid": False
    })

# ================= SERVER CHECK =================
@app.route("/ping")
def ping():
    return jsonify({"status": "server running"})

# ================= DASHBOARD =================
@app.route("/dashboard")
def dashboard():

    # 🔐 SECURITY CHECK
    if not session.get("logged_in"):
        return redirect("/login")

    keys = load_keys()

    active = 0
    inactive = 0

    parsed = []

    for line in keys:
        parts = line.split("|")
        if len(parts) != 2:
            continue

        k, s = parts
        parsed.append((k, s))

        if s == "active":
            active += 1
        else:
            inactive += 1

    return render_template_string(""" 
<!DOCTYPE html>
<html>
<head>
<title>Dashboard</title>

<style>
body{
    background:#0f172a;
    font-family:Arial;
    color:white;
    padding:30px;
}
.top{
    display:flex;
    justify-content:space-between;
    align-items:center;
    margin-bottom:30px;
}
.grid{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:25px;
}
.box{
    padding:50px;
    border-radius:20px;
    text-align:center;
    font-size:35px;
    font-weight:bold;
}
.red{background:#ef4444;}
.green{background:#22c55e;}
.cyan{
    grid-column:1/3;
    background:linear-gradient(90deg,#06b6d4,#14b8a6);
}
.btn-box{
    padding:30px;
    border-radius:15px;
    font-size:22px;
    font-weight:bold;
    cursor:pointer;
    text-align:center;
}
.yellow{background:#84cc16;}
.blue{background:#3b82f6;}
.popup{
    display:none;
    position:fixed;
    top:0;
    left:0;
    width:100%;
    height:100%;
    background:rgba(0,0,0,0.7);
}
.popup-content{
    background:#1e293b;
    margin:5% auto;
    padding:20px;
    width:50%;
    border-radius:15px;
}
.scroll-box{
    max-height:400px;
    overflow-y:auto;
}
.key-row{
    background:#0f172a;
    padding:12px;
    margin:10px 0;
    border-radius:10px;
    display:flex;
    justify-content:space-between;
}
.close{
    float:right;
    color:red;
    cursor:pointer;
    font-size:22px;
}
.logout{
    position:absolute;
    top:20px;
    right:30px;
    color:white;
    text-decoration:none;
}
</style>
</head>

<body>

<a href="/logout" class="logout">Logout</a>

<div class="top">
<h1>🔥 License Dashboard</h1>
</div>

<div class="grid">

<div class="box red">
{{inactive}}<br>Inactive
</div>

<div class="box green">
{{active}}<br>Active
</div>

<div class="btn-box yellow" onclick="openManage()">
Manage Key
</div>

<div class="btn-box blue" onclick="openAdd()">
Generate Key
</div>

<div class="box cyan">
{{total}}<br>All Key
</div>

</div>

<!-- MANAGE -->
<div id="managePopup" class="popup">
<div class="popup-content">

<span class="close" onclick="closeManage()">✖</span>
<h2>🔑 Manage Key</h2>

<div class="scroll-box">

{% for k,s in keys %}

<div class="key-row">

<div>
{{k}} →
<span style="color:{{'lime' if s=='active' else 'red'}};">
{{s}}
</span>
</div>

<div>

<a href="/toggle?toggle={{k}}&set=inactive"
style="padding:5px 10px;
background:{{'red' if s=='inactive' else '#333'}};
color:white;border-radius:5px;">
OFF</a>

<a href="/toggle?toggle={{k}}&set=active"
style="padding:5px 10px;
background:{{'red' if s=='active' else '#333'}};
color:white;border-radius:5px;">
ON</a>

<a href="/delete?delete={{k}}" style="color:red;margin-left:10px;">
Delete
</a>

</div>

</div>

{% endfor %}

</div>
</div>
</div>

<!-- ADD -->
<div id="addPopup" class="popup">
<div class="popup-content" style="width:35%; text-align:center;">

<span class="close" onclick="closeAdd()">✖</span>

<h2>🔑 Add Key</h2>

<form action="/add" method="POST">
<input type="text" name="new_key" placeholder="Enter Key"
style="width:80%;padding:10px;border-radius:8px;border:none;">

<br><br>

<button type="submit"
style="padding:10px 25px;background:#16a34a;border:none;color:white;border-radius:8px;">
Add
</button>
</form>

</div>
</div>

<script>
function openManage(){ document.getElementById("managePopup").style.display="block"; }
function closeManage(){ document.getElementById("managePopup").style.display="none"; }
function openAdd(){ document.getElementById("addPopup").style.display="block"; }
function closeAdd(){ document.getElementById("addPopup").style.display="none"; }
</script>

</body>
</html>
""", keys=parsed, active=active, inactive=inactive, total=len(parsed))


# ================= RUN =================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
