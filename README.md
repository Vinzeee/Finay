# Finay — Professional News Research & Analysis Tool

Finay is a lightweight Streamlit app that lets you paste a few news/article URLs, build a local semantic index with FAISS embeddings, and ask targeted questions to extract key insights with source citations. It is designed for quick financial/business news triage with a clean, minimalist UI.

---

## Demo

<p align="center">
  <img src="Finay/screenshots/Finay.png" alt="Finay main screen" width="75%">
</p>

<p align="center">
  <img src="Finay/screenshots/finay2.png" alt="Articles processed example" width="45%">
  <img src="Finay/screenshots/finay3.png" alt="Q&A with sources example" width="45%">
</p>

> Screenshots live under `finay/screenshots/` in this repo. Adjust the relative paths above if you move folders.

---

## Features

- Process 1–3 article URLs at a time using LangChain’s `UnstructuredURLLoader`
- Split content into chunks with `RecursiveCharacterTextSplitter`
- Embed with `OpenAIEmbeddings` and store locally in FAISS (`.pkl` file)
- Ask questions over the processed set via `RetrievalQAWithSourcesChain`
- Persist the vector store on disk so you don’t need to re-process every run
- Simple, Notion‑inspired UI built with Streamlit

---

## Tech Stack

- Python 3.10+
- Streamlit
- LangChain
- OpenAI API (for embeddings and LLM)
- FAISS (CPU)

See `finay/requirements.txt` for exact package list.

---

## Project Structure

```
finay/
├── finay/
│   ├── main.py               # Streamlit application
│   ├── requirements.txt      # Python dependencies
│   ├── setup_finay.py        # Optional one‑time setup helper
│   ├── .gitignore            # Ignoring env, cache, large artifacts
│   ├── .env                  # Your API key goes here (not committed)
│   ├── faiss_store.pkl       # Vector store (generated)
│   ├── notebooks/.gitkeep    # Placeholder for experiments
│   └── screenshots/          # PNG screenshots used in this README
│       ├── Finay.png
│       ├── finay2.png
│       └── finay3.png
└── README.md                 # This file (you can keep at repo root)
```

> Note: The app expects to read/write the FAISS store (e.g., `faiss_store.pkl`) in the same folder as `main.py` unless you modify the path in code.

---

## Prerequisites

1. **Python** 3.10 or newer
2. **OpenAI API key**
   - Create a `.env` file next to `main.py` with:
     ```bash
     OPENAI_API_KEY=your_api_key_here
     ```
   - The `.gitignore` already excludes `.env` so you won’t accidentally commit your key.

---

## Setup & Run Locally

From the repo root:

```bash
# 1) Create and activate a virtual environment (recommended)
python -m venv .venv
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate

# 2) Install dependencies
pip install -r finay/finay/requirements.txt

# 3) Add your API key to finay/finay/.env
#    OPENAI_API_KEY=...

# 4) Launch the app
streamlit run finay/finay/main.py
```

Then open the local URL that Streamlit prints (usually `http://localhost:8501`).

---

## How to Use

1. Paste up to 3 article/news URLs.
2. Click **Process Articles** — this loads, splits, and embeds the content and saves a FAISS store to disk.
3. Ask a question in the **Ask a Question** box (e.g., “What are the key takeaways and risks?”).
4. Read the **Answer** and verify with the **Sources** list.

To refresh the knowledge base, change the URLs and re‑process.

---

## Configuration Notes

- **Environment variables**: Only `OPENAI_API_KEY` is required.
- **Vector store location**: By default, a `faiss_store.pkl` is written in the app folder. You can safely delete it to force a full rebuild.
- **Library versions**: `openai==0.28.0` is pinned in `requirements.txt` to match the LangChain usage in this app.

---

## Troubleshooting

- **“Missing required library” in app**: Install packages from `requirements.txt` inside the same virtual environment you are using to run Streamlit.
- **“OpenAI API Key not found”**: Ensure you created `.env` next to `main.py` and that it contains `OPENAI_API_KEY=...`. Restart Streamlit after saving.
- **Dependency conflicts**: If you previously installed different versions globally, prefer a fresh virtualenv as shown above.
- **Windows PowerShell execution policy**: If activation fails, run PowerShell as Administrator and execute:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

---

## Publish to GitHub (Step‑by‑Step)

Below are clean steps for **Windows PowerShell**. Replace `YOUR-USERNAME` and `finay` with your values.

1. **Create a new empty repository on GitHub** named `finay` (no README, no .gitignore — we already have them).
2. In PowerShell, go to the repo root (the folder that contains `finay/` and this `README.md`):
   ```powershell
   cd path\to\your\project\root
   git init
   git add .
   git commit -m "Initial commit: Finay app"
   ```
3. **Set the main branch and remote**:
   ```powershell
   git branch -M main
   git remote add origin https://github.com/YOUR-USERNAME/finay.git
   ```
4. **Push**:
   ```powershell
   git push -u origin main
   ```

Notes:
- Your `.env` and generated `.pkl` files are already ignored via `.gitignore`.
- If you see an auth prompt, log in with your GitHub credentials or use a **Personal Access Token** when prompted for a password.



## License

MIT — see `LICENSE` if you add one.

---

## Acknowledgments

- LangChain
- FAISS
- Streamlit
