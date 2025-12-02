document.getElementById('ask').onclick = async () => {
  const q = document.getElementById('q').value;
  document.getElementById('answer').textContent = "Thinking…";
  document.getElementById('sources').innerHTML = "";
  try {
    const res = await fetch(`http://localhost:8001/qa?q=${encodeURIComponent(q)}`);
    const j = await res.json();
    document.getElementById('answer').textContent = j.answer || JSON.stringify(j, null, 2);
    (j.sources || []).forEach((s, i) => {
      const d = document.createElement('div');
      d.className = 'source';
      d.innerHTML = `<strong>[${i}]</strong> ${s.text || JSON.stringify(s)}`;
      document.getElementById('sources').appendChild(d);
    });
  } catch (e) {
    document.getElementById('answer').textContent = 'Error: ' + e;
  }
};