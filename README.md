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
2. Go to [share.streamlit.io](https://share.streamlit.io) → your app → **Manage app**
3. Repo `sheldor33/LabGenie`, branch `main`, file `app.py`
4. **Advanced settings → Python version**: select **3.12** (recommended).  
   Community Cloud ignores `runtime.txt`; the UI setting is what matters.  
   If you stay on 3.14, this repo’s `requirements.txt` uses Streamlit ≥1.52 so Pillow installs with a wheel.
5. Under **Advanced settings → Secrets**, add:
   ```toml
   OPENAI_API_KEY = "sk-..."
   ```
6. Redeploy / reboot the app

### Privacy note
Do not upload real patient reports with identifiable information to public demos.
