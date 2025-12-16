# DevCTO Agent 🤖

> A self-improving AI DevOps system that learns best practices, maintains codebases, and generates applications from specifications.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub Stars](https://img.shields.io/github/stars/Mikecranesync/CodeBang?style=social)](https://github.com/Mikecranesync/CodeBang)

---

## 🎯 What is DevCTO Agent?

DevCTO Agent is an autonomous AI system that acts as your DevOps CTO. It:

- **📊 Digests** codebases into AI-readable summaries
- **🔍 Analyzes** them against a knowledge base of proven patterns
- **⚡ Executes** safe improvements via Claude Code headless mode
- **🧠 Learns** from PR outcomes to continuously improve

**Target Users:** Non-technical founders who want an AI partner that maintains their code, suggests improvements, and eventually generates complete applications from specifications.

---

## 🏗️ Architecture: The Core Loop

```
┌─────────────────────────────────────────────────────────────┐
│                     DevCTO Core Loop                        │
└─────────────────────────────────────────────────────────────┘

   1. DIGEST                    2. ANALYZE
   ┌──────────────┐            ┌──────────────┐
   │  Repo        │            │  Compare vs  │
   │  Analysis    │───────────▶│  KB Patterns │
   │  (Repomix)   │            │  (Claude)    │
   └──────────────┘            └──────────────┘
         │                            │
         │                            ▼
         │                     3. ACT
         │                    ┌──────────────┐
         │                    │  Execute     │
         │                    │  Safe        │
         │                    │  Changes     │
         │                    └──────────────┘
         │                            │
         │                            ▼
         │                     4. LEARN
         │                    ┌──────────────┐
         └───────────────────▶│  Track PR    │
                              │  Outcomes    │
                              └──────────────┘
```

---

## 🔑 Key Innovation: KB-First Architecture

DevCTO **doesn't invent architecture** - it consults a knowledge base of proven patterns before making any changes.

### The Bootstrapping Rule

Before creating or modifying any code, DevCTO:

1. **Queries the Agent-Factory KB** for relevant atoms
2. **Reads proven patterns** (e.g., `devcto_core_loop`, `devcto_guardrails_philosophy`)
3. **Applies those patterns** instead of guessing
4. **References atom IDs** in commits for traceability

This ensures:
- ✅ **No reinventing the wheel** - reuse what works
- ✅ **Consistency** - all instances use the same patterns
- ✅ **Traceability** - know where every decision came from
- ✅ **Continuous improvement** - update atoms, improve all future work

---

## 📚 The 14 Learning Atoms

DevCTO's knowledge is broken into discrete atoms (namespace: `devcto_`):

| Atom | Purpose |
|------|---------|
| **project_overview** | What DevCTO is and why it exists |
| **core_loop** | The digest → analyze → act → learn workflow |
| **repo_structure** | Where code lives and why |
| **kb_integration** | How to query and use the knowledge base |
| **guardrails_philosophy** | Safety principles and limits |
| **headless_exec** | Running Claude Code non-interactively |
| **learning_loop** | How DevCTO improves from PR outcomes |
| **digest_tools** | Using Repomix/Codebase-digest |
| **analyzer_pattern** | How to analyze repos against patterns |
| **executor_pattern** | How to safely execute improvements |
| **non_coder_safety** | Design for non-technical users |
| **template_structure** | How to define reusable templates |
| **pattern_versioning** | How patterns evolve over time |
| **implementation_phases** | The 7-phase build roadmap |

See [DEVCTO_CLAUDE_ATOMS.md](DEVCTO_CLAUDE_ATOMS.md) for complete details.

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- [Claude Code CLI](https://claude.ai/code)
- Access to Agent-Factory knowledge base (or set one up)
- Git

### Setup

```bash
# Clone the repository
git clone https://github.com/Mikecranesync/CodeBang.git
cd CodeBang

# Read the guidance files
cat CLAUDE.md              # Architecture and patterns
cat NEXT_STEPS.md          # What to do next
cat DevCTO_Complete_Build_Plan.md  # Full 7-phase plan
```

### Current Phase: Phase 0-1 (Bootstrap)

This repository contains the **foundation** for DevCTO. The actual implementation happens in phases:

- ✅ **Phase 0:** Learning foundation (atoms created)
- ✅ **Phase 1:** Repository design (architecture documented)
- 🔄 **Phase 2:** Scaffold the DevCTO repo ← **YOU ARE HERE**
- ⏳ **Phase 3:** Implement core loop
- ⏳ **Phase 4:** Add safety guardrails
- ⏳ **Phase 5:** Build template library
- ⏳ **Phase 6:** Spec-driven app builder
- ⏳ **Phase 7:** Continuous learning

---

## 📂 Repository Structure

```
CodeBang/
├── CLAUDE.md                      # Instructions for Claude Code instances
├── DEVCTO_CLAUDE_ATOMS.md        # 14 learning atoms for KB ingestion
├── DevCTO_Complete_Build_Plan.md # Comprehensive 7-phase implementation guide
├── NEXT_STEPS.md                  # Your action plan (start here!)
├── kb_client_example.py           # Reference KB client implementation
└── README.md                      # You are here
```

### Future Structure (Phase 2+)

Once scaffolded, the repo will have:

```
devcto-agent/
├── src/
│   ├── orchestrator/        # Main loop coordination
│   ├── kb_client/           # Agent-Factory KB integration
│   ├── digest/              # Repo analysis
│   ├── analyzer/            # Pattern matching
│   ├── executor/            # Safe change execution
│   ├── feedback/            # Learning from outcomes
│   └── templates/           # Reusable patterns
├── config/
│   ├── guardrails.yaml      # Safety rules
│   ├── patterns.yaml        # Known patterns
│   └── integrations.yaml    # API endpoints
├── scripts/
│   └── run_once.sh          # Single DevCTO cycle
└── tests/                   # Full test suite
```

---

## 🛡️ Safety Guardrails

DevCTO is designed to be **safe for non-technical users**:

- **Diff limits:** Max 300 lines changed per PR
- **Protected zones:** Never touches payment code, secrets, production infra
- **Validation required:** Tests must pass before commit
- **Branch naming:** All changes in `devcto/improvement-{id}` branches
- **Clear explanations:** Every PR explains what, why, and how to rollback
- **Auto-approve whitelist:** Only proven-safe patterns run automatically

See [CLAUDE.md](CLAUDE.md) for complete guardrails philosophy.

---

## 🔧 How It Works

### 1. Digest Phase

Uses Repomix or Codebase-digest to create an AI-readable summary:

```python
digest = DigestBuilder().build_repo_digest("/path/to/repo")
# Returns: file tree, metrics, hotspots, summary
```

### 2. Analyze Phase

Queries the KB for relevant patterns and uses Claude to identify improvements:

```python
patterns = kb_client.search("code quality patterns", top_k=10)
analysis = analyzer.analyze_digest(digest, patterns)
# Returns: issues found, recommended improvements
```

### 3. Execute Phase

Runs Claude Code headless with strict guardrails:

```bash
claude -p "Improvement plan: ..." \
  --allowedTools "Bash,Read,Edit" \
  --permission-mode "acceptEdits"
```

### 4. Learn Phase

Tracks PR outcomes to improve future recommendations:

```python
if pr_merged:
    learner.log_success(pattern_id, changes)
else:
    learner.log_rejection(pattern_id, reason)
```

---

## 📖 Documentation

| File | Purpose |
|------|---------|
| [CLAUDE.md](CLAUDE.md) | Complete architecture and guidance for Claude Code |
| [DEVCTO_CLAUDE_ATOMS.md](DEVCTO_CLAUDE_ATOMS.md) | 14 learning atoms with code examples |
| [DevCTO_Complete_Build_Plan.md](DevCTO_Complete_Build_Plan.md) | Detailed 7-phase implementation guide |
| [NEXT_STEPS.md](NEXT_STEPS.md) | Your immediate action plan |
| [kb_client_example.py](kb_client_example.py) | Reference KB client implementation |

---

## 🎯 Next Steps

Ready to build? Follow this path:

### 1. Ingest Atoms into Agent-Factory KB

```bash
# Copy atoms to Agent-Factory
cp DEVCTO_CLAUDE_ATOMS.md /path/to/Agent-Factory/docs/learning/

# Ingest into KB
cd /path/to/Agent-Factory
poetry run python agents/atom_builder.py \
  --source "docs/learning/DEVCTO_CLAUDE_ATOMS.md" \
  --namespace "devcto"
```

### 2. Expose KB API Endpoints

Start Agent-Factory API server:

```bash
cd /path/to/Agent-Factory
poetry run uvicorn app:app --port 8000
```

Test it:
```bash
curl http://localhost:8000/api/kb/search \
  -H "Content-Type: application/json" \
  -d '{"query": "devcto_core_loop", "top_k": 1}'
```

### 3. Start Building DevCTO

```bash
# In this repository
claude

# Tell Claude:
# "Read CLAUDE.md and NEXT_STEPS.md, then start Phase 2:
#  scaffold the DevCTO repository structure using the atoms
#  from the knowledge base as your guide."
```

See [NEXT_STEPS.md](NEXT_STEPS.md) for complete details.

---

## 🤝 Contributing

This is a bootstrapping repository. Contributions should:

1. **Consult the KB first** - query relevant atoms before proposing changes
2. **Reference atom IDs** - cite which atoms guided your decisions
3. **Update atoms** - if you discover better patterns, update the atoms
4. **Follow guardrails** - respect the safety boundaries

---

## 📊 Success Metrics

DevCTO is successful when:

- ✅ **Phase 3:** `./scripts/run_once.sh` works end-to-end on a test repo
- ✅ **Phase 4:** System refuses unsafe changes (protected zones, diff limits)
- ✅ **Phase 5:** You have 3-5 proven templates in the library
- ✅ **Phase 6:** You can generate a working app from a spec in <10 minutes
- ✅ **Phase 7:** System continuously learns and improves over time

---

## 🔗 Related Projects

- **Agent-Factory** - The knowledge base and ingestion pipeline
- **Claude Code** - The AI pair programmer powering execution
- **Repomix / Codebase-digest** - Tools for repo analysis

---

## 📝 License

MIT License - see LICENSE file for details

---

## 🙏 Acknowledgments

Built with:
- [Claude Code](https://claude.ai/code) by Anthropic
- [Claude Sonnet 4.5](https://www.anthropic.com/claude) - The AI powering DevCTO
- Knowledge Base architecture inspired by modern RAG patterns

---

## 💬 Questions?

1. **Read the atoms:** [DEVCTO_CLAUDE_ATOMS.md](DEVCTO_CLAUDE_ATOMS.md)
2. **Check the plan:** [DevCTO_Complete_Build_Plan.md](DevCTO_Complete_Build_Plan.md)
3. **Follow next steps:** [NEXT_STEPS.md](NEXT_STEPS.md)
4. **Open an issue:** [GitHub Issues](https://github.com/Mikecranesync/CodeBang/issues)

---

**The system is designed to teach itself - let the atoms guide you.** 🚀

---

<div align="center">

**[⭐ Star this repo](https://github.com/Mikecranesync/CodeBang)** if you believe in self-improving AI systems!

Made with 🤖 by [Claude Code](https://claude.ai/code)

</div>
