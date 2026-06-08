// ================= CONFIG =================

// 🔊 SOUND INIT (باش يخدم فـ Chrome)
document.body.addEventListener("click", ()=>{
let sound = document.getElementById("notifSound");
if(sound) sound.play().catch(()=>{});
},{once:true});

// ================= TOAST =================

let shownAlerts = new Set();

function playSound(){
let sound = document.getElementById("notifSound");
if(sound){
sound.currentTime = 0;
sound.play().catch(()=>{});
}
}

function showToast(message, type="warning"){

let container = document.getElementById("toast-container");

let toast = document.createElement("div");
toast.className = "toast " + type;
toast.innerText = message;

container.appendChild(toast);

// 🔊 SOUND
playSound();

// auto remove
setTimeout(()=>{
toast.remove();
},5000);
}

// ================= STATS =================

function loadStats(){
fetch("/stats")
.then(res=>res.json())
.then(data=>{

document.getElementById("prod").innerText = data.production;
document.getElementById("dep").innerText = data.depense;
document.getElementById("profit").innerText = data.profit;

});
}

// ================= ALERT 21 =================

function loadAlert21(){

fetch("/alerts_21")
.then(res=>res.json())
.then(data=>{

let html = "";

if(data.length === 0){
html = "<tr><td colspan='2'>Aucune alerte</td></tr>";
}

data.forEach(v=>{

let key = "21_" + v.id;

html += `
<tr>
<td>${v.nom}</td>
<td>
<button onclick="confirmDiag(${v.id})">✔ OK</button>
</td>
</tr>
`;

if(!shownAlerts.has(key)){
showToast("🔔 " + v.nom + " : Vérifier grossesse","warning");
shownAlerts.add(key);
}

});

document.getElementById("alert21").innerHTML = html;

});
}

// ================= ALERT VELAGE =================

function loadVelage(){

fetch("/alerts_velage")
.then(res=>res.json())
.then(data=>{

let html = "";

if(data.length === 0){
html = "<tr><td colspan='3'>Aucune alerte</td></tr>";
}

data.forEach(v=>{

let key = "velage_" + v.id;

html += `
<tr>
<td>${v.nom}</td>
<td>${v.jours}</td>
<td>
<button onclick="confirmVelage(${v.id})">✔ Née</button>
</td>
</tr>
`;

if(!shownAlerts.has(key)){
showToast("🐄 " + v.nom + " : Mise bas proche ("+v.jours+"j)","danger");
shownAlerts.add(key);
}

});

document.getElementById("velage").innerHTML = html;

});
}

// ================= ACTIONS =================

function confirmDiag(id){
fetch("/confirm_diagnostic/" + id)
.then(()=>{
loadAlert21();
});
}

function confirmVelage(id){
fetch("/confirm_velage/" + id)
.then(()=>{
loadVelage();
});
}

// ================= CHART =================

let chartInstance = null;

function loadChart(){

let prod = parseFloat(document.getElementById("prod").innerText) || 0;
let dep = parseFloat(document.getElementById("dep").innerText) || 0;
let profit = parseFloat(document.getElementById("profit").innerText) || 0;

let ctx = document.getElementById("chart");

if(chartInstance){
chartInstance.destroy();
}

chartInstance = new Chart(ctx,{
type:"bar",
data:{
labels:["Production","Dépenses","Profit"],
datasets:[{
data:[prod,dep,profit]
}]
}
});
}

// ================= AUTO REFRESH =================

function autoRefresh(){

setInterval(()=>{
loadStats();
loadAlert21();
loadVelage();

setTimeout(loadChart,300);

},30000); // كل 30 ثانية

}

// ================= INIT =================

window.onload = ()=>{

loadStats();

// chart بعد تحميل stats
setTimeout(loadChart,500);

loadAlert21();
loadVelage();

autoRefresh();

};