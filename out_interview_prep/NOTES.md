# Interview prep notes

## Gemini APIs (Google)

| API | What it does | We use it? |
|-----|--------------|------------|
| **Interactions** | Chat / extract text / JSON (new, recommended) | **YES** |
| generateContent | Same idea, older style | No |
| Embeddings | Turn text into vectors for search | No |
| Batch API | Many requests overnight, cheaper | No |
| Files API | Upload big PDFs | No |
| Live API | Real-time audio/video | No |

**Our case:** `client.interactions.create()` + `response_mime_type="application/json"`

```python
result = client.interactions.create(
    model="gemini-3.6-flash",
    input=prompt,
    response_mime_type="application/json",
)
text = result.output_text
```

OpenAI equivalent: **Chat Completions**

---

## Claude APIs (Anthropic)

| API | What it does | We use it? |
|-----|--------------|------------|
| **Messages** | Chat / extract text (main one) | **YES** |
| Structured Outputs | Force JSON with schema (`output_config`) | Optional — nicer JSON, not required |
| Message Batches | Many requests overnight | No |
| Files API | Upload big PDFs | No |
| Managed Agents / Sessions | Long agent workflows | No |

**Our case:** `client.messages.create()` + parse JSON from response

```python
message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=4096,
    messages=[{"role": "user", "content": prompt}],
)
text = message.content[0].text
```

OpenAI equivalent: **Chat Completions**

**Better for JSON (not in our code yet):**
```python
client.messages.parse(..., output_format=list[Requirement])
```

---

## Our pipeline (both providers)

```
read file → send text to LLM → json.loads → Requirement(**item) → compare expected
```

- Gemini: Interactions API
- Claude: Messages API
- Validate: Pydantic (our code, not the API)

---

## Testing (remember)

1. **Unit test** — Pydantic, JSON parsing (no API)
2. **Mock** — fake LLM response in pytest (no API)
3. **Manual** — run `scripts/read_one.py` with real key (real API)

Don't pytest the real AI every time — answers change.

---

## Libraries we use

| Library | What it actually does |
|---------|------------------------|
| **fastapi** | Builds the web API. You hit URLs like `/health`, upload a PDF, get JSON back. |
| **uvicorn** | The server that runs FastAPI. Without it, the API doesn't start. |
| **pydantic** | Defines rules for your data. Example: every requirement must have `id`, `section`, `text`. Wrong shape = error. |
| **pytest** | Runs your tests automatically. |
| **python-dotenv** | Reads secrets from `.env` file (API keys) so you don't hardcode them in code. |
| **google-genai** | Official Python package to talk to Gemini (Google's AI). |
| **anthropic** | Official Python package to talk to Claude (Anthropic's AI). |
| **pdfplumber** | Opens a normal PDF and pulls out the text that's already inside it. Our first choice. |
| **pymupdf** | Does the same job as pdfplumber — opens PDF, gets text. Second option if pdfplumber fails or returns empty. |
| **pytesseract** | OCR. Looks at a picture or scan and guesses the words (no text layer in the file). Needs `tesseract` installed on the machine. |
| **pdf2image** | Converts each PDF page into an image so pytesseract can read scanned PDFs. |
| **pillow (PIL)** | Opens and creates image files (PNG, JPG). Used for OCR and our fake scan sample. |
| **tenacity** | If a download fails, try again a few times before giving up. |
| **httpx** | Sends HTTP requests — used to download sample PDFs from the internet. |
| **python-multipart** | Lets FastAPI accept file uploads in POST requests. |
| **uv** | Python package manager. `uv sync` installs everything from `pyproject.toml`. |
| **Docker** | Packages the app + system tools (tesseract, poppler) into one runnable box. |
| **docker-compose** | Starts Docker with the right ports, volumes, and `.env` in one command. |

**PDF text vs OCR — remember:**
- **pdfplumber / pymupdf** = PDF already has text inside → just read it
- **pytesseract + pdf2image** = PDF is a scan/photo → no text inside → OCR reads pixels


---

## Approaches (how we built it)

**1. Manifest file (`manifest.jsonl`)**  
One JSON object per line = list of docs to process.  
Read first line → get file path → open that file.

**2. Extract text locally first**  
- `.txt` → read file  
- PDF with real text inside → `pdfplumber` first, `pymupdf` if needed  
- Scanned PDF/image → OCR (`pytesseract`)  
Then send **text string** to LLM. Don't rely on LLM to read files unless needed.

**3. LLM extraction**  
Prompt: "extract requirements, return JSON list"  
Parse: `json.loads()` → `Requirement(**item)` for each dict.

**4. Golden expected data**  
`data/expected/requirements.json` = what correct output looks like.  
Compare counts / fields after extraction.

**5. Two practice folders**  
- `out_data_prac` — Gemini script only (`read_one.py`)  
- `out_interview_prep` — full stack: FastAPI, PDF, OCR, Claude + Gemini, pytest, Docker

**6. Docker**  
`Dockerfile` = recipe to build image  
`docker-compose.yml` = run services (api on port 8000, mount `data/`, load `.env`)

**7. Env keys**  
- `GEMINI_API_KEY` or `GEMINI_API_KEY_NEW`  
- `ANTHROPIC_API_KEY`  
Never commit `.env` to git.

---

## Quick commands

```bash
cd out_interview_prep
uv sync
uv run pytest
uv run python scripts/read_one.py --provider claude
uv run python scripts/read_one.py --provider gemini
uv run uvicorn app.main:app --reload
docker compose up --build
```

