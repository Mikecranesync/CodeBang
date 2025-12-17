# CLAUDE.md

## Cloud Dev Box Quick Start

**On a fresh cloud VM:**

1. **Clone the repos:**
   ```bash
   mkdir ~/repos && cd ~/repos
   git clone <codebang-repo-url> CodeBang
   git clone <agent-factory-repo-url> "Agent Factory"
   ```

2. **One-time setup:**
   ```bash
   cd CodeBang
   ./scripts/setup_vm.sh
   ```

3. **Configure Agent-Factory (if using KB):**
   ```bash
   cd "../Agent Factory"
   cp .env.example .env
   # Edit .env with your API keys (OPENAI_API_KEY, SUPABASE_URL, etc.)
   ```

4. **Start working:**
   ```bash
   cd ~/repos/CodeBang

   # Option 1: Work on CodeBang (DevCTO bootstrap)
   ./scripts/start_claude.sh codebang

   # Option 2: Work on CodeBang with KB API running
   ./scripts/start_claude.sh codebang --with-kb

   # Option 3: Work on Agent-Factory
   ./scripts/start_claude.sh agent-factory
   ```

5. **From laptop/Android:**
   ```bash
   ssh user@your-vm-ip
   cd ~/repos/CodeBang
   ./scripts/start_claude.sh
   ```

---

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**DevCTO Agent** is a self-improving AI DevOps agent that learns best practices, templates, and patterns, then uses that knowledge to maintain codebases and eventually generate complete applications from specifications.

**Target Architecture:** This system follows a digest → analyze → act → learn loop that:
1. Digests codebases into AI-readable summaries
2. Analyzes them against a knowledge base of patterns
3. Executes safe improvements via Claude Code headless mode
4. Learns from PR outcomes to improve future recommendations

## Bootstrapping Rule

**CRITICAL:** Before creating, modifying, or proposing changes to any DevCTO code, you MUST:

1. **Query the Agent-Factory KB** via KBClient for DevCTO atoms
2. **Search for these core atoms:**
   - `devcto_core_loop` - Understand the fundamental workflow
   - `devcto_repo_structure` - Know where code belongs
   - `devcto_guardrails_philosophy` - Understand safety constraints
   - `devcto_kb_integration` - Learn how to use the KB properly
   - `devcto_headless_exec` - Understand execution patterns
3. **Read their summaries and code examples** before proceeding
4. **Reference atom IDs** in commits and PRs for traceability

This ensures all DevCTO work is grounded in proven patterns from the knowledge base, not invented from scratch.

### Quick Bootstrap Query
```python
from src.kb_client.client import KBClient

kb = KBClient(agent_factory_url)
atoms = kb.get_devcto_bootstrap_atoms()  # Returns core DevCTO atoms
for atom in atoms:
    print(f"{atom['id']}: {atom['summary']}")
```

### Atom Source
All DevCTO atoms are derived from `DEVCTO_CLAUDE_ATOMS.md`, which breaks this CLAUDE.md file into 14 discrete learning atoms. When in doubt, consult the atoms rather than guessing implementation details.

## Repository Structure (Planned)

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
└── docs/
    ├── CLAUDE.md
    ├── API_SPEC.md
    └── GUARDRAILS.md
```

## Common Commands

### Development
```bash
# Install dependencies
poetry install

# Run tests
poetry run pytest

# Run single DevCTO cycle on a repo
./scripts/run_once.sh /path/to/your/repo

# Run with specific config
./scripts/run_once.sh /path/to/repo ./config/guardrails.yaml
```

### Testing Individual Components
```bash
# Test digest builder
poetry run pytest tests/test_digest.py

# Test analyzer
poetry run pytest tests/test_analyzer.py

# Test executor
poetry run pytest tests/test_executor.py

# End-to-end test
poetry run pytest tests/test_e2e.py
```

## Key Architectural Concepts

### 1. Knowledge Base Integration
- DevCTO queries an external Agent-Factory knowledge base (KB) for patterns and best practices
- KB client (`src/kb_client/client.py`) handles all API calls to Agent-Factory
- Learning atoms are discrete units of knowledge (patterns, practices, examples)
- Search KB before implementing features to leverage existing patterns

### 2. Safety Guardrails
All changes must pass safety checks defined in `config/guardrails.yaml`:
- **Max diff size:** Limited number of lines changed per PR
- **Protected zones:** Certain directories/files cannot be modified
- **Validation requirements:** Tests must pass, code must have type hints/docstrings
- **Branch naming:** Enforced `devcto/improvement-{id}` pattern
- **PR requirements:** Must include summary, KB atom references, explanations

### 3. Claude Code Headless Execution
The executor module calls Claude Code in headless mode:
- Uses `--allowedTools` to restrict available tools
- Uses `--permission-mode acceptEdits` for automated approval
- Prompts include digest context + improvement plan
- Creates branches, commits changes, generates reports

### 4. Learning Loop
- Tracks PR outcomes (merged vs rejected)
- Updates local patterns based on success/failure
- Continuously queries KB for updated patterns
- Maintains success rate metrics per pattern

## Implementation Phases

This repository is being built in phases as outlined in `DevCTO_Complete_Build_Plan.md`:

- **Phase 0:** Learning foundation (build KB in Agent-Factory)
- **Phase 1:** Design the DevCTO repo structure
- **Phase 2:** Create and scaffold the repository
- **Phase 3:** Implement core digest → analyze → act → learn loop
- **Phase 4:** Add safety guardrails
- **Phase 5:** Build template library
- **Phase 6:** Spec-driven app builder
- **Phase 7:** Continuous learning and updates

## Dependencies

### Required Tools
- **Repomix or Codebase-digest:** For generating repo digests
- **Claude Code CLI:** For headless automation
- **Agent-Factory API:** External knowledge base service

### Python Dependencies (to be added to pyproject.toml)
- requests (for KB API calls)
- pyyaml (for config parsing)
- pytest (for testing)
- subprocess (standard library, for running external commands)

## Working with This Codebase

### Before Implementing Features
1. Check `docs/learning/DEVCTO_LEARNING_SPEC.md` (when it exists) for relevant learned patterns
2. Query the KB via kb_client to see if a pattern exists
3. Reference real repos in examples when designing patterns
4. Keep guardrails strict - refuse changes rather than break things

### When Adding New Features
1. Test after each small change
2. Document reasoning in comments and commit messages
3. Ensure changes pass all validation requirements
4. Update relevant config files if adding new guardrails or patterns

### Template Development
Templates should include:
- Unique ID (e.g., "auth_saas_backend")
- Clear description and use cases
- Stack/technology requirements
- Preconditions for usage
- Validation commands
- Dependencies list
- Example repos using the pattern
- Links to relevant learning atoms

### Guardrails Philosophy
- **Better to refuse than to break:** If uncertain about safety, block the change
- **Small, incremental changes:** Large refactors should be broken into smaller PRs
- **Always validate:** Run tests and checks before committing
- **Respect boundaries:** Never modify protected directories/files

## Integration Points

### Agent-Factory API
The system expects these endpoints:
- `POST /api/kb/search` - Search learning atoms
- `POST /api/kb/atom` - Fetch specific atom
- `POST /api/ingest` - Trigger new source ingestion

### GitHub Integration
- Creates branches following `devcto/improvement-{id}` naming
- Generates PR descriptions with required sections
- Tracks PR outcomes for learning

## Non-Coder Friendly Design

This system is designed for non-technical founders:
- Clear, explanatory PR descriptions
- Mandatory summaries in `DEVCTO_REPORT.md`
- Links to relevant documentation/atoms for context
- Rollback paths documented
- "Don't touch" zones clearly marked
- Auto-approve only for proven safe patterns

## Reference Documentation

For complete implementation details, architectural decisions, and phase-by-phase instructions, see `DevCTO_Complete_Build_Plan.md` (30KB comprehensive guide).
