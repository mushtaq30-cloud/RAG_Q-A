const askBtn = document.getElementById('ask');
const answerEl = document.getElementById('answer');
const sourcesEl = document.getElementById('sources');

askBtn.onclick = async () => {
  const q = document.getElementById('q').value;
  answerEl.textContent = "Thinking…";
  sourcesEl.innerHTML = "";
  askBtn.disabled = true;

  try {
    const resp = await fetch(`http://localhost:8001/qa?q=${encodeURIComponent(q)}`);

    // Read raw text so we can surface non-JSON errors too
    const raw = await resp.text();

    // Show HTTP status if something went wrong
    if (!resp.ok) {
      answerEl.textContent = `HTTP ${resp.status} ${resp.statusText}\n\n${raw}`;
      console.error('Request failed', resp.status, resp.statusText, raw);
      askBtn.disabled = false;
      return;
    }

    // Try parsing JSON; if it fails, show raw text
    let j;
    try {
      j = JSON.parse(raw);
    } catch (err) {
      answerEl.textContent = raw;
      console.warn('Response was not JSON:', raw);
      askBtn.disabled = false;
      return;
    }

    answerEl.textContent = j.answer || JSON.stringify(j, null, 2);

    (j.sources || []).forEach((s, i) => {
      const d = document.createElement('div');
      d.className = 'source';
      d.innerHTML = `<strong>[${i}]</strong> ${s.text || JSON.stringify(s)}`;
      sourcesEl.appendChild(d);
    });

  } catch (e) {
    // network-level error (server down, CORS, DNS, etc.)
    answerEl.textContent = 'Fetch/network error: ' + e.toString();
    console.error(e);
  } finally {
    askBtn.disabled = false;
  }
};