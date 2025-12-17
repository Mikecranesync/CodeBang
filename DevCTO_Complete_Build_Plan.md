# DevCTO Agent: Complete Build Plan A to Z

**Project Goal:** Build a self-improving AI DevOps agent that learns best practices, templates, and patterns, then uses that knowledge to maintain your codebases and eventually generate complete applications from specifications.

**Your Role:** Non-coder founder + Claude Code as your development partner.

---

## Phase 0: The Learning Foundation (Before You Build the Repo)

### 0.1 Purpose

Before creating a new `DevCTO-Agent` repo, you need to **teach the system how to build itself**. This means your existing Agent-Factory ingestion pipeline and knowledge base become the blueprint and knowledge source for everything that comes next.

### 0.2 Set Up the Learning Spec in Agent-Factory

Create a new document: `docs/learning/DEVCTO_LEARNING_SPEC.md` in your Agent-Factory repo.

```markdown
# DevCTO Learning Specification

## Topics to Master (in order)

1. **Claude Code Headless Automation**
   - How to run Claude Code from scripts non-interactively
   - Allowed tools, permission modes, output formats
   - Integration with bash/cron/CI

2. **Repository Digest & Analysis**
   - Tools like Repomix and Codebase-digest
   - Converting code into AI-readable summaries
   - Metrics and health scores

3. **Model Context Protocol (MCP)**
   - Server design and tool patterns
   - Gateway architecture and routing
   - Security and least-privilege patterns

4. **Observability & LangFuse**
   - Wiring traces and metrics into LLM apps
   - Evaluation patterns and sampling
   - Callback hooks and decorators

5. **GitHub Scouting & Reuse**
   - Finding and evaluating open-source repos
   - License filtering and integration patterns
   - Adapting external code to your stack

6. **Non-Coder Guardrails**
   - Safe PR generation (diff limits, tests, etc.)
   - "Don't touch" zones and permissions
   - Mandatory explanations and rollback paths

7. **Git Workflows & Worktrees**
   - Creating and managing git worktrees
   - Branch naming and commit patterns
   - PR safety and review checklists

## Sources to Ingest

- Claude Code docs (especially headless and automation)
- Anthropic best-practices guides
- Real GitHub repos: LangGraph + LangFuse examples, MCP servers, Claude automation demos
- Code review tool comparisons and tutorials
- DevOps and "self-healing code" articles from 2025
- Your own CLAUDE.md and existing patterns

## Output: Learning Atoms

Each ingested source becomes one or more atoms:
- `headless_pattern_basic`
- `mcp_gateway_design`
- `repo_digest_tools`
- `langfuse_integration_pattern`
- `github_scout_workflow`
- `pr_safety_checklist`
- `git_worktree_guide`

Each atom includes: summary, when to use, code examples, real repo links.
```

### 0.3 Ingest Sources Using Agent-Factory

1. **Run your existing ingestion agents** on the sources listed in the spec.
   - Example: `poetry run python agents/research_agent.py --query "Claude Code headless automation"`
2. **Build atoms** from the results using your AtomBuilder agent.
3. **Store in your knowledge base** (Pinecone, Supabase, or local vector DB).

### 0.4 Validate the Learning

Ask Claude (in a simple chat or notebook):

> "Here are the learning atoms we've ingested about building a self-improving dev agent. 
> Does this cover enough ground for me to design and build a repo that does:
> 1) digest codebases,
> 2) analyze them for improvements,
> 3) propose and implement small safe changes,
> 4) learn patterns from successes/failures?
> 
> What's missing?"

Update the learning spec with gaps, then re-ingest.

**Milestone:** When Claude can answer "Design the DevCTO repo structure from these atoms" with confidence → move to Phase 1.

---

## Phase 0.5: Cloud Dev Box Setup ✅

**Goal:** Make CodeBang and Agent-Factory accessible via SSH from laptop/Android with minimal setup overhead.

**Status:** Implemented

### What Was Created

Three helper scripts in `CodeBang/scripts/`:

1. **setup_vm.sh** - One-time VM setup
   - Checks Claude Code CLI installation
   - Installs Python dependencies (python-dotenv, openai, requests, pyyaml)
   - Verifies Agent-Factory .env configuration
   - Provides next steps guidance

2. **start_kb_api.sh** - KB API startup helper
   - Checks if API already running at http://localhost:8000
   - Locates Agent-Factory repository
   - Starts uvicorn server (poetry or pip mode)
   - Verifies successful startup with health check
   - Writes logs to /tmp/kb_api.log

3. **start_claude.sh** - Main entry point
   - Unified launcher for both CodeBang and Agent-Factory repos
   - Optional KB API startup with `--with-kb` flag
   - Shows context files available to Claude
   - Launches Claude Code in interactive mode

### Usage on Fresh Cloud VM

```bash
# One-time setup
mkdir ~/repos && cd ~/repos
git clone <codebang-url> CodeBang
git clone <agent-factory-url> "Agent Factory"

cd CodeBang
./scripts/setup_vm.sh

# Configure Agent-Factory (if using KB)
cd "../Agent Factory"
cp .env.example .env
nano .env  # Add API keys

# Start working
cd ~/repos/CodeBang
./scripts/start_claude.sh                   # Work on CodeBang
./scripts/start_claude.sh codebang --with-kb  # Work on CodeBang + KB API
./scripts/start_claude.sh agent-factory     # Work on Agent-Factory
```

### From Laptop/Android

```bash
ssh user@your-vm-ip
cd ~/repos/CodeBang
./scripts/start_claude.sh
```

### Documentation Updates

- **CLAUDE.md** - Added "Cloud Dev Box Quick Start" section at top
- **This file** - Added Phase 0.5 documentation

**Milestone:** User can SSH into cloud VM, run one command (`./scripts/start_claude.sh`), and immediately work with Claude Code having full DevCTO context.

---

## Phase 1: Design the DevCTO Repo (Still Using Agent-Factory)

### 1.1 Repo Design Document

Create `docs/learning/DEVCTO_REPO_DESIGN.md` in Agent-Factory by asking Claude:

> "Based on the learning atoms about Claude Code headless, MCP, repo analysis, and observability,
> design a new repository structure for DevCTO Agent that:
> 
> 1) Calls Agent-Factory APIs for KB queries and analysis
> 2) Runs digest → analyze → act → learn loops
> 3) Has safety guardrails for non-coders
> 4) Supports future template and app-builder features
> 
> Provide:
> - Folder structure (tree)
> - Key modules and their responsibilities
> - Config files needed
> - Validation commands (what tests run)
> - How it integrates with Agent-Factory"

Claude will output something like:

```
devcto-agent/
├── src/
│   ├── orchestrator/        # Main digest → analyze → act → learn loop
│   ├── kb_client/           # Calls Agent-Factory KB via API
│   ├── digest/              # Repo analysis using Repomix/Codebase-digest
│   ├── analyzer/            # Claude analysis of digests
│   ├── executor/            # Claude Code headless execution
│   ├── feedback/            # Tracks PR outcomes and learns
│   └── templates/           # Stores and versions templates
├── config/
│   ├── guardrails.yaml      # Safety rules: diff limits, don't-touch zones
│   ├── patterns.yaml        # Known patterns for this repo
│   └── integrations.yaml    # API endpoints for Agent-Factory, GitHub, etc.
├── scripts/
│   ├── run_digest.sh
│   ├── run_analysis.sh
│   ├── run_once.sh          # Single end-to-end run
│   └── schedule.sh          # Cron/automation setup
├── tests/
│   ├── test_digest.py
│   ├── test_analyzer.py
│   ├── test_executor.py
│   └── test_e2e.py
├── docs/
│   ├── CLAUDE.md            # AI assistant instructions
│   ├── API_SPEC.md          # How to call Agent-Factory
│   └── GUARDRAILS.md        # Safety and permissions
├── pyproject.toml
└── README.md
```

### 1.2 Document Key Decisions

In the design doc, capture:

- **Why MCP for KB access?** → Standardized, secure, scalable.
- **Why headless Claude Code?** → Automatable, works in CI and cron.
- **How do we keep it safe?** → Strict diff limits, validation commands, guardrails.yaml.
- **How does it learn?** → Tracks merged/rejected PRs, updates patterns.yaml.

### 1.3 Validate the Design

Share this design with Claude and ask:

> "Does this design make sense? Can Claude Code realistically build a working skeleton 
> from this? What's the first thing we should implement to test the core loop?"

Update the design based on feedback.

**Milestone:** Design doc approved → ready to create the real repo.

---

## Phase 2: Create and Scaffold the DevCTO Repo

### 2.1 Create the GitHub Repo

1. Go to github.com and create a new repo: `DevCTO-Agent` or `CodeForge-Agent`.
2. Clone it locally:
   ```bash
   git clone https://github.com/yourusername/DevCTO-Agent.git
   cd DevCTO-Agent
   ```

### 2.2 Have Claude Code Build the Skeleton

1. **Open Claude Code in the new repo:**
   ```bash
   cd DevCTO-Agent
   claude
   ```

2. **Give it the design and learning atoms:**

Copy/paste or reference your `DEVCTO_REPO_DESIGN.md` and sample learning atoms into the chat.

3. **Prompt Claude Code:**

```
You are building the DevCTO Agent, a self-improving AI DevOps system.

Here is the target repo structure and the learning atoms about Claude Code, MCP, repo analysis, and safety.

For this first session:
1) Create the full folder structure from the design
2) Add skeleton Python modules with docstrings (no logic yet)
3) Create guardrails.yaml with safety defaults
4) Add a CLAUDE.md for future Claude Code work
5) Add pyproject.toml with required dependencies
6) Add basic tests that import and run

Do NOT implement full logic; just prove the skeleton compiles and basic imports work.
Run: poetry install && poetry run pytest

Show me the structure and test results.
```

4. **Claude Code will:**
   - Create folders
   - Write stub modules
   - Add config files
   - Create basic tests

5. **Review and iterate** until:
   - All imports pass
   - Tests run (even if they just check structure)
   - You understand what's in each folder

### 2.3 Commit and Document

```bash
git add .
git commit -m "SKELETON: Initial repo structure and modules"
git push
```

Create a file `docs/SKELETON_NOTES.md` documenting what was built and why.

**Milestone:** Repo skeleton exists, tests pass, you can read and understand the structure.

---

## Phase 3: Implement the Core Loop (Digest → Analyze → Act → Learn)

### 3.1 Connect to Agent-Factory KB via API

First, expose KB APIs in Agent-Factory:

In `agent_factory/core/api.py` (or equivalent), add endpoints:

```python
@app.post("/api/kb/search")
def search_atoms(query: str, top_k: int = 5):
    """Search learning atoms by query"""
    results = kb.search(query, top_k)
    return {"atoms": results}

@app.post("/api/kb/atom")
def get_atom(atom_id: str):
    """Fetch a specific atom"""
    atom = kb.get(atom_id)
    return {"atom": atom}

@app.post("/api/ingest")
def ingest_source(url: str, source_type: str):
    """Trigger ingestion of a new source"""
    job_id = ingest_agent.queue_job(url, source_type)
    return {"job_id": job_id}
```

### 3.2 Build KB Client in DevCTO

In `src/kb_client/client.py`:

```python
import requests

class KBClient:
    def __init__(self, agent_factory_url: str):
        self.base_url = agent_factory_url
    
    def search(self, query: str, top_k: int = 5):
        """Search the knowledge base"""
        resp = requests.post(
            f"{self.base_url}/api/kb/search",
            json={"query": query, "top_k": top_k}
        )
        return resp.json()["atoms"]
    
    def get_atom(self, atom_id: str):
        """Get a specific atom"""
        resp = requests.get(
            f"{self.base_url}/api/kb/atom",
            params={"atom_id": atom_id}
        )
        return resp.json()["atom"]
```

### 3.3 Implement Digest Module

`src/digest/digest_builder.py`:

```python
import subprocess
import json

class DigestBuilder:
    def build_repo_digest(self, repo_path: str):
        """
        Use Repomix or Codebase-digest to create a repo summary.
        Returns: structured summary, metrics, file tree.
        """
        # Example: run Repomix
        result = subprocess.run(
            ["npx", "codebase-digest@latest"],
            cwd=repo_path,
            capture_output=True,
            text=True
        )
        
        digest = json.loads(result.stdout)
        return {
            "tree": digest.get("tree"),
            "metrics": digest.get("metrics"),
            "hotspots": digest.get("hotspots"),
            "summary": digest.get("summary")
        }
```

### 3.4 Implement Analyzer Module

`src/analyzer/analyzer.py`:

```python
class AnalyzerAgent:
    def __init__(self, kb_client):
        self.kb = kb_client
    
    def analyze_digest(self, digest: dict, repo_context: dict):
        """
        Analyze a repo digest and return:
        - identified issues
        - missing patterns
        - suggested improvements
        """
        # Search KB for relevant patterns
        patterns = self.kb.search("code quality patterns", top_k=10)
        
        # TODO: Call Claude to analyze using patterns + digest
        # For now, return placeholder
        return {
            "issues": ["missing tests", "weak observability"],
            "patterns_available": patterns,
            "next_steps": ["add LangFuse hooks", "add unit tests"]
        }
```

### 3.5 Implement Executor Module

`src/executor/executor.py`:

```python
import subprocess

class CodeExecutor:
    def execute_improvement(self, repo_path: str, plan: dict):
        """
        Execute a plan by calling Claude Code headless.
        Returns: success, branch created, PR info.
        """
        prompt = f"""
        Here is a repo digest and improvement plan.
        
        Digest: {plan['digest']}
        Plan: {plan['improvements']}
        
        Follow these steps:
        1) Create a branch: git checkout -b devcto/improvement-{plan['id']}
        2) Apply the improvement (add tests, fix structure, etc.)
        3) Run validation: pytest
        4) Commit and push the branch
        5) Report what you did in a file: .devcto/last_run.md
        """
        
        result = subprocess.run(
            ["claude", "-p", prompt, "--allowedTools", "Bash,Read,Edit", "--permission-mode", "acceptEdits"],
            cwd=repo_path,
            capture_output=True,
            text=True
        )
        
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "errors": result.stderr
        }
```

### 3.6 Implement Learn Module

`src/feedback/learner.py`:

```python
class Learner:
    def __init__(self, kb_client):
        self.kb = kb_client
    
    def process_pr_outcome(self, pr_info: dict):
        """
        Track whether a PR was merged and update patterns.
        """
        if pr_info["merged"]:
            # Log success: this pattern works
            self.log_success(pr_info["pattern_id"], pr_info["changes"])
        else:
            # Log rejection: update pattern or skip
            self.log_rejection(pr_info["pattern_id"], pr_info["reason"])
    
    def update_local_patterns(self):
        """
        Refresh patterns.yaml with what we've learned.
        """
        # Query KB for updated patterns
        updated = self.kb.search("learned patterns", top_k=20)
        self.write_patterns_yaml(updated)
```

### 3.7 Main Orchestrator

`src/orchestrator/orchestrator.py`:

```python
class Orchestrator:
    def __init__(self, config):
        self.config = config
        self.kb = KBClient(config["agent_factory_url"])
        self.digest_builder = DigestBuilder()
        self.analyzer = AnalyzerAgent(self.kb)
        self.executor = CodeExecutor()
        self.learner = Learner(self.kb)
    
    def run_once(self, repo_path: str):
        """
        Single end-to-end cycle: digest → analyze → act → learn
        """
        print("=== DevCTO: Digest ===")
        digest = self.digest_builder.build_repo_digest(repo_path)
        
        print("=== DevCTO: Analyze ===")
        analysis = self.analyzer.analyze_digest(digest, {"path": repo_path})
        
        print("=== DevCTO: Execute ===")
        result = self.executor.execute_improvement(repo_path, analysis)
        
        if result["success"]:
            print("=== DevCTO: Learn ===")
            self.learner.process_pr_outcome({
                "merged": True,
                "pattern_id": analysis.get("pattern_id"),
                "changes": result.get("summary")
            })
        
        return result
```

### 3.8 Add Orchestration Script

`scripts/run_once.sh`:

```bash
#!/usr/bin/env bash
set -e

REPO_PATH="${1:-.}"
CONFIG="${2:./config/guardrails.yaml}"

echo "DevCTO: Running single cycle on $REPO_PATH"
poetry run python -c "
from src.orchestrator.orchestrator import Orchestrator
import yaml

with open('$CONFIG') as f:
    config = yaml.safe_load(f)

orchestrator = Orchestrator(config)
result = orchestrator.run_once('$REPO_PATH')
print('Done:', result)
"
```

### 3.9 Write Tests

`tests/test_e2e.py`:

```python
def test_end_to_end_on_sample_repo():
    """Test the full digest → analyze → execute → learn loop"""
    from src.orchestrator.orchestrator import Orchestrator
    
    config = {
        "agent_factory_url": "http://localhost:8000",
        "max_diff_lines": 300,
    }
    
    orchestrator = Orchestrator(config)
    result = orchestrator.run_once("./test_fixtures/sample_repo")
    
    assert result["success"]
    assert "changes" in result
```

### 3.10 Validate and Commit

```bash
poetry install
poetry run pytest
git add .
git commit -m "CORE LOOP: Digest, analyze, execute, learn implemented"
git push
```

**Milestone:** Core loop works end-to-end. You can run `./scripts/run_once.sh /path/to/repo` and it digests, analyzes, and attempts an improvement.

---

## Phase 4: Add Safety Guardrails

### 4.1 Guardrails Configuration

`config/guardrails.yaml`:

```yaml
safety:
  max_diff_lines: 300
  max_files_changed: 10
  max_time_per_run_seconds: 900
  
dont_touch:
  - "infra/production"
  - "src/payments"
  - ".env*"
  - "secrets/*"

required_before_commit:
  - "pytest passes"
  - "code is type-hinted"
  - "docstrings added"

branch_naming:
  prefix: "devcto/"
  pattern: "devcto/improvement-{id}"

pr_requirements:
  - "include summary in DEVCTO_REPORT.md"
  - "link to relevant KB atoms"
  - "explain what changed and why"

auto_approve_patterns:
  - "add_tests_for_function"
  - "type_hints_missing_module"
  - "add_logging_pattern"

manual_approval_required:
  - "database_migrations"
  - "api_signature_changes"
  - "security_related"
```

### 4.2 Implement Guardrails Checker

`src/guardrails/checker.py`:

```python
import yaml

class GuardrailsChecker:
    def __init__(self, config_path: str):
        with open(config_path) as f:
            self.config = yaml.safe_load(f)
    
    def check_diff(self, diff_lines: list, files_changed: list):
        """Validate a diff against guardrails"""
        errors = []
        
        # Check line count
        if len(diff_lines) > self.config["safety"]["max_diff_lines"]:
            errors.append(f"Diff too large: {len(diff_lines)} > {self.config['safety']['max_diff_lines']}")
        
        # Check files
        if len(files_changed) > self.config["safety"]["max_files_changed"]:
            errors.append(f"Too many files changed: {len(files_changed)}")
        
        # Check don't-touch zones
        for file in files_changed:
            for danger_zone in self.config["dont_touch"]:
                if file.startswith(danger_zone):
                    errors.append(f"File in protected zone: {file}")
        
        return len(errors) == 0, errors
    
    def validate_pr(self, pr_info: dict):
        """Check if PR meets requirements"""
        missing = []
        for req in self.config["pr_requirements"]:
            if req not in pr_info.get("description", ""):
                missing.append(req)
        
        return len(missing) == 0, missing
```

### 4.3 Integrate Into Executor

Update `src/executor/executor.py` to check guardrails before allowing changes:

```python
def execute_improvement(self, repo_path: str, plan: dict):
    checker = GuardrailsChecker("config/guardrails.yaml")
    
    # Simulate the change and check guardrails
    # ... (get proposed diff)
    
    safe, errors = checker.check_diff(diff_lines, files_changed)
    if not safe:
        return {"success": False, "errors": errors}
    
    # If safe, proceed with Claude Code headless call
    # ...
```

**Milestone:** Guardrails are in place. The system can't touch sensitive areas or make massive changes.

---

## Phase 5: Template Library (In Parallel with Phase 4)

### 5.1 Define Template Structure

`src/templates/schema.py`:

```python
from dataclasses import dataclass

@dataclass
class Template:
    id: str  # e.g., "auth_saas_backend"
    name: str
    description: str
    stack: list  # e.g., ["Python", "FastAPI", "PostgreSQL", "Supabase"]
    files: dict  # dict of template files
    preconditions: list  # when to use this template
    validation_commands: list  # how to test it
    dependencies: list  # what to install
    examples: list  # example repos using this pattern
    learning_atoms: list  # relevant KB atom IDs
```

### 5.2 Extract Templates from Real Repos

As you run DevCTO on your own repos and see patterns that work:

1. **Capture successful PRs** as template candidates.
2. **Generalize the structure** (replace specific paths/names with placeholders).
3. **Add metadata** (when to use, preconditions, validation).
4. **Store in `src/templates/library.json`**:

```json
{
  "auth_saas_backend": {
    "name": "Authenticated SaaS Backend",
    "stack": ["Python", "FastAPI", "PostgreSQL", "Supabase"],
    "files": {
      "src/auth/models.py": "... template content ...",
      "src/auth/routes.py": "... template content ..."
    },
    "preconditions": ["python project", "fastapi in deps"],
    "validation": ["pytest", "import src.auth"],
    "learning_atoms": ["fastapi_auth_pattern", "supabase_integration"]
  }
}
```

### 5.3 Test Templates on New Repos

When you create a new app:

1. **Describe requirements** in a spec file.
2. **Have the system match to templates** (which stack, which patterns?).
3. **Assemble templates into a new repo**.
4. **Run validation** to ensure it works.

This is the foundation for Phase 3 (app builder).

**Milestone:** You have 3–5 proven templates in the library.

---

## Phase 6: Spec-Driven App Builder (Future)

### 6.1 Spec Format

Users (you, initially) describe apps as:

```yaml
name: "Analytics Dashboard SaaS"
description: "Multi-tenant analytics platform with auth, API, and dashboards"

requirements:
  - "User authentication with email/password"
  - "Role-based access (admin, viewer, editor)"
  - "REST API for data ingestion"
  - "Interactive dashboards with charts"

constraints:
  - "PostgreSQL backend"
  - "React frontend"
  - "Deployed to Railway"
  - "LangFuse observability"

examples:
  - "https://github.com/example/saas-dashboard"
  - "https://github.com/another/analytics-app"
```

### 6.2 Match Spec to Templates

`src/builder/spec_matcher.py`:

```python
class SpecMatcher:
    def __init__(self, template_library):
        self.templates = template_library
    
    def match_templates(self, spec: dict):
        """Find templates that match the spec"""
        matches = []
        
        for template_id, template in self.templates.items():
            score = self.calculate_fit(spec, template)
            if score > 0.7:
                matches.append((template_id, score, template))
        
        return sorted(matches, key=lambda x: x[1], reverse=True)
    
    def calculate_fit(self, spec: dict, template: dict):
        """Score how well a template fits the spec"""
        # Check stack match, requirements covered, etc.
        score = 0
        if all(tech in template["stack"] for tech in spec.get("stack", [])):
            score += 0.5
        # More scoring logic...
        return score
```

### 6.3 Assemble App from Templates

`src/builder/assembler.py`:

```python
class AppAssembler:
    def __init__(self, spec, matched_templates):
        self.spec = spec
        self.templates = matched_templates
    
    def assemble(self, output_path: str):
        """
        Create a new app repo by combining templates.
        """
        # 1. Create base structure from primary template
        # 2. Layer in secondary templates (auth, observability, etc.)
        # 3. Resolve conflicts and dependencies
        # 4. Populate config files
        # 5. Run validation
        # 6. Generate README and docs
        
        return output_path
```

### 6.4 Validate Generated App

The assembled app must pass:

- **Structure checks**: required files exist.
- **Import tests**: code compiles.
- **Security**: no secrets in configs.
- **Observability**: LangFuse hooks present.
- **Tests**: basic test suite runs.

**Milestone:** You can generate a working app from a spec in ~5 minutes, and it runs on the first or second try.

---

## Phase 7: Continuous Learning and Updates

### 7.1 Daily/Weekly Learning Ingestion

Keep the KB fed with new patterns:

- New blog posts on best practices.
- New GitHub repos with useful patterns.
- Your own successful PRs and learnings.

`scripts/schedule_learning.sh`:

```bash
#!/usr/bin/env bash
# Run nightly learning updates

poetry run python -c "
from agents.research_agent import ResearchAgent

agent = ResearchAgent()
agent.ingest_recent_articles('langfuse', limit=10)
agent.ingest_recent_articles('mcp', limit=10)
agent.ingest_recent_articles('langraph', limit=10)
agent.ingest_github_repos('claude code automation', stars=100, limit=5)
"
```

### 7.2 Template Versioning

As templates evolve:

- Tag versions (v1.0, v1.1, v2.0).
- Track which versions work where.
- Deprecate old patterns when new ones prove better.

`src/templates/versioning.py`:

```python
class TemplateVersionManager:
    def tag_version(self, template_id: str, version: str, notes: str):
        """Tag a template version"""
        pass
    
    def get_stable_version(self, template_id: str):
        """Get the recommended (stable) version"""
        pass
    
    def deprecate(self, template_id: str, version: str, reason: str):
        """Mark a template version as deprecated"""
        pass
```

### 7.3 Feedback Loop: PRs → Learnings

Track which patterns work and which don't:

`src/feedback/stats.py`:

```python
class StatTracker:
    def record_pr_outcome(self, pr_id, pattern_id, merged: bool, reason: str):
        """Log whether a PR succeeded"""
        # Used for learning which patterns work best
        pass
    
    def get_pattern_success_rate(self, pattern_id: str):
        """How often does this pattern lead to merged PRs?"""
        pass
    
    def recommend_patterns(self, context: dict):
        """Suggest patterns most likely to succeed given context"""
        pass
```

**Milestone:** System continuously learns and improves over time.

---

## Implementation Timeline

- **Week 1–2: Learning Phase (Phase 0)**
  - Set up learning spec, ingest sources, build atom library.
  - Goal: KB has solid coverage of Claude headless, MCP, digests, observability.

- **Week 3: Design (Phase 1)**
  - Claude designs the repo structure and architecture.
  - Output: `DEVCTO_REPO_DESIGN.md` approved.

- **Week 4: Skeleton & Core Loop (Phases 2–3)**
  - Create repo, scaffold structure, implement digest → analyze → execute → learn.
  - Goal: `./scripts/run_once.sh` works end-to-end on one test repo.

- **Week 5: Guardrails (Phase 4)**
  - Add safety checks, validate diffs, protect sensitive areas.
  - Goal: System can't accidentally break things.

- **Week 6: Templates (Phase 5)**
  - Extract and test 3–5 templates from successful runs.
  - Goal: You have a library of reusable patterns.

- **Week 7+: App Builder (Phase 6) & Ongoing Learning (Phase 7)**
  - Implement spec → templates → app generation.
  - Set up continuous KB updates.

---

## Key Commands You'll Use

```bash
# Build learning atoms
poetry run python agents/research_agent.py --query "Claude Code headless"

# Run a single DevCTO cycle on your repo
./scripts/run_once.sh /path/to/your/repo

# Ingest a GitHub repo as a pattern
poetry run python -c "
from src.kb_client import client
client.ingest_github_repo('https://github.com/example/repo')
"

# Check what the system learned recently
poetry run python -c "
from src.kb_client import client
atoms = client.search('recently learned', top_k=10)
for atom in atoms:
    print(atom['title'])
"

# Generate an app from a spec
poetry run python -c "
from src.builder.assembler import AppAssembler
spec = load_spec('my_app_spec.yaml')
templates = match_templates(spec)
app = AppAssembler(spec, templates).assemble('./my_new_app')
"
```

---

## Recap: What You're Building

1. **A learning engine** (Agent-Factory KB) that ingests best practices and real patterns.
2. **A DevCTO agent** that uses that KB to analyze and improve your repos with small, safe PRs.
3. **A template library** that captures what works.
4. **An app builder** that eventually generates full applications from specifications, using your template library.

All built by Claude Code, orchestrated by you, and continuously learning.

---

## Success Criteria

**Phase 0 (Learning):** ✓ KB has 50+ atoms covering Claude automation, MCP, observability, and templates.

**Phase 1 (Design):** ✓ DEVCTO_REPO_DESIGN.md is complete and validated.

**Phase 2–3 (Core):** ✓ Run `./scripts/run_once.sh` on Agent-Factory and it:
- Digests the repo
- Analyzes for issues
- Proposes an improvement (e.g., "add tests for orchestrator")
- Creates a branch and commits changes
- Leaves a summary report

**Phase 4 (Guardrails):** ✓ System refuses to touch protected areas and limits diff size.

**Phase 5 (Templates):** ✓ You have 3–5 templates you trust and reuse.

**Phase 6 (App Builder):** ✓ You can generate a working SaaS skeleton from a spec in <10 minutes.

**Phase 7 (Learning):** ✓ System automatically ingests new patterns and improves over time.

---

## Notes for Claude Code

When working on this project:

1. **Always check `docs/learning/DEVCTO_LEARNING_SPEC.md`** for what patterns we've learned.
2. **Query the KB before implementing** – ask "search atoms about X" to see if there's a pattern.
3. **Reference real repos** when designing patterns – link to `examples/` in atoms.
4. **Test after each small change** – don't let broken code accumulate.
5. **Document why you did things** in comments and commit messages.
6. **Keep guardrails strict** – it's better to refuse a change than to break something.
7. **Use `CLAUDE.md` as your north star** – that file defines how to work in this project.

---

**Good luck. Build slow, test often, and let Claude help you all the way.**
