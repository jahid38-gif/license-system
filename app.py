from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# 🔥 KEY STORAGE (key: status)
keys = {
    "JAHID_11": "active",
    "HASAN_11": "active"
}

# ================= API =================

@app.route("/get_keys")
def get_keys():
    return jsonify(keys)

@app.route("/add_key", methods=["POST"])
def add_key():
    data = request.json
    key = data.get("key")

    if key:
        keys[key] = "active"

    return jsonify({"status": "ok"})

@app.route("/delete_key", methods=["POST"])
def delete_key():
    data = request.json
    key = data.get("key")

    if key in keys:
        del keys[key]

    return jsonify({"status": "ok"})

@app.route("/toggle_key", methods=["POST"])
def toggle_key():
    data = request.json
    key = data.get("key")
    status = data.get("status")

    if key in keys:
        keys[key] = status

    return jsonify({"status": "ok"})


# ================= DASHBOARD =================

@app.route("/dashboard")
def dashboard():
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
<title>Dashboard</title>

<style>

body{
    margin:0;
    font-family:sans-serif;
    background: linear-gradient(135deg,#0f2027,#203a43,#2c5364);
    color:white;
}

.title{
    text-align:center;
    font-size:28px;
    margin:20px;
}

.container{
    width:80%;
    margin:auto;
}

.row{
    display:flex;
    gap:20px;
    margin-bottom:20px;
}

.card{
    flex:1;
    padding:30px;
    border-radius:15px;
    text-align:center;
    font-size:22px;
    backdrop-filter: blur(10px);
    box-shadow:0 0 20px rgba(0,0,0,0.5);
}

.red{
    background:linear-gradient(45deg,#ff416c,#ff4b2b);
}

.green{
    background:linear-gradient(45deg,#00c853,#64dd17);
}

.btn{
    flex:1;
    padding:15px;
    border:none;
    border-radius:10px;
    font-size:18px;
    cursor:pointer;
    transition:0.3s;
}

.btn:hover{
    transform:scale(1.05);
}

.manage{
    background:linear-gradient(45deg,#7bed9f,#2ed573);
}

.generate{
    background:linear-gradient(45deg,#1e90ff,#3742fa);
    color:white;
}

.overlay{
    position:fixed;
    top:0;
    left:0;
    width:100%;
    height:100%;
    background:rgba(0,0,0,0.7);
    display:none;
    justify-content:center;
    align-items:center;
}

.popup{
    width:500px;
    background:rgba(30,42,56,0.95);
    padding:20px;
    border-radius:15px;
    box-shadow:0 0 30px rgba(0,0,0,0.8);
}

.key-row{
    display:flex;
    justify-content:space-between;
    align-items:center;
    margin:10px 0;
    padding:10px;
    background:rgba(255,255,255,0.05);
    border-radius:8px;
}

.small{
    padding:5px 10px;
    margin-left:5px;
    border:none;
    border-radius:5px;
    cursor:pointer;
}

.on{ background:#2ecc71; }
.off{ background:#e67e22; }
.delete{ background:#e74c3c; color:white; }

input{
    width:100%;
    padding:10px;
    margin-bottom:10px;
    border-radius:8px;
    border:none;
}

</style>
</head>

<body>

<div class="title">🔥 License Dashboard</div>

<div class="container">

    <div class="row">
        <div class="card red">
            Inactive<br><span id="inactive">0</span>
        </div>

        <div class="card green">
            Active<br><span id="active">0</span>
        </div>
    </div>

    <div class="row">
        <button class="btn manage" onclick="openManage()">Manage Key</button>
        <button class="btn generate" onclick="openAdd()">Generate Key</button>
    </div>

</div>

<!-- MANAGE -->
<div class="overlay" id="manage">
    <div class="popup">
        <h2>Manage Keys</h2>
        <div id="list"></div>
        <button onclick="closeAll()">Close</button>
    </div>
</div>

<!-- ADD -->
<div class="overlay" id="add">
    <div class="popup">
        <h2>Add Key</h2>
        <input id="key" placeholder="Enter key">
        <button onclick="addKey()">Add</button>
        <button onclick="closeAll()">Close</button>
    </div>
</div>

<script>

function load(){
    fetch("/get_keys")
    .then(r=>r.json())
    .then(d=>{
        let active=0
        let inactive=0
        let html=""

        for(let k in d){

            if(d[k]=="active") active++
            else inactive++

            html+=`
            <div class="key-row">
                <span>${k} → ${d[k]}</span>
                <div>
                    <button class="small on" onclick="setStatus('${k}','active')">ON</button>
                    <button class="small off" onclick="setStatus('${k}','inactive')">OFF</button>
                    <button class="small delete" onclick="delKey('${k}')">Delete</button>
                </div>
            </div>`
        }

        document.getElementById("list").innerHTML=html
        document.getElementById("active").innerText=active
        document.getElementById("inactive").innerText=inactive
    })
}

function addKey(){
    let k=document.getElementById("key").value
    fetch("/add_key",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({key:k})
    }).then(()=>{load();closeAll()})
}

function delKey(k){
    fetch("/delete_key",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({key:k})
    }).then(()=>load())
}

function setStatus(k,status){
    fetch("/toggle_key",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({key:k,status:status})
    }).then(()=>load())
}

function openManage(){
    document.getElementById("manage").style.display="flex"
    load()
}

function openAdd(){
    document.getElementById("add").style.display="flex"
}

function closeAll(){
    document.getElementById("manage").style.display="none"
    document.getElementById("add").style.display="none"
}

load()

</script>

</body>
</html>
""")


# ================= RUN =================

if __name__ == "__main__":
    app.run(debug=True)
