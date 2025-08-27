
const $ = (q, el=document) => el.querySelector(q);
const $$ = (q, el=document) => Array.from(el.querySelectorAll(q));

// Simple i18n
let LANG = 'en';
const I18N = {};
async function loadI18n(lang='en'){
  LANG = lang;
  try {
    const res = await fetch(`/assets/i18n/${lang}.json`);
    const data = await res.json();
    Object.assign(I18N, data);
  } catch(e){}
  applyI18n();
}
function t(key, fallback=""){ return I18N[key] || fallback || key; }
function applyI18n(){
  $$('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    el.textContent = t(key, el.textContent);
  });
  $('#symptoms').placeholder = t('placeholder.symptoms', 'Describe your symptoms...');
  $('#chat-input').placeholder = t('placeholder.chat', 'Ask health questions...');
}

// Diagnosis submit
async function submitDiagnosis(e){
  e.preventDefault();
  const symptoms = $('#symptoms').value.trim();
  if(!symptoms) return;
  const res = await fetch('/api/diagnose', {
    method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({symptoms})
  });
  const data = await res.json();
  renderDiagnosis(data);
}

function amazonLink(q){ 
  const url = `https://www.amazon.com/s?k=${encodeURIComponent(q)}`;
  return url;
}

function renderDiagnosis(data){
  const out = $('#diagnosis-results');
  if(!data || !data.top){ out.innerHTML = '<p>Unable to diagnose.</p>'; return; }
  



const mkMed = (m) => `
    <div class="med-item">
      <div class="med-left"><strong class="med-name">${m.name}</strong> — <span class="dose">${m.dosage || ''}</span></div>
      <div class="actions">
        ${m.info_url ? `<button class="btn info-btn" onclick="window.open('${m.info_url}','_blank')">Info</button>` : ''}
        <button class="btn amz-btn" onclick="window.open('${amazonLink(m.name)}','_blank')">Amazon</button>
      </div>
    </div>
  `;
  const mkPoss = (p) => `
    <div class="poss">
      <div class="pill">${Math.round(p.confidence*100)}%</div>
      <div class="pill">${p.triage}</div>
      <div><strong>${p.name}</strong></div>
      <div class="meds">${(p.medications||[]).map(mkMed).join('')}</div>
    </div>
  `;
  out.innerHTML = `
    <h3>${t('label.most_likely','Most likely')}</h3>
    ${mkPoss(data.top)}
    ${data.others && data.others.length ? `<h3>${t('label.other_poss','Other possibilities')}</h3>${data.others.map(mkPoss).join('')}` : ''}
    <p><small class="disclaimer">${data.advice || ''} ${t('disclaimer','This tool is for reference only and not a medical diagnosis. Seek licensed care when available.')}</small></p>
  `;
}

// Chat (WebSocket with HTTP fallback)
let ws;
function connectWS(){
  try {
    const proto = location.protocol === 'https:' ? 'wss' : 'ws';
    ws = new WebSocket(`${proto}://${location.host}/ws/chat`);
    ws.onmessage = (ev)=> addMsg('assistant', ev.data);
    ws.onopen = ()=> addMsg('assistant', t('chat.ready','Chat connected. How can I help?'));
    ws.onclose = ()=> { ws = null; addMsg('assistant', t('chat.fallback','Connection lost. I will reply over HTTP.')); }
  } catch(e) { ws = null; }
}

function addMsg(who, text){
  const stream = $('#chat-stream');
  const el = document.createElement('div');
  el.className = `msg ${who}`;
  el.innerHTML = `<div class="who">${who}</div><div class="bubble">${text}</div>`;
  stream.appendChild(el);
  stream.scrollTop = stream.scrollHeight;
}

async function sendChat(e){
  e.preventDefault();
  const txt = $('#chat-input').value.trim();
  if(!txt) return;
  addMsg('user', txt);
  $('#chat-input').value = '';
  if(ws && ws.readyState === WebSocket.OPEN){
    ws.send(txt);
  } else {
    const res = await fetch('/api/chat', {
      method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({message: txt})
    });
    const data = await res.json();
    addMsg('assistant', data.reply || '...');
  }
}

// Language switch
$('#lang-select').addEventListener('change', (e)=> loadI18n(e.target.value));

// Hook up events
$('#diagnosis-form').addEventListener('submit', submitDiagnosis);
$('#chat-form').addEventListener('submit', sendChat);

// Init
loadI18n('en');
connectWS();
applyI18n();
