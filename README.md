# 🧬 Aethera AI

> **Next-Generation Computational Chemistry & Molecular Science Intelligence Platform**

Aethera AI is a full-stack platform designed for exploring biochemical compounds, molecular properties, 3D visualization, and real-time scientific AI dialogue powered by **Aera AI** (integrated with Groq LPUs and Google Gemini).

---

## 🚀 Key Features

- **Molecular Explorer**: Interactive exploration of biochemical compounds, IUPAC names, SMILES, and chemical classifications.
- **Interactive 3D Visualizer**: Native 3D molecular viewer powered by `3Dmol.js` with multi-angle rotation, zoom, and representation styles.
- **Aera AI Assistant**: Domain-specialized scientific AI copilot streaming real-time analysis, literature citations, and biochemical explanations via ultra-low latency inference (Groq `openai/gpt-oss-120b` and Gemini fallback).
- **Trigram Fast Search**: Real-time fuzzy and trigram search across compounds, IUPAC names, formulas, and synonyms.
- **Production-Ready Architecture**: Designed for zero-downtime deployment on Vercel (Frontend), Railway/Render (Backend), and PostgreSQL.

---

## 🏗️ Architecture

```
Aethera AI
├── frontend/             # Next.js 16 (React 19, Tailwind CSS, Turbopack, 3Dmol.js)
├── backend/              # FastAPI, SQLAlchemy, PostgreSQL / SQLite, Groq & Google GenAI
│   ├── app/
│   │   ├── ai/           # Aera AI engine (Groq, Gemini, citations, streaming)
│   │   ├── api/          # REST endpoints (compounds, categories, search, chat)
│   │   ├── core/         # DB config (Postgres/SQLite auto-switching) & settings
│   │   └── models/       # SQLAlchemy database schemas
│   ├── alembic/          # Database schema migrations
│   ├── aethera_pg_dump.sql # Complete 174-record dataset dump for PostgreSQL
│   └── migrate_to_postgres.py # Automated SQLite-to-PostgreSQL migration tool
└── .gitignore            # Secret & credential protection
```

---

## ⚡ Quickstart (Local Development)

### 1. Backend Setup

```bash
cd backend
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
# Fill in GROQ_API_KEY from https://console.groq.com/keys

uvicorn app.main:app --reload --port 8000
```

Backend will run at: `http://localhost:8000` (API Docs: `http://localhost:8000/docs`)

### 2. Frontend Setup

```bash
cd frontend
npm install
cp .env.example .env.local

npm run dev
```

Frontend will run at: `http://localhost:3000`

---

## 🌐 Live Deployment (Path A)

1. **Database**: Provision a PostgreSQL instance on [Railway](https://railway.app) or [Neon](https://neon.tech).
2. **Data Migration**: Run `python backend/migrate_to_postgres.py --target "<YOUR_POSTGRES_URL>"` to upload all 174 records with zero data loss.
3. **Backend Deployment**: Deploy `backend/` to Railway with your `DATABASE_URL` and `GROQ_API_KEY`.
4. **Frontend Deployment**: Deploy `frontend/` to Vercel with `NEXT_PUBLIC_API_URL=https://<your-backend>.up.railway.app/api/v1`.

---

## 📄 License

MIT License. Built with ❤️ for molecular scientists, bioinformaticians, and developers.
