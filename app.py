from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

def load_keys():
    try:
        with open("key.txt", "r") as f:
            return [line.strip() for line in f.readlines()]
    except:
        return []

def save_keys(keys):
    with open("key.txt", "w") as f:
        for key in keys:
            f.write(key + "\n")

@app.route("/")
def home():
    return "Server Running"

@app.route("/get_keys")
def get_keys():
    return jsonify(load_keys())

@app.route("/add_key", methods=["POST"])
def add_key():
    key = request.json.get("key")
    keys = load_keys()
    if key not in keys:
        keys.append(key)
        save_keys(keys)
    return jsonify({"status": "added"})

@app.route("/delete_key", methods=["POST"])
def delete_key():
    key = request.json.get("key")
    keys = load_keys()
    keys = [k for k in keys if k != key]
    save_keys(keys)
    return jsonify({"status": "deleted"})


@app.route("/dashboard")
def dashboard():
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
<title>Dashboard</title>

<style>

body {
    margin:0;
    font-family:Arial;
    background: linear-gradient(135deg,#0f2027,#2c5364);
    color:white;
}

/* HEADER */
h1 {
    text-align:center;
    margin:20px;
}

/* BOX */
.container {
    width:80%;
    margin:auto;
}

.row {
    display:flex;
    gap:20px;
    margin-bottom:20px;
}

.card {
    flex:1;
    padding:30px;
    border-radius:12px;
    text-align:center;
    font-size:20px;
    font-weight:bold;
}

.red { background:#ff3b3b; }
.green { background:#2ecc71; }

.btn {
    flex:1;
    padding:15px;
    border:none;
    border-radius:10px;
    font-size:18px;
    cursor:pointer;
}

.manage { background:#7bed9f; }
.generate { background:#3498db; color:white; }

/* POPUP */
.overlay {
    position:fixed;
    top:0;
    left:0;
    width:100%;
    height:100%;
    background:rgba(0,0,0,0.6);
    display:none;
    justify-content:center;
    align-items:center;
}

.popup {
    background:#1e2a38;
    padding:20px;
    border-radius:12px;
    width:500px;
}

/* KEY ROW */
.key-row {
    display:flex;
    justify-content:space-between;
    margin:10px 0;
}

button.small {
    padding:5px 10px;
    margin-left:5px;
}

</style>
</head>

<body>

<h1>🔥 License Dashboard</h1>

<div class="container">

    <div class="row">
        <div class="card red">
            Inactive <br> 0
        </div>

        <div class="card green">
            Active <br> <span id="total">0</span>
        </div>
    </div>

    <div class="row">
        <button class="btn manage" onclick="openManage()">Manage Key</button>
        <button class="btn generate" onclick="openAdd()">Generate Key</button>
    </div>

</div>

<!-- MANAGE POPUP -->
<div class="overlay" id="manageBox">
    <div class="popup">
        <h2>Manage Keys</h2>
        <div id="keyList"></div>
        <button onclick="closeAll()">Close</button>
    </div>
</div>

<!-- ADD POPUP -->
<div class="overlay" id="addBox">
    <div class="popup">
        <h2>Add Key</h2>
        <input id="newKey">
        <button onclick="addKey()">Add</button>
        <button onclick="closeAll()">Close</button>
    </div>
</div>

<script>

function loadKeys(){
    fetch("/get_keys")
    .then(r=>r.json())
    .then(data=>{
        document.getElementById("total").innerText = data.length

        let html=""
        data.forEach(k=>{
            html += `
            <div class="key-row">
                <span>${k}</span>
                <div>
                    <button class="small">ON</button>
                    <button class="small">OFF</button>
                    <button class="small" onclick="deleteKey('${k}')">Delete</button>
                </div>
            </div>`
        })

        document.getElementById("keyList").innerHTML = html
    })
}

function addKey(){
    let key=document.getElementById("newKey").value
    fetch("/add_key",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({key:key})
    }).then(()=>{loadKeys();closeAll()})
}

function deleteKey(k){
    fetch("/delete_key",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({key:k})
    }).then(()=>loadKeys())
}

function openManage(){
    document.getElementById("manageBox").style.display="flex"
    loadKeys()
}

function openAdd(){
    document.getElementById("addBox").style.display="flex"
}

function closeAll(){
    document.getElementById("manageBox").style.display="none"
    document.getElementById("addBox").style.display="none"
}

loadKeys()

</script>

</body>
</html>
""")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
