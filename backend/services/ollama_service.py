import json
import urllib.error
import urllib.request
from backend.config import OLLAMA_BASE_URL, OLLAMA_MODEL, OLLAMA_TIMEOUT

class OllamaUnavailable(RuntimeError):
    pass

def generate_answer(prompt: str, system: str = "", temperature: float = 0.4) -> str:
    """Call Ollama's local /api/generate endpoint without any cloud API key."""
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "system": system,
        "stream": False,
        "options": {"temperature": temperature}
    }
    req = urllib.request.Request(
        f"{OLLAMA_BASE_URL.rstrip('/')}/api/generate",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=OLLAMA_TIMEOUT) as response:
            result = json.loads(response.read().decode("utf-8"))
        text = str(result.get("response", "")).strip()
        if not text:
            raise OllamaUnavailable("Ollama returned an empty response. Try asking again.")
        return text
    except urllib.error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")[:500]
        if exc.code == 404:
            raise OllamaUnavailable(
                f"Model '{OLLAMA_MODEL}' was not found by Ollama. Run `ollama list` and set OLLAMA_MODEL in backend/config.py to the exact model tag."
            ) from exc
        raise OllamaUnavailable(f"Ollama returned HTTP {exc.code}: {details}") from exc
    except (urllib.error.URLError, TimeoutError, ConnectionError) as exc:
        raise OllamaUnavailable(
            "Cannot connect to Ollama at " + OLLAMA_BASE_URL +
            ". Start Ollama, then try again. If needed, run `ollama serve` in a terminal."
        ) from exc
