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
    background: linear-gradient(135deg,#0f2027,#2c5364);
    color:white;
    font-family:Arial;
    text-align:center;
}

.box {display:flex;justify-content:space-around;margin:20px;}
.card {padding:30px;border-radius:10px;width:40%;}
.red{background:red;}
.green{background:green;}

.btn {
    padding:15px;
    width:40%;
    margin:10px;
    border:none;
    border-radius:10px;
    cursor:pointer;
    font-size:18px;
}

.manage{background:lime;}
.generate{background:blue;color:white;}

.popup {
    display:none;
    position:fixed;
    top:50%;
    left:50%;
    transform:translate(-50%,-50%);
    background:#1e2a38;
    padding:20px;
    border-radius:10px;
    width:60%;
}

</style>
</head>

<body>

<h1>🔥 License Dashboard</h1>

<div class="box">
    <div class="card red">
        <h2>Inactive</h2>
        <p>0</p>
    </div>

    <div class="card green">
        <h2>Active</h2>
        <p id="total">0</p>
    </div>
</div>

<button class="btn manage" onclick="openManage()">Manage Key</button>
<button class="btn generate" onclick="openAdd()">Generate Key</button>

<!-- MANAGE POPUP -->
<div class="popup" id="manageBox">
    <h2>Manage Keys</h2>
    <div id="keyList"></div>
    <button onclick="closeAll()">Close</button>
</div>

<!-- ADD POPUP -->
<div class="popup" id="addBox">
    <h2>Add Key</h2>
    <input id="newKey">
    <button onclick="addKey()">Add</button>
    <button onclick="closeAll()">Close</button>
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
            <p>
                ${k}
                <button onclick="deleteKey('${k}')">Delete</button>
            </p>`
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
    document.getElementById("manageBox").style.display="block"
    loadKeys()
}

function openAdd(){
    document.getElementById("addBox").style.display="block"
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
