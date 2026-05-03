# 🚀 CareerCopilot AI — Resume Builder & Job Matcher

> **An AI-powered career suite** that generates resumes, scores them against ATS systems, matches jobs via FAISS embeddings, improves bullet points, and provides personalised career roadmaps — all inside a beautiful Streamlit dashboard.

---

## ✨ Features

| Feature | Description |
|---|---|
| **Resume Generator** | LLM-generated summary, skills, experience, and projects tailored to a target role |
| **ATS Scorer** | Keyword-match scoring (0–100), missing-skills detection, section analysis |
| **Job Matcher** | FAISS vector similarity + LLM explanation of fit, match % per job |
| **Bullet Improver** | Converts weak bullets into strong, quantified achievements |
| **Career Advisor** | Skills roadmap, project suggestions, week-by-week learning plan |
| **File Handling** | Upload PDF/DOCX resume, download generated resume as `.txt` |

---

## 🛠 Tech Stack

- **Frontend**: Streamlit 1.32+
- **LLM**: LangChain + Groq (Llama 3 70B) or OpenAI (GPT-4o-mini)
- **Vector Search**: FAISS + `sentence-transformers` (all-MiniLM-L6-v2)
- **Resume Parsing**: PyPDF2, python-docx
- **Data & Charts**: pandas, numpy, plotly
- **Config**: python-dotenv

---

## ⚡ Quick Start (Local)

### 1. Clone the repo
```bash
git clone https://github.com/yourname/careercoPilot-ai.git
cd careercoPilot-ai/resume-analyzer
```

### 2. Create virtual environment
```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment
```bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY or OPENAI_API_KEY
```

Get a **free** Groq API key at https://console.groq.com

### 5. Run the app
```bash
streamlit run app.py
```

Open http://localhost:8501 in your browser.

---

## 🌐 Deployment

### Streamlit Community Cloud (Free)
1. Push the repo to GitHub.
2. Go to https://share.streamlit.io → **New app**.
3. Set **Main file path** to `resume-analyzer/app.py`.
4. Add secrets in **Advanced settings → Secrets** (paste your `.env` contents).
5. Click **Deploy**.

### Render.com
1. Create a new **Web Service** linked to your GitHub repo.
2. Set **Root directory** to `resume-analyzer`.
3. **Build command**: `pip install -r requirements.txt`
4. **Start command**: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true`
5. Add environment variables under **Environment**.

---

## 📂 Project Structure

```
resume-analyzer/
├── app.py                  # Streamlit entry point & navigation
├── requirements.txt
├── runtime.txt
├── Procfile
├── .env.example
├── README.md
├── src/
│   ├── embeddings.py       # FAISS index creation & search
│   ├── job_matcher.py      # Job matching orchestration
│   ├── rag_chain.py        # LangChain LLM chain factory
│   ├── resume_parser.py    # PDF / DOCX text extraction
│   ├── utils.py            # Shared helpers
│   ├── ats_scorer.py       # ATS keyword scoring
│   ├── resume_generator.py # LLM resume generation
│   ├── bullet_improver.py  # Bullet point enhancement
│   ├── career_advisor.py   # Career roadmap generation
│   └── pages/
│       ├── dashboard.py
│       ├── resume_analysis.py
│       ├── job_match.py
│       ├── resume_gen.py
│       ├── bullet_page.py
│       └── career_page.py
├── data/
│   └── jobs/
│       ├── sample_software_engineer.txt
│       └── sample_data_scientist.txt
└── vectorstore/            # FAISS index files (auto-generated)
```

---

## 🔮 Future Improvements

- [ ] LinkedIn profile import via scraping
- [ ] Multi-language resume support
- [ ] Interview question generator per job
- [ ] Cover letter generator
- [ ] Resume version history (database backend)
- [ ] OAuth login + cloud save
- [ ] Real-time job board scraping (Indeed, LinkedIn)
- [ ] Salary estimator per role
