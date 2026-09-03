## LabGenie — Medical Lab Report Decoder

Streamlit + LangChain app that turns lab-report PDFs into plain-language definitions and an interactive health Q&A chat.

### Features
- Upload a PDF lab report
- Extract health-related keywords
- Generate short definitions, healthy ranges, and balance tips via OpenAI
- Chat follow-ups about the report

### Local run
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
pip install -r requirements.txt
```

Create `.streamlit/secrets.toml` (or a `.env` file):
```toml
OPENAI_API_KEY = "sk-..."
```

```bash
streamlit run app.py
```

### Streamlit Community Cloud
1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**
3. Select repo `sheldor33/LabGenie`, branch `main`, file `app.py`
4. Python is pinned to **3.12** via `runtime.txt` (required for reliable installs)
5. Under **Advanced settings → Secrets**, add:
   ```toml
   OPENAI_API_KEY = "sk-..."
   ```
6. Deploy

### Privacy note
Do not upload real patient reports with identifiable information to public demos. Use anonymized sample PDFs for interviews.
