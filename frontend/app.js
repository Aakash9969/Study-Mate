const state = { mode: "faq", history: [], busy: false };
const $ = (id) => document.getElementById(id);
const welcome = $("welcome"), chat = $("chat"), form = $("chat-form"), input = $("message"), send = $("send");
const modeTitles = {
  faq: "Intelligent FAQ Assistant",
  zero: "Zero-shot Prompting",
  few: "Few-shot Prompting",
  role: "Role Prompting"
};
const modeDescriptions = {
  faq: "Student FAQ assistant",
  zero: "Direct question, no examples",
  few: "Prompt guided by examples",
  role: "Friendly computer science tutor"
};

function selectMode(mode) {
  state.mode = mode;
  document.querySelectorAll(".mode").forEach(btn => btn.classList.toggle("active", btn.dataset.mode === mode));
  $("mode-title").textContent = modeTitles[mode] || modeTitles.faq;
}
document.querySelectorAll(".mode").forEach(btn => btn.addEventListener("click", () => selectMode(btn.dataset.mode)));
$("new-chat").addEventListener("click", () => {
  state.history = [];
  chat.innerHTML = "";
  chat.classList.add("hidden");
  welcome.classList.remove("hidden");
  input.value = "";
  input.focus();
});
document.querySelectorAll(".suggestion").forEach(btn => btn.addEventListener("click", () => {
  input.value = btn.dataset.question;
  input.focus();
  autoResize();
}));
input.addEventListener("input", autoResize);
input.addEventListener("keydown", e => {
  if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); form.requestSubmit(); }
});
function autoResize() { input.style.height = "auto"; input.style.height = Math.min(input.scrollHeight, 150) + "px"; }

function addMessage(role, content, meta = "") {
  const wrapper = document.createElement("article");
  wrapper.className = `message ${role}`;
  const avatar = document.createElement("div");
  avatar.className = "avatar";
  avatar.textContent = role === "user" ? "Y" : "✦";
  const body = document.createElement("div");
  body.className = "message-body";
  const label = document.createElement("div");
  label.className = "message-label";
  label.textContent = role === "user" ? "YOU" : "STUDYMATE";
  const text = document.createElement("div");
  text.className = "message-content";
  text.textContent = content;
  body.append(label, text);
  if (meta) {
    const metadata = document.createElement("div");
    metadata.className = "answer-meta";
    metadata.textContent = meta;
    body.append(metadata);
  }
  wrapper.append(avatar, body);
  chat.append(wrapper);
  chat.scrollTop = chat.scrollHeight;
  return { wrapper, text };
}

async function checkHealth() {
  const status = $("connection-status");
  status.textContent = "Checking local Ollama…";
  try {
    const res = await fetch("/api/health");
    const data = await res.json();
    $("model-name").textContent = `${data.model || "Gemma 4B"} · Ollama`;
    status.textContent = data.ok ? `Connected · ${data.model}` : data.message;
    status.style.color = data.ok ? "var(--green)" : "#ffaaa9";
  } catch {
    status.textContent = "Backend not reachable. Start the app with python app.py.";
    status.style.color = "#ffaaa9";
  }
}
$("check-connection").addEventListener("click", checkHealth);

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const message = input.value.trim();
  if (!message || state.busy) return;
  state.busy = true;
  send.disabled = true;
  welcome.classList.add("hidden");
  chat.classList.remove("hidden");
  addMessage("user", message);
  const waiting = addMessage("assistant", "Thinking…", modeDescriptions[state.mode]);
  waiting.text.classList.add("typing");
  input.value = "";
  autoResize();
  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ message, mode: state.mode, history: state.history })
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "The request failed.");
    waiting.text.classList.remove("typing");
    waiting.text.textContent = data.answer;
    const meta = document.createElement("div");
    meta.className = "answer-meta";
    meta.textContent = `${modeTitles[data.mode] || "Study Assistant"} · ${data.model || "Local model"}` +
      (data.matched_faq ? " · FAQ reference used" : "");
    waiting.wrapper.querySelector(".message-body").append(meta);
    state.history.push({role: "user", content: message}, {role: "assistant", content: data.answer});
    state.history = state.history.slice(-12);
  } catch (err) {
    waiting.text.classList.remove("typing");
    waiting.text.classList.add("error");
    waiting.text.textContent = `Could not get an answer: ${err.message}`;
  } finally {
    state.busy = false;
    send.disabled = false;
    input.focus();
    chat.scrollTop = chat.scrollHeight;
  }
});

checkHealth();
