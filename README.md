# 🧠 High-Performance RAG Web Application

> A production-ready **Retrieval-Augmented Generation (RAG)** system built with FastAPI and React. Designed for zero-cost deployment and high accuracy.

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)
![Python 3.11](https://img.shields.io/badge/Python-3.11-blue)
![React](https://img.shields.io/badge/React-18-cyan)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-teal)

## ✨ key Features

This application isn't just a simple search wrapper. It includes advanced features to mimic a conversational AI experience without the cost of LLMs.

### 🔍 Advanced Retrieval
- **Context Awareness (Memory)**: Remembers who you are talking about.
  - *User*: "Who is Sundar Pichai?"
  - *User*: "Where did **he** study?" -> *System understands "he" = Sundar Pichai*
- **Fuzzy Search & Typo Tolerance**: Handles misspellings gracefully.
  - *User*: "tell me about satya **nadela**" -> *Finds Satya Nadella* (96% match)
- **Comprehensive Answers**: ask for "everything" to get a full report.
  - *User*: "tell me **everything** about Jensen Huang" -> *Combines Summary + Education + Career + Contribution*
- **Concept Understanding**: Retrieves technical concepts from `json` knowledge bases.
  - *User*: "python list comprehension" -> *Returns direct technical explanation*
- **Smart Shortcuts**: Understands quick commands.
  - `info` -> `information`, `def` -> `definition`

### 🏗️ Architecture
- **Backend**: FastAPI (Python) with `sentence-transformers` (all-MiniLM-L6-v2) and FAISS for vector search.
- **Frontend**: React + Tailwind CSS (bundled and served by FastAPI).
- **Deployment**: Monolithic architecture ready for Render Free Tier.
- **Database**: Zero-conf SQLite + JSON file loading.

---

## 🚀 Quick Start (Local)

### 1. Clone & Setup
```bash
git clone https://github.com/RohitSrivatsa29/rag-app.git
cd rag-app
```

### 2. Install Backend Dependencies
```bash
pip install -r requirements.txt
```

### 3. Build Frontend
```bash
cd frontend
npm install
npm run build
cd ..
```

### 4. Run Application
```bash
python app.py
```
Visit **http://localhost:8000** to chat!

---

## �️ Configuration

### adding Knowledge
Simply drop your JSON files into the `data/` folder. The system auto-indexes them on startup.
Supported structure:
```json
[
  {
    "id": "unique_id",
    "name": "Entity Name",
    "summary": "Brief description...",
    "education": "University...",
    "career": "Work history..."
  }
]
```

### Deployment (Render)
1. Push this repo to GitHub.
2. Link to **Render** as a Web Service.
3. Use the following commands:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app:app --host 0.0.0.0 --port 10000`

---

## 🤝 Contributing
Contributions are welcome! improving the `search.py` logic or adding new data sources is a great place to start.

## 📄 License
MIT License.
