from flask import Flask, request, jsonify, send_from_directory
from pathlib import Path
from backend.services.ollama_service import generate_answer, OllamaUnavailable
from backend.prompts import build_prompt, MODES
from backend.faq import FAQS, find_faq

ROOT = Path(__file__).resolve().parent
app = Flask(__name__, static_folder="frontend", static_url_path="")

@app.get("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.get("/api/health")
def health():
    from backend.config import OLLAMA_MODEL, OLLAMA_BASE_URL
    try:
        answer = generate_answer("Reply with exactly: OK", system="You are a connection test. Reply briefly.", temperature=0)
        return jsonify({"ok": True, "model": OLLAMA_MODEL, "ollama_url": OLLAMA_BASE_URL, "message": "Ollama is responding."})
    except OllamaUnavailable as exc:
        return jsonify({"ok": False, "model": OLLAMA_MODEL, "message": str(exc)}), 503

@app.get("/api/modes")
def modes():
    return jsonify({"modes": MODES})

@app.get("/api/faqs")
def faqs():
    return jsonify({"faqs": FAQS})

@app.post("/api/chat")
def chat():
    data = request.get_json(silent=True) or {}
    question = str(data.get("message", "")).strip()
    mode = str(data.get("mode", "faq")).strip().lower()
    history = data.get("history", [])

    if not question:
        return jsonify({"error": "Please enter a question."}), 400
    if len(question) > 4000:
        return jsonify({"error": "Please keep your question under 4,000 characters."}), 400
    if mode not in MODES:
        return jsonify({"error": "Unknown prompting mode."}), 400
    if not isinstance(history, list):
        history = []
    # Keep only a small, sanitized conversation window.
    safe_history = []
    for item in history[-6:]:
        if isinstance(item, dict):
            role = item.get("role")
            content = item.get("content")
            if role in ("user", "assistant") and isinstance(content, str):
                safe_history.append({"role": role, "content": content[:1500]})

    faq_match = find_faq(question) if mode == "faq" else None
    prompt, system = build_prompt(question, mode, history=safe_history, faq_match=faq_match)
    try:
        answer = generate_answer(prompt, system=system)
        return jsonify({
            "answer": answer,
            "mode": mode,
            "matched_faq": faq_match,
            "model": __import__("backend.config", fromlist=["OLLAMA_MODEL"]).OLLAMA_MODEL
        })
    except OllamaUnavailable as exc:
        return jsonify({"error": str(exc)}), 503
    except Exception:
        app.logger.exception("Unexpected generation error")
        return jsonify({"error": "Something went wrong while generating the answer. Check the backend terminal for details."}), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
