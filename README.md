# StudyMate — Study Assistant Agent & Intelligent FAQ Assistant

A local AI study assistant demonstrating **zero-shot prompting, few-shot prompting, role prompting, and an Intelligent FAQ Assistant** using Ollama + Gemma. No OpenAI key or cloud LLM is required.

## Project structure

```text
study_assistant_agent/
├── app.py
├── requirements.txt
├── README.md
├── .env.example
├── backend/
│   ├── config.py
│   ├── prompts.py
│   ├── faq.py
│   └── services/ollama_service.py
└── frontend/
    ├── index.html
    ├── styles.css
    └── app.js
```

## Requirements
- Python 3.10+
- Ollama installed and running
- Your Gemma model downloaded in Ollama

## Windows setup

1. Open PowerShell in this folder.
2. Run `ollama list` and check the exact model tag.
3. If the tag is not `gemma4b`, edit `OLLAMA_MODEL` in `backend/config.py` to match it exactly.
4. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

5. Make sure Ollama is running. If needed, open another terminal and run `ollama serve`.
6. Start the backend and frontend server:

```powershell
python app.py
```

7. Visit http://127.0.0.1:5000 in your browser.

## Assignment demo

- **Zero-shot:** Ask `What is artificial intelligence?`
- **Few-shot:** Ask `What is ROM?` The prompt includes CPU and RAM examples to demonstrate format guidance.
- **Role prompting:** Ask `Teach me Python loops as a beginner.` The model is instructed to respond as a patient computer science tutor.
- **Intelligent FAQ:** Ask `How can I prepare for semester exams?` The backend looks for a relevant FAQ entry and includes it as context.

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/health` | Check Ollama connection |
| GET | `/api/modes` | List prompting modes |
| GET | `/api/faqs` | Return FAQ knowledge base |
| POST | `/api/chat` | Generate an answer |

Example JSON request to `/api/chat`:

```json
{"message":"Explain a Python function","mode":"role","history":[]}
```

## Troubleshooting

- **Cannot connect to Ollama:** Open Ollama or run `ollama serve` in a second terminal.
- **Model not found:** Run `ollama list`, then set `OLLAMA_MODEL` to the exact tag shown.
- **Python command not found:** Install Python and enable adding it to PATH, then reopen the terminal.
- **Slow answers:** Generation speed depends on your hardware and local model variant.

## Limitations

The FAQ retrieval is a small keyword-based demo, not a full semantic search system or college database connection. It cannot know your institution's actual attendance rules or deadlines unless you add trusted source data. Verify important college-specific information. Flask debug mode is intended for local development only; do not expose this server publicly.
