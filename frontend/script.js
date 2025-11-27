// script.js
const analyzeBtn = document.getElementById('analyzeBtn');
const resultsDiv = document.getElementById('results');
const taskForm = document.getElementById('taskForm');
const bulkInput = document.getElementById('bulkInput');

let tasks = [];

taskForm.addEventListener('submit', (e) => {
  e.preventDefault();
  const title = document.getElementById('title').value.trim();
  const due_date = document.getElementById('due_date').value || null;
  const estimated_hours = parseFloat(document.getElementById('estimated_hours').value || 1);
  const importance = parseInt(document.getElementById('importance').value || 1);
  const dependencies = document.getElementById('dependencies').value
    .split(',')
    .map(s => s.trim())
    .filter(s => s.length > 0)
    .map(Number);

  const newTask = { title, due_date, estimated_hours, importance, dependencies };
  tasks.push(newTask);
  renderTasksPreview();
  taskForm.reset();
});

function renderTasksPreview() {
  resultsDiv.innerHTML = '<h3>Preview (not analyzed yet)</h3>';
  tasks.forEach((t,i) => {
    const el = document.createElement('div');
    el.className = 'task';
    el.innerHTML = `<strong>${i+1}. ${t.title}</strong><div>Due: ${t.due_date || '—'}</div><div>Hours: ${t.estimated_hours} | Importance: ${t.importance}</div>`;
    resultsDiv.appendChild(el);
  });
}

analyzeBtn.addEventListener('click', async () => {
  let payloadTasks = [];

  if (bulkInput.value.trim()) {
    try {
      payloadTasks = JSON.parse(bulkInput.value);
    } catch (err) {
      alert('Invalid JSON in bulk input');
      return;
    }
  } else {
    payloadTasks = tasks;
  }

  if (!Array.isArray(payloadTasks) || payloadTasks.length === 0) {
    alert('Add tasks or paste a JSON array first.');
    return;
  }

  const mode = document.getElementById('mode').value;

  // call backend
  try {
    const resp = await fetch('http://127.0.0.1:8000/api/tasks/analyze/', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ tasks: payloadTasks, mode })
    });
    const data = await resp.json();
    displayResults(data.tasks || []);
  } catch (err) {
    alert('Error contacting API. Is the backend server running?');
    console.error(err);
  }
});

function displayResults(sortedTasks) {
  resultsDiv.innerHTML = "";

  sortedTasks.forEach((t, idx) => {
    const div = document.createElement("div");
    div.className = "task-card " + priorityClass(t.score);

    div.innerHTML = `
      <h3>${idx + 1}. ${escapeHtml(t.title)}</h3>
      <div class="score">Score: <strong>${t.score}</strong></div>
      <div class="score">Due: ${t.due_date || "—"} | Hours: ${t.estimated_hours} | Importance: ${t.importance}</div>
      <p class="explanation">${escapeHtml(t.explanation)}</p>
    `;

    resultsDiv.appendChild(div);
  });
}


function priorityClass(score){
  if (score >= 15) return 'high';
  if (score >= 8) return 'medium';
  return 'low';
}

function escapeHtml(text){
  if (!text) return '';
  return text.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;');
}
