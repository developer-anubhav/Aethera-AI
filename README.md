# 🧬 Aethera AI — Precision Molecular Knowledge & Intelligence Platform

[![Frontend Status](https://img.shields.io/badge/Vercel-Deployed-black?style=flat&logo=vercel)](https://aethera-ai-flax.vercel.app)
[![Backend Status](https://img.shields.io/badge/Render-Live-46E3B7?style=flat&logo=render)](https://aethera-ai-f4g9.onrender.com)
[![Database](https://img.shields.io/badge/Neon-Serverless%20Postgres-00E599?style=flat&logo=postgresql)](https://neon.tech)
[![AI Engine](https://img.shields.io/badge/Aera%20AI-Groq%20LPU%20120B-F55036?style=flat)](https://groq.com)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

> **Next-Generation Computational Chemistry, 3D Molecular Visualization, and Real-Time Biochemical Intelligence.**

Aethera AI is a full-stack scientific platform engineered for molecular researchers, students, and computational chemists. It brings together verified biochemical data, interactive WebGL 3D molecular modeling, trigram-accelerated chemical search, and **Aera AI**—a domain-specialized scientific copilot streaming real-time analysis, literature citations, and biochemical mechanisms at ultra-low latency.

---

## 🌐 Live Production Deployments

| Component | Platform | Live URL | Description |
| :--- | :--- | :--- | :--- |
| **Frontend Web App** | **Vercel** | [https://aethera-ai-flax.vercel.app](https://aethera-ai-flax.vercel.app) | Next.js 16 (React 19) App Router UI with 3D WebGL viewer |
| **Backend REST API** | **Render** | [https://aethera-ai-f4g9.onrender.com](https://aethera-ai-f4g9.onrender.com) | FastAPI production ASGI service running Python |
| **Interactive API Docs** | **Render** | [https://aethera-ai-f4g9.onrender.com/api/v1/docs](https://aethera-ai-f4g9.onrender.com/api/v1/docs) | Swagger / OpenAPI 3.0 interactive endpoints |
| **API Health Check** | **Render** | [https://aethera-ai-f4g9.onrender.com/health](https://aethera-ai-f4g9.onrender.com/health) | Live system status & database ping probe |
| **Database** | **Neon** | Serverless PostgreSQL | High-concurrency pooled PostgreSQL with `pg_trgm` |

---

## ✨ Core Platform Capabilities

### 1. 🧪 Comprehensive Molecular Knowledge Base
- **Curated Dataset**: Deep scientific records covering Organic Chemistry, Inorganic Chemistry, Alcohols, Acids, Hydrocarbons, Carbohydrates, Proteins, Enzymes, Hormones, Lipids, Neurotransmitters, and more.
- **Biochemical Identifiers**: Standardized IUPAC names, molecular formulas, molecular weights, Canonical SMILES, InChI strings, CAS registry numbers, PubChem CIDs, and ChEBI IDs.
- **Physical & Chemical Specifications**: Solubilities, melting/boiling points, densities, appearance descriptions, acid dissociation constants ($\text{p}K_a$), refractive indices, chemical stability ratings, and reactivity profiles.
- **GHS Safety & Hazard Data**: Full Globally Harmonized System (GHS) classifications, hazard statements, precautionary measures, and recommended personal protective equipment (PPE).
- **Peer-Reviewed Reference Catalog**: Grounded literature citations linked to PubMed, PubChem, and digital object identifiers (DOIs).

### 2. 🧊 Interactive 3D WebGL Molecular Visualizer
- Native WebGL-accelerated 3D molecular modeling powered by `3Dmol.js`.
- Multi-angle rotation, zoom, pan, and centering controls.
- Dynamic structural representations: Ball-and-Stick, Wireframe, Space-Filling (CPK van der Waals spheres), and Cartoon ribbons.
- Real-time fallback to clean 2D topological structural formulas when WebGL is constrained.

### 3. 🧠 Aera AI — Scientific Intelligence Copilot
- **Ultra-Low Latency Inference**: Powered by **Groq LPU** inference engine (`openai/gpt-oss-120b`, ~300+ tokens/sec) with automatic failover to Google Gemini (`gemini-3.8-flash`).
- **Server-Sent Events (SSE) Streaming**: Instant token-by-token streaming response delivery.
- **Publication-Grade Formatting**: Structured Markdown headings, LaTeX mathematical rendering for chemical thermodynamics and equilibria ($\Delta G^\circ = \Delta H^\circ - T\Delta S^\circ$), reaction mechanisms, and side-by-side comparison tables.
- **Context-Grounded Verification**: Answers incorporate real-time database facts, citations, and structural data for the active molecule, while answering broader scientific questions with academic rigor.
- **5 Explanation Levels**: Adaptive pedagogical depths:
  - *School* (intuitive analogies and foundations)
  - *High School* (reaction types, basic stoichiometry)
  - *University* (orbital hybridization, kinetics, reaction mechanisms)
  - *Research* (crystallography, binding affinities, active-site amino acids)
  - *Professional* (pharmacodynamics, toxicology, clinical formulation)
- **4 Analytical Study Modes**: *Explain*, *Compare* (side-by-side matrix), *Summarize*, and *Teach*.
- **Stabilized UI Scrolling**: Container-isolated auto-scroll engine with overscroll containment—eliminates jitter and ensures the screen remains stationary while text streams in.

### 4. ⚡ Trigram-Accelerated Fuzzy Search
- Database-level trigram indexing using PostgreSQL's `pg_trgm` extension.
- Sub-millisecond search across compound names, IUPAC nomenclature, chemical formulas, and 60+ verified synonyms.
- Typo-tolerant query matching with automatic fallback scoring.

---

## 🏗️ System Architecture

```
                                  ┌──────────────────────────┐
                                  │   End Users / Chemists   │
                                  └────────────┬─────────────┘
                                               │
                                       HTTPS (Port 443)
                                               │
                                               ▼
                         ┌──────────────────────────────────────────┐
                         │         Vercel Edge Network              │
                         │   Next.js 16 (App Router + Turbopack)    │
                         │   React 19, Tailwind CSS 4, 3Dmol.js     │
                         └─────────────────────┬────────────────────┘
                                               │
                                   REST / SSE (/api/v1/*)
                                               │
                                               ▼
                         ┌──────────────────────────────────────────┐
                         │       Render Web Service (Linux)         │
                         │     FastAPI + Uvicorn Production ASGI    │
                         │  Clean Architecture: Repos / Services    │
                         └───────┬──────────────────────────┬───────┘
                                 │                          │
                 PostgreSQL Wire │ (pg_trgm)        HTTPS   │ Ultra-Fast SSE
                                 ▼                          ▼
       ┌───────────────────────────────────┐    ┌──────────────────────────┐
       │     Neon Serverless PostgreSQL    │    │      Groq LPU Cloud      │
       │   Pooled Connection (Port 5432)   │    │   openai/gpt-oss-120b    │
       │   11 Normalized Scientific Tables │    │ (Fallback: Google Gemini)│
       └───────────────────────────────────┘    └──────────────────────────┘
```

---

## 🗄️ Database Schema & Data Models

The relational schema is engineered with strict referential integrity, cascading deletes, and foreign key constraints:

| Table | Primary Key | Description | Relationships |
| :--- | :--- | :--- | :--- |
| `categories` | `id` (Serial) | Broad chemical classifications (slug, description) | $1 \to N$ with `compounds` |
| `compounds` | `id` (Serial) | Core molecular record (name, formula, smiles, inchi, CAS) | Belongs to `category`, has many child entities |
| `biomolecules` | `id` (Serial) | Classification for biological macromolecules | Belongs to `compound` |
| `proteins` | `id` (Serial) | Structural protein details (PDB ID, sequence, structure) | Belongs to `biomolecule` |
| `enzymes` | `id` (Serial) | Catalytic properties (EC number, active site, substrates) | Belongs to `biomolecule` |
| `physical_properties` | `id` (Serial) | Boiling/melting points, appearance, density, solubility | $1 \to 1$ with `compound` |
| `chemical_properties` | `id` (Serial) | $\text{p}K_a$, reactivity, refractive index, chemical stability | $1 \to 1$ with `compound` |
| `hazards` | `id` (Serial) | GHS classifications, hazard/precautionary statements, PPE | $1 \to 1$ with `compound` |
| `references` | `id` (Serial) | Peer-reviewed citations, DOIs, and literature URLs | $N \to 1$ with `compound` |
| `visualization_metadata`| `id` (Serial) | WebGL camera angles, default styles, 3D rendering hints | $1 \to 1$ with `compound` |
| `synonyms` | `id` (Serial) | Alternate chemical and commercial trade names | $N \to 1$ with `compound` |

---

## 🔌 API Reference & Endpoints

All REST API endpoints are prefixed with `/api/v1`. Interactive documentation is accessible at [`/api/v1/docs`](https://aethera-ai-f4g9.onrender.com/api/v1/docs).

### Core Endpoints

#### 1. System Health
- `GET /health` or `GET /api/v1/health`
  - Returns: `{"status": "healthy", "service": "Aethera AI"}`

#### 2. Compounds
- `GET /api/v1/compounds` — List all compounds (supports pagination: `skip`, `limit`, and `category_id`).
- `GET /api/v1/compounds/{slug_or_id}` — Retrieve complete molecular record including physical properties, chemical properties, GHS hazards, references, and 3D visualization metadata.

#### 3. Categories
- `GET /api/v1/categories` — List all chemical classifications.
- `GET /api/v1/categories/{slug_or_id}` — Get category details and list associated compounds.

#### 4. Search
- `GET /api/v1/search?q={query}` — Execute trigram fuzzy search across names, formulas, IUPAC descriptions, and synonyms.
- `GET /api/v1/search/suggestions?q={query}` — Fast auto-complete suggestions.

#### 5. Aera AI Scientific Intelligence
- `POST /api/v1/aera/chat` — Real-time Server-Sent Events (SSE) streaming chat endpoint.
  - **Request Body**:
    ```json
    {
      "compound_slug": "aspirin",
      "question": "What is the mechanism of ester hydrolysis in acidic media?",
      "level": "university",
      "mode": "explain",
      "messages": []
    }
    ```
  - **Response**: `text/event-stream` yielding token deltas and finishing with an audited citation metadata payload:
    ```json
    data: {"type": "content", "delta": "## Mechanism of Hydrolysis\n..."}
    data: {"type": "metadata", "request_id": "8ac9226b", "completion_tokens": 916, "total_time_ms": 3360, "citations": [...]}
    ```

---

## 🛠️ Tech Stack Overview

### Frontend
- **Framework**: Next.js 16.3 (React 19, Turbopack)
- **Styling**: Tailwind CSS 4, `@tailwindcss/postcss`
- **State & Data Fetching**: TanStack React Query v5, Zustand v5, Axios
- **Molecular Rendering**: `3Dmol.js` (WebGL-accelerated PDB/SDF coordinate renderer)
- **Markdown & LaTeX**: `react-markdown` v10, `remark-gfm` v4
- **Icons**: Lucide React

### Backend
- **Framework**: FastAPI (Python 3.11 / 3.12 / 3.14 compatible)
- **ASGI Server**: Uvicorn (standard event loop with uvloop)
- **ORM & Data**: SQLAlchemy 2.0, Alembic migrations, Psycopg2-binary
- **Validation**: Pydantic v2, Pydantic-Settings
- **LLM Integrations**: Groq SDK (`openai/gpt-oss-120b`), Google GenAI SDK (`google-genai` v2)
- **Cache**: Redis pass-through client with graceful in-memory fallback

### Cloud Infrastructure
- **Frontend Hosting**: Vercel (Edge network, global CDN, automatic SSL)
- **Backend Hosting**: Render (Linux Web Service, automatic CI/CD from `main`)
- **Database**: Neon (Serverless PostgreSQL with connection pooling & `pg_trgm`)

---

## 💻 Local Development Setup

### Prerequisites
- Python 3.11+
- Node.js 18+ and `npm`
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/developer-anubhav/Aethera-AI.git
cd Aethera-AI
```

### 2. Backend Setup
```bash
cd backend

# Create and activate virtual environment
python -m venv .venv

# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
```

Edit `backend/.env` with your credentials:
```env
LLM_PROVIDER=groq
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=openai/gpt-oss-120b
DATABASE_URL=sqlite:///./aethera.db
BACKEND_CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

Start the backend server:
```bash
uvicorn app.main:app --reload --port 8000
```
API will be live at: `http://localhost:8000` (Docs: `http://localhost:8000/docs`)

### 3. Frontend Setup
In a new terminal window:
```bash
cd frontend

# Install Node dependencies
npm install

# Configure environment variables
cp .env.example .env.local
```

Ensure `frontend/.env.local` contains:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

Start the frontend development server:
```bash
npm run dev
```
Open `http://localhost:3000` in your browser.

---

## 🧪 Testing & Verification

Aethera AI includes a standalone end-to-end verification suite that validates database connectivity, schema integrity, trigram queries, and live LLM streaming:

```bash
# Run from project root with backend venv active
python backend/verify_neon_e2e.py
```

### Test Suite Output:
```text
==================================================
AETHERA AI — END-TO-END NEON POSTGRESQL VERIFICATION
==================================================
[PASS] 1. API Health: 200 -> {'status': 'healthy', 'service': 'Aethera AI'}
[PASS] 2. Categories: 200 -> Successfully retrieved 17 categories from Neon
[PASS] 3. Compounds: 200 -> Successfully retrieved 13 compounds from Neon
[PASS] 4. PostgreSQL Trigram Search: Found 1 matches for query 'aspirin' -> ['Aspirin']
[PASS] 5. Compound Detail: Aspirin | SMILES=CC(=O)Oc1ccccc1C(=O)O | Formula=C9H8O4
[PASS] 6. Aera AI Real-time Streaming (Groq): 200 -> Stream connected! Sample: ## Overview...
==================================================
ALL 6 END-TO-END VERIFICATION TESTS PASSED SUCCESSFULLY!
==================================================
```

---

## 🚀 Zero-Loss Migration (SQLite $\to$ PostgreSQL)

A dedicated migration tool is included to sync records between local development SQLite (`aethera.db`) and remote PostgreSQL without data loss:

```bash
# Push all data live to any PostgreSQL instance (Neon, Supabase, Railway)
python backend/migrate_to_postgres.py --target "postgresql://user:password@host:5432/dbname?sslmode=require"
```

The script automatically:
1. Generates an idempotent SQL dump ([`backend/aethera_pg_dump.sql`](backend/aethera_pg_dump.sql)).
2. Enables the `pg_trgm` extension on PostgreSQL.
3. Builds the relational schema via SQLAlchemy.
4. Transfers records in strict foreign-key dependency order with `ON CONFLICT ("id") DO NOTHING`.
5. Resets all PostgreSQL sequence counters (`setval`).
6. Verifies row-for-row parity across all 11 tables.

---

## ⚙️ Environment Variables Reference

### Backend (`backend/.env` / Render Settings)
| Variable | Required | Default / Example | Purpose |
| :--- | :--- | :--- | :--- |
| `LLM_PROVIDER` | Yes | `groq` | Active AI provider (`groq` or `gemini`) |
| `GROQ_API_KEY` | Yes | `gsk_...` | Groq Cloud API key from console.groq.com |
| `GROQ_MODEL` | Yes | `openai/gpt-oss-120b` | Primary Groq model ID |
| `GEMINI_API_KEY`| No | `AIza...` | Google AI Studio key (fallback) |
| `GEMINI_MODEL` | No | `gemini-3.8-flash` | Fallback Gemini model ID |
| `DATABASE_URL` | Yes | `postgresql://...` | Connection-pooled PostgreSQL connection string |
| `DATABASE_URL_UNPOOLED` | No | `postgresql://...` | Direct connection string for DDL migrations |
| `BACKEND_CORS_ORIGINS` | Yes | `*` or comma-separated URLs | Allowed origins for cross-origin resource sharing |

### Frontend (`frontend/.env.local` / Vercel Settings)
| Variable | Required | Example | Purpose |
| :--- | :--- | :--- | :--- |
| `NEXT_PUBLIC_API_URL` | Yes | `https://aethera-ai-f4g9.onrender.com/api/v1` | URL pointing to the FastAPI backend API root |

---

## 📁 Repository Directory Structure

```
Aethera-AI/
├── .github/                # GitHub workflows & configuration
├── .gitignore              # Multi-tier secret & artifact exclusion
├── LICENSE                 # MIT License
├── README.md               # Full platform documentation & specifications
├── neon.ts                 # Neon database & branch configuration
├── package.json            # Neon CLI dependency manifest
│
├── backend/                # FastAPI Production Backend Service
│   ├── alembic/            # Database schema migration revisions
│   ├── app/
│   │   ├── ai/             # Aera AI engine (Groq, Gemini, citations, prompts)
│   │   │   ├── prompts/    # Specialized pedagogical templates (explain, compare, etc.)
│   │   │   ├── factory.py  # Unified multi-provider LLM factory
│   │   │   ├── groq_client.py   # Groq LPU streaming integration
│   │   │   ├── gemini_client.py # Google GenAI SDK fallback client
│   │   │   └── system_prompt.py # Scientific persona & constraints
│   │   ├── api/            # API route controllers (compounds, categories, search, aera)
│   │   ├── core/           # DB connection management, exceptions, settings
│   │   ├── models/         # SQLAlchemy 2.0 ORM database models
│   │   ├── repositories/   # Clean data-access layer repositories
│   │   ├── schemas/        # Pydantic v2 validation schemas
│   │   ├── services/       # Business logic (Aera streaming, compound orchestration)
│   │   └── main.py         # FastAPI application entrypoint & lifespan events
│   ├── aethera_pg_dump.sql # Complete 163-record PostgreSQL verified dump
│   ├── Dockerfile          # Production multi-stage Docker build recipe
│   ├── migrate_to_postgres.py # Automated zero-loss SQLite-to-PostgreSQL migrator
│   ├── Procfile            # Deployment start command for Render / Heroku
│   ├── requirements.txt    # Frozen Python production dependencies
│   └── verify_neon_e2e.py  # Automated 6-step end-to-end verification suite
│
└── frontend/               # Next.js 16 Web Application
    ├── public/             # Static scientific visual assets & 3Dmol.js
    ├── src/
    │   ├── app/            # App Router pages (/search, /categories, /compounds/[id])
    │   ├── components/     # Reusable layout & 3D/2D visualizers (MolecularViewer3D)
    │   ├── features/       # Feature modules (CompoundDetailView, AeraChatPanel)
    │   ├── services/       # Axios & SSE API client integration (api.ts)
    │   └── types/          # TypeScript scientific domain definitions
    ├── next.config.ts      # Next.js engine configuration
    ├── package.json        # Frontend dependencies & npm scripts
    └── vercel.json         # Vercel deployment routing & headers
```

---

## 📜 License

This project is licensed under the terms of the [MIT License](LICENSE).

---

## 🤝 Contributing & Acknowledgments

Contributions to scientific records, molecular visualizations, and chemical search algorithms are welcome! Feel free to open an issue or submit a pull request.

Special thanks to:
- **PubChem & ChEBI** for open chemical data standards.
- **3Dmol.js** team for WebGL molecular visualization tools.
- **Groq** for high-throughput LPU inference technology.
- **Neon** for serverless PostgreSQL developer infrastructure.
