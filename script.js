/* ================= Navigation ================= */
function show(id){
  document.querySelectorAll('.section').forEach(s=>s.classList.remove('active'));
  document.getElementById(id).classList.add('active');
}

/* ================= Chart Setup ================= */
const ctx = document.getElementById('chart');

let chart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: [],
    datasets: [{
      label: 'Device Activity',
      data: []
    }]
  }
});

/* ================= Fake Live Data ================= */

const deviceTable = document.getElementById("deviceTable");
const alertTable = document.getElementById("alertTable");

let alerts = 0;

function randomHash(){
  return Math.random().toString(16).substring(2,10);
}

function addDeviceRows(){
  deviceTable.innerHTML = `
    <tr>
      <th>ID</th>
      <th>Status</th>
      <th>Hash</th>
    </tr>
  `;

  for(let i=1;i<=5;i++){
    let tamper = Math.random() < 0.2;

    let row = `
      <tr>
        <td>Device-${i}</td>
        <td class="${tamper?'alert blink':'secure'}">
          ${tamper?'Tampered':'Verified'}
        </td>
        <td>${randomHash()}</td>
      </tr>
    `;

    deviceTable.innerHTML += row;

    if(tamper){
      addAlert(`Device-${i} HASH MISMATCH`);
    }
  }
}

function addAlert(msg){
  alerts++;

  let time = new Date().toLocaleTimeString();

  alertTable.innerHTML += `
    <tr class="blink">
      <td>${time}</td>
      <td class="alert">${msg}</td>
    </tr>
  `;

  document.getElementById("alertCount").innerText = alerts;
  document.getElementById("systemStatus").innerText = "Alert";
  document.getElementById("systemStatus").className = "alert blink";
}

/* ================= Auto Update Every 2s ================= */

let counter = 0;

setInterval(()=>{
  counter++;

  document.getElementById("blockCount").innerText = 500 + counter;

  chart.data.labels.push(counter);
  chart.data.datasets[0].data.push(Math.floor(Math.random()*20)+5);

  if(chart.data.labels.length > 10){
    chart.data.labels.shift();
    chart.data.datasets[0].data.shift();
  }

  chart.update();

  addDeviceRows();

}, 2000);

addDeviceRows();
