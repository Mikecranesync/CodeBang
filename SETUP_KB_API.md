# DevCTO Knowledge Base API - Setup Guide

Quick guide to set up and test the Agent-Factory KB API for DevCTO atoms.

## What Was Created

### 1. API Server
**File:** `Agent Factory/agent_factory/api/kb_api.py`

FastAPI server with endpoints:
- `GET /health` - Health check
- `POST /api/kb/search` - Vector search for atoms
- `GET /api/kb/atom?atom_id=<id>` - Fetch specific atom
- `POST /api/ingest` - Trigger ingestion
- `GET /api/kb/stats` - KB statistics

### 2. Parser
**File:** `CodeBang/parse_devcto_atoms.py`

Parses `DEVCTO_CLAUDE_ATOMS.md` into structured atoms with:
- Extracted metadata (atom_id, title, summary)
- Parsed keywords and related atoms
- Generated OpenAI embeddings

### 3. Ingestion Script
**File:** `CodeBang/ingest_devcto_atoms.py`

Inserts parsed atoms into `knowledge_atoms` table via Supabase.

### 4. KB Client (Ready to Use)
**File:** `CodeBang/kb_client_example.py`

Already configured with `http://localhost:8000` - no changes needed!

## Setup Steps

### Step 1: Verify Environment Variables

Check Agent-Factory `.env` has:
```bash
# In Agent Factory directory
cat .env | grep -E "OPENAI_API_KEY|SUPABASE_URL|SUPABASE_SERVICE_ROLE_KEY"
```

Required variables:
- `OPENAI_API_KEY` - For embeddings
- `SUPABASE_URL` - Database connection
- `SUPABASE_SERVICE_ROLE_KEY` (or `SUPABASE_KEY`)

### Step 2: Test the Parser

```bash
cd "C:\Users\hharp\OneDrive\Desktop\CodeBang"

# Test parser (should output 14 atoms)
python parse_devcto_atoms.py
```

Expected output:
```
Processing: devcto_project_overview
  Generating embedding for devcto_project_overview...
  ✓ Processed devcto_project_overview
...
Parsed 14 atoms successfully

PARSED ATOMS SUMMARY
====================================
devcto_project_overview:
  Title: Devcto Project Overview
  Summary: DevCTO Agent is a self-improving AI DevOps system...
  Keywords: Self-improving system, Targets non-technical founders, Builds on knowledge base...
  Related: devcto_core_loop, devcto_kb_integration, devcto_non_coder_safety...
  Embedding dims: 1536
...
Total atoms parsed: 14
```

### Step 3: Run Ingestion

```bash
cd "C:\Users\hharp\OneDrive\Desktop\CodeBang"

# Run ingestion
python ingest_devcto_atoms.py
```

Expected output:
```
DevCTO Atom Ingestion
======================================================================

Checking for existing DevCTO atoms...
Found 0 existing DevCTO atoms in database.

[1/4] Parsing DEVCTO_CLAUDE_ATOMS.md...
Processing: devcto_project_overview
...
✓ Parsed 14 atoms

[2/4] Connecting to Agent-Factory storage...
✓ Connected to Supabase

[3/4] Inserting atoms into knowledge_atoms table...
  ✓ devcto_project_overview
  ✓ devcto_core_loop
  ...
  ✓ devcto_implementation_phases

Ingestion complete: 14/14 successful

[4/4] Verifying ingestion...
✓ Verified: 14 DevCTO atoms in database

Ingested atoms:
  - devcto_project_overview
  - devcto_core_loop
  ...

SUMMARY: 14 succeeded, 0 failed
```

### Step 4: Start API Server

```bash
cd "C:\Users\hharp\OneDrive\Desktop\Agent Factory"

# Start API server
poetry run uvicorn agent_factory.api.kb_api:app --host 0.0.0.0 --port 8000 --reload
```

Expected output:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Step 5: Test API Endpoints

Open a new terminal and run:

**Health check:**
```bash
curl http://localhost:8000/health
```

Expected:
```json
{"status":"ok","database":"connected","provider":"supabase"}
```

**Search test:**
```bash
curl -X POST http://localhost:8000/api/kb/search \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"how does DevCTO work\", \"top_k\": 3}"
```

Expected: Returns `devcto_core_loop`, `devcto_project_overview`, etc.

**Get specific atom:**
```bash
curl http://localhost:8000/api/kb/atom?atom_id=devcto_core_loop
```

Expected: Full atom with summary, content, related_atoms, etc.

**Stats:**
```bash
curl http://localhost:8000/api/kb/stats
```

Expected:
```json
{
  "total_atoms": 1978,
  "namespaces": {
    "plc": 1964,
    "devcto": 14
  }
}
```

### Step 6: Test KB Client

```bash
cd "C:\Users\hharp\OneDrive\Desktop\CodeBang"

# Run KB client test
python kb_client_example.py
```

Expected output:
```
=== Bootstrap DevCTO Atoms ===

devcto_core_loop:
  Summary: The fundamental DevCTO workflow: (1) Digest...
  When to use: When implementing orchestrator logic...

...

=== KB Statistics ===
Total atoms: 1978
Namespaces: {'plc': 1964, 'devcto': 14}
```

## Troubleshooting

### Parser fails with "OPENAI_API_KEY not set"
**Solution:** Add to `.env` file:
```bash
OPENAI_API_KEY=sk-...your-key-here...
```

### Ingestion fails with "Supabase credentials not found"
**Solution:** Check `.env` has:
```bash
SUPABASE_URL=https://...supabase.co
SUPABASE_SERVICE_ROLE_KEY=eyJ...
```

### API server fails to start
**Solution:** Install dependencies:
```bash
cd "C:\Users\hharp\OneDrive\Desktop\Agent Factory"
poetry install
poetry add fastapi uvicorn python-dotenv openai
```

### Search returns no results
**Solution:** Check embeddings were generated:
```bash
# In Supabase dashboard, check knowledge_atoms table
# embedding column should have values, not NULL
```

### Port 8000 already in use
**Solution:** Use different port:
```bash
poetry run uvicorn agent_factory.api.kb_api:app --port 8001
# Update kb_client_example.py: KBClient("http://localhost:8001")
```

## Validation Checklist

- [ ] Parser runs and outputs 14 atoms
- [ ] Ingestion script completes with 14/14 successful
- [ ] API server starts without errors
- [ ] `/health` endpoint returns `"status": "ok"`
- [ ] `/api/kb/search` returns relevant atoms
- [ ] `/api/kb/atom?atom_id=devcto_core_loop` returns full atom
- [ ] `/api/kb/stats` shows `"devcto": 14` in namespaces
- [ ] `kb_client_example.py` successfully queries atoms

## Next Steps

Once all validation passes:

1. **Keep API running** in background or as service
2. **Update NEXT_STEPS.md** with API URL
3. **Start Phase 2** of DevCTO build plan
4. **Use KB in DevCTO** via kb_client.py

## Architecture Summary

```
CodeBang (DevCTO Bootstrap)
├── parse_devcto_atoms.py ─────┐
├── DEVCTO_CLAUDE_ATOMS.md     │
└── ingest_devcto_atoms.py ────┤
                               │
                               ▼
                    Agent Factory API
                    (kb_api.py)
                           │
                           ▼
                    Supabase Database
                    (knowledge_atoms table)
                           │
                           ▼
                    kb_client_example.py
                    (DevCTO queries KB)
```

## Database Schema

The atoms are stored in `knowledge_atoms` table:

```sql
CREATE TABLE knowledge_atoms (
    id UUID PRIMARY KEY,
    atom_id TEXT UNIQUE NOT NULL,     -- "devcto_core_loop"
    atom_type TEXT NOT NULL,           -- "pattern"
    title TEXT NOT NULL,               -- "Devcto Core Loop"
    summary TEXT NOT NULL,             -- Short description
    content TEXT NOT NULL,             -- Full markdown
    manufacturer TEXT NOT NULL,        -- "devcto" (namespace)
    product_family TEXT,               -- "agent"
    product_version TEXT,              -- "v1.0"
    difficulty TEXT NOT NULL,          -- "intermediate"
    prerequisites TEXT[],              -- []
    related_atoms TEXT[],              -- ["devcto_kb_integration", ...]
    source_document TEXT NOT NULL,     -- "DEVCTO_CLAUDE_ATOMS.md"
    source_pages INTEGER[],            -- [1]
    keywords TEXT[],                   -- ["digest", "analyze", ...]
    quality_score FLOAT DEFAULT 1.0,   -- 1.0 (hand-crafted)
    embedding vector(1536),            -- OpenAI embedding
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

## Cost

- **Parser:** ~$0.01 (14 OpenAI embeddings)
- **API:** $0 (runs locally or free tier)
- **Database:** $0 (Supabase free tier, 14 atoms = ~100KB)
- **Total:** ~$0.01 one-time

## Done!

Your DevCTO Knowledge Base is now ready! 🎉

The 14 learning atoms are accessible via API for DevCTO to query before implementing features.
