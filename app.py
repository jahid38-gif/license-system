from flask import render_template_string

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

/* TITLE */
.title{
    text-align:center;
    font-size:28px;
    margin:20px;
}

/* GRID */
.container{
    width:80%;
    margin:auto;
}

.row{
    display:flex;
    gap:20px;
    margin-bottom:20px;
}

/* CARD */
.card{
    flex:1;
    padding:30px;
    border-radius:15px;
    text-align:center;
    font-size:22px;
    backdrop-filter: blur(10px);
    box-shadow:0 0 20px rgba(0,0,0,0.5);
}

/* COLORS */
.red{
    background:linear-gradient(45deg,#ff416c,#ff4b2b);
}

.green{
    background:linear-gradient(45deg,#00c853,#64dd17);
}

/* BUTTON */
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

/* OVERLAY */
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

/* POPUP */
.popup{
    width:500px;
    background:rgba(30,42,56,0.95);
    padding:20px;
    border-radius:15px;
    box-shadow:0 0 30px rgba(0,0,0,0.8);
}

/* KEY ROW */
.key-row{
    display:flex;
    justify-content:space-between;
    align-items:center;
    margin:10px 0;
    padding:10px;
    background:rgba(255,255,255,0.05);
    border-radius:8px;
}

/* SMALL BTN */
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
            Inactive<br>0
        </div>

        <div class="card green">
            Active<br><span id="total">0</span>
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
        <input id="key">
        <button onclick="addKey()">Add</button>
        <button onclick="closeAll()">Close</button>
    </div>
</div>

<script>

function load(){
    fetch("/get_keys")
    .then(r=>r.json())
    .then(d=>{
        document.getElementById("total").innerText=d.length

        let html=""
        d.forEach(k=>{
            html+=`
            <div class="key-row">
                <span>${k}</span>
                <div>
                    <button class="small on">ON</button>
                    <button class="small off">OFF</button>
                    <button class="small delete" onclick="del('${k}')">Delete</button>
                </div>
            </div>`
        })

        document.getElementById("list").innerHTML=html
    })
}

function addKey(){
    let k=document.getElementById("key").value
    fetch("/add_key",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({key:k})})
    .then(()=>{load();closeAll()})
}

function del(k){
    fetch("/delete_key",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({key:k})})
    .then(()=>load())
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
