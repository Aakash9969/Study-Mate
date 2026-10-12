
import os

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma2:latest")
OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://127.0.0.1:11434"
)
OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "120"))
