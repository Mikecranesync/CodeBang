# DevCTO CLAUDE.md Atoms

This document breaks down CLAUDE.md into discrete learning atoms for ingestion into the Agent-Factory knowledge base.

---

## Atom: devcto_project_overview

**Source:** CLAUDE.md / Project Overview
**Summary:** DevCTO Agent is a self-improving AI DevOps system that learns best practices, templates, and patterns to maintain codebases and generate applications from specifications. Uses a digest → analyze → act → learn loop.

**When to use:**
- When explaining DevCTO to new developers or agents
- When creating initial repo documentation
- When planning DevCTO integrations with other systems

**Key concepts:**
- Self-improving system that learns from outcomes
- Targets non-technical founders as primary users
- Builds on knowledge base of proven patterns
- Eventually generates complete applications from specs

**Related atoms:** `devcto_core_loop`, `devcto_kb_integration`, `devcto_non_coder_safety`

---

## Atom: devcto_core_loop

**Source:** CLAUDE.md / Key Architectural Concepts
**Summary:** The fundamental DevCTO workflow: (1) Digest - analyze repos into AI-readable summaries, (2) Analyze - compare against KB patterns, (3) Act - execute safe improvements via headless Claude Code, (4) Learn - track PR outcomes to improve recommendations.

**When to use:**
- When implementing orchestrator logic
- When explaining DevCTO's workflow
- When debugging why DevCTO made certain decisions
- When adding new phases to the loop

**Code pattern:**
```python
class Orchestrator:
    def run_once(self, repo_path: str):
        digest = self.digest_builder.build_repo_digest(repo_path)
        analysis = self.analyzer.analyze_digest(digest, context)
        result = self.executor.execute_improvement(repo_path, analysis)
        if result["success"]:
            self.learner.process_pr_outcome(result)
```

**Implementation notes:**
- Each phase should be independently testable
- Phases communicate via structured dicts
- Failed phases should not crash the loop
- All phases log to observability system

**Related atoms:** `devcto_digest_tools`, `devcto_analyzer_pattern`, `devcto_headless_exec`, `devcto_learning_loop`

---

## Atom: devcto_repo_structure

**Source:** CLAUDE.md / Repository Structure
**Summary:** Fixed directory layout for DevCTO: `src/` contains orchestrator, kb_client, digest, analyzer, executor, feedback, and templates modules. `config/` holds guardrails, patterns, and integrations. `scripts/` provides automation. `tests/` mirrors src structure.

**When to use:**
- When scaffolding new DevCTO installations
- When deciding where new code belongs
- When reviewing PRs for proper file placement
- When documenting architecture

**Directory responsibilities:**
- `src/orchestrator/` - Main loop coordination
- `src/kb_client/` - Agent-Factory API calls
- `src/digest/` - Repo analysis (Repomix/Codebase-digest)
- `src/analyzer/` - Claude-powered analysis
- `src/executor/` - Claude Code headless execution
- `src/feedback/` - PR outcome tracking
- `src/templates/` - Template storage and versioning

**Validation:**
```bash
# Structure should support these tests
pytest tests/test_digest.py
pytest tests/test_analyzer.py
pytest tests/test_executor.py
pytest tests/test_e2e.py
```

**Related atoms:** `devcto_project_overview`, `devcto_core_loop`

---

## Atom: devcto_kb_integration

**Source:** CLAUDE.md / Key Architectural Concepts #1
**Summary:** DevCTO queries external Agent-Factory KB for patterns and best practices. KB client handles API calls. Learning atoms are discrete knowledge units. Always search KB before implementing to leverage existing patterns.

**When to use:**
- When implementing features that might have existing patterns
- When analyzer needs to fetch relevant patterns
- When learning new successful patterns
- When validating proposed changes against known practices

**API endpoints required:**
- `POST /api/kb/search` - Search learning atoms by query
- `POST /api/kb/atom` - Fetch specific atom by ID
- `POST /api/ingest` - Trigger ingestion of new sources

**Code pattern:**
```python
class KBClient:
    def search(self, query: str, top_k: int = 5):
        resp = requests.post(
            f"{self.base_url}/api/kb/search",
            json={"query": query, "top_k": top_k}
        )
        return resp.json()["atoms"]
```

**Best practices:**
- Cache KB responses to reduce API calls
- Namespace atoms (e.g., "devcto_*", "langfuse_*")
- Include atom IDs in PR descriptions for traceability
- Update KB when patterns prove successful

**Related atoms:** `devcto_learning_loop`, `devcto_analyzer_pattern`

---

## Atom: devcto_guardrails_philosophy

**Source:** CLAUDE.md / Key Architectural Concepts #2
**Summary:** All DevCTO changes must pass safety checks: max diff size, protected zones, validation requirements, branch naming, PR requirements. Philosophy: refuse changes rather than break things, prefer small incremental changes, always validate, respect boundaries.

**When to use:**
- When implementing executor logic
- When reviewing proposed changes
- When configuring new DevCTO installations
- When explaining safety to non-technical users

**Guardrails categories:**
1. **Size limits** - Max lines changed, max files modified
2. **Protected zones** - Directories/files that cannot be touched
3. **Validation** - Tests must pass, type hints required, docstrings required
4. **Naming** - Enforced branch patterns (devcto/improvement-{id})
5. **Documentation** - PR must explain changes and link to atoms

**Config example:**
```yaml
safety:
  max_diff_lines: 300
  max_files_changed: 10
dont_touch:
  - "infra/production"
  - "src/payments"
  - ".env*"
required_before_commit:
  - "pytest passes"
  - "code is type-hinted"
```

**Implementation pattern:**
```python
class GuardrailsChecker:
    def check_diff(self, diff_lines, files_changed):
        errors = []
        if len(diff_lines) > self.config["safety"]["max_diff_lines"]:
            errors.append(f"Diff too large")
        # Check protected zones, validation, etc.
        return len(errors) == 0, errors
```

**Related atoms:** `devcto_non_coder_safety`, `devcto_executor_pattern`

---

## Atom: devcto_headless_exec

**Source:** CLAUDE.md / Key Architectural Concepts #3
**Summary:** DevCTO calls Claude Code in non-interactive headless mode with restricted tools, automated approval, structured prompts including digest + plan. Creates branches, commits changes, generates reports.

**When to use:**
- When implementing executor module
- When debugging why changes weren't applied
- When designing improvement prompts
- When setting up CI/CD integration

**Headless invocation pattern:**
```python
subprocess.run([
    "claude",
    "-p", prompt,
    "--allowedTools", "Bash,Read,Edit",
    "--permission-mode", "acceptEdits"
], cwd=repo_path, capture_output=True)
```

**Prompt structure:**
```
Here is a repo digest and improvement plan.

Digest: {digest_summary}
Plan: {specific_improvements}

Steps:
1. Create branch: git checkout -b devcto/improvement-{id}
2. Apply improvement (add tests, fix structure, etc.)
3. Run validation: pytest
4. Commit and push
5. Create report: .devcto/last_run.md
```

**Safety considerations:**
- Restrict allowed tools to minimum needed
- Always validate before commit
- Capture stdout/stderr for debugging
- Set timeouts to prevent runaway execution
- Never use in production without guardrails

**Related atoms:** `devcto_executor_pattern`, `devcto_guardrails_philosophy`

---

## Atom: devcto_learning_loop

**Source:** CLAUDE.md / Key Architectural Concepts #4
**Summary:** DevCTO tracks PR outcomes (merged vs rejected), updates local patterns based on success/failure, continuously queries KB for updated patterns, maintains success rate metrics per pattern.

**When to use:**
- When implementing feedback module
- When analyzing which patterns work best
- When deciding whether to apply a pattern
- When reporting DevCTO effectiveness

**Learning workflow:**
1. PR created with pattern_id tag
2. Track PR state (merged, rejected, reason)
3. Log outcome to feedback system
4. Update pattern success rates
5. Query KB for refined patterns
6. Update local patterns.yaml

**Code pattern:**
```python
class Learner:
    def process_pr_outcome(self, pr_info: dict):
        if pr_info["merged"]:
            self.log_success(pr_info["pattern_id"], pr_info["changes"])
        else:
            self.log_rejection(pr_info["pattern_id"], pr_info["reason"])

    def update_local_patterns(self):
        updated = self.kb.search("learned patterns", top_k=20)
        self.write_patterns_yaml(updated)
```

**Metrics to track:**
- Pattern success rate (merged PRs / total PRs)
- Average time to merge
- Common rejection reasons
- Most effective patterns by repo type

**Related atoms:** `devcto_kb_integration`, `devcto_core_loop`, `devcto_pattern_versioning`

---

## Atom: devcto_digest_tools

**Source:** CLAUDE.md / Dependencies
**Summary:** DevCTO uses Repomix or Codebase-digest to generate AI-readable repo summaries including file tree, metrics, hotspots, and summary. Digest is foundation for analysis phase.

**When to use:**
- When implementing digest module
- When debugging poor analysis quality
- When choosing between digest tools
- When customizing digest output

**Tool options:**
- **Repomix** - Comprehensive, includes metrics
- **Codebase-digest** - Fast, lightweight

**Digest structure:**
```python
{
    "tree": "file_structure_tree",
    "metrics": {
        "total_files": 150,
        "total_lines": 12000,
        "languages": {"Python": 80, "YAML": 20}
    },
    "hotspots": ["src/executor/executor.py", "config/guardrails.yaml"],
    "summary": "FastAPI backend with 15 modules..."
}
```

**Implementation:**
```python
subprocess.run(
    ["npx", "codebase-digest@latest"],
    cwd=repo_path,
    capture_output=True
)
```

**Related atoms:** `devcto_core_loop`, `devcto_analyzer_pattern`

---

## Atom: devcto_analyzer_pattern

**Source:** CLAUDE.md / Key Architectural Concepts #1
**Summary:** Analyzer queries KB for relevant patterns, uses Claude to compare digest against patterns, identifies issues and missing patterns, suggests improvements with confidence scores.

**When to use:**
- When implementing analyzer module
- When improving analysis quality
- When adding new analysis heuristics
- When debugging why certain issues weren't detected

**Analysis workflow:**
1. Receive digest from digest phase
2. Search KB for patterns matching repo context
3. Call Claude with digest + patterns
4. Extract issues, gaps, opportunities
5. Rank suggestions by confidence/impact
6. Return structured analysis

**Code pattern:**
```python
class AnalyzerAgent:
    def analyze_digest(self, digest: dict, repo_context: dict):
        patterns = self.kb.search("code quality patterns", top_k=10)

        # Call Claude to analyze
        analysis = self.call_claude_with_context(digest, patterns)

        return {
            "issues": analysis["identified_issues"],
            "patterns_available": patterns,
            "next_steps": analysis["recommended_improvements"],
            "confidence": analysis["confidence_scores"]
        }
```

**Output structure:**
```python
{
    "issues": ["missing tests", "weak observability"],
    "patterns_available": [atom1, atom2, ...],
    "next_steps": [
        {"action": "add_langfuse_hooks", "confidence": 0.9},
        {"action": "add_unit_tests", "confidence": 0.85}
    ]
}
```

**Related atoms:** `devcto_kb_integration`, `devcto_core_loop`

---

## Atom: devcto_executor_pattern

**Source:** CLAUDE.md / Key Architectural Concepts #3
**Summary:** Executor validates plans against guardrails, calls headless Claude Code, creates branches, commits changes, runs validation, reports outcomes.

**When to use:**
- When implementing executor module
- When debugging failed executions
- When adding new validation steps
- When customizing PR creation

**Execution workflow:**
1. Receive improvement plan from analyzer
2. Check guardrails (diff size, protected zones)
3. If safe, construct Claude Code prompt
4. Execute headless with restricted tools
5. Validate results (tests pass, etc.)
6. Create branch and commit
7. Generate report with summary
8. Return success/failure status

**Safety checks before execution:**
```python
def execute_improvement(self, repo_path: str, plan: dict):
    checker = GuardrailsChecker("config/guardrails.yaml")
    safe, errors = checker.check_diff(plan["diff"], plan["files"])

    if not safe:
        return {"success": False, "errors": errors}

    # Proceed with headless execution
```

**Report format (.devcto/last_run.md):**
```markdown
# DevCTO Run Report

**Date:** 2025-01-15
**Pattern:** add_unit_tests
**Files Changed:** 3
**Lines Changed:** 127

## Changes Made
- Added tests for orchestrator.py
- Added tests for kb_client.py
- Updated test fixtures

## Validation
- ✓ pytest passes
- ✓ Type hints present
- ✓ Under 300 line limit

## KB Atoms Used
- testing_best_practices
- pytest_patterns
```

**Related atoms:** `devcto_guardrails_philosophy`, `devcto_headless_exec`

---

## Atom: devcto_non_coder_safety

**Source:** CLAUDE.md / Non-Coder Friendly Design
**Summary:** DevCTO is designed for non-technical founders with clear PR descriptions, mandatory summaries, documentation links, rollback paths, marked "don't touch" zones, auto-approve only for proven patterns.

**When to use:**
- When explaining DevCTO to non-technical stakeholders
- When designing PR templates
- When configuring guardrails for new users
- When writing documentation

**Safety features for non-coders:**
1. **Clear explanations** - Every PR explains what, why, how
2. **Mandatory summaries** - `DEVCTO_REPORT.md` in every PR
3. **Context links** - References to KB atoms and docs
4. **Rollback documented** - How to revert if needed
5. **Visual boundaries** - Protected zones clearly marked
6. **Conservative defaults** - Auto-approve only proven safe changes

**PR description template:**
```markdown
## Summary
Brief explanation of changes in plain language

## What Changed
- File 1: Added X
- File 2: Updated Y

## Why
This addresses [issue] using pattern [atom_id]

## Validation
- ✓ Tests pass
- ✓ No protected files touched
- ✓ Under size limits

## Rollback
To revert: git revert [commit-sha]

## Learn More
- KB Atom: testing_best_practices
- Docs: docs/testing.md
```

**Auto-approve criteria:**
```yaml
auto_approve_patterns:
  - "add_tests_for_function"
  - "type_hints_missing_module"
  - "add_logging_pattern"

manual_approval_required:
  - "database_migrations"
  - "api_signature_changes"
  - "security_related"
```

**Related atoms:** `devcto_guardrails_philosophy`, `devcto_executor_pattern`

---

## Atom: devcto_template_structure

**Source:** CLAUDE.md / Working with This Codebase / Template Development
**Summary:** DevCTO templates include unique ID, description, stack requirements, preconditions, validation commands, dependencies, example repos, KB atom links. Templates are versioned and tracked for success rates.

**When to use:**
- When creating new templates
- When evaluating template quality
- When choosing templates for app generation
- When documenting patterns

**Template schema:**
```python
@dataclass
class Template:
    id: str  # e.g., "auth_saas_backend"
    name: str
    description: str
    stack: list  # ["Python", "FastAPI", "PostgreSQL"]
    files: dict  # {path: content}
    preconditions: list  # When to use
    validation_commands: list  # How to test
    dependencies: list  # What to install
    examples: list  # Example repos
    learning_atoms: list  # Relevant atom IDs
```

**Template example:**
```json
{
  "auth_saas_backend": {
    "name": "Authenticated SaaS Backend",
    "stack": ["Python", "FastAPI", "PostgreSQL", "Supabase"],
    "preconditions": ["python project", "fastapi in deps"],
    "validation": ["pytest", "import src.auth"],
    "learning_atoms": ["fastapi_auth_pattern", "supabase_integration"]
  }
}
```

**Quality criteria:**
- Proven in at least 2 real projects
- Validation commands pass consistently
- Clear preconditions (when to use / not use)
- Documented dependencies
- Links to working examples

**Related atoms:** `devcto_learning_loop`, `devcto_pattern_versioning`

---

## Atom: devcto_pattern_versioning

**Source:** CLAUDE.md (inferred from build plan)
**Summary:** Templates and patterns are versioned (v1.0, v1.1, v2.0), tracked for effectiveness, deprecated when better patterns emerge. Maintains stable version recommendations.

**When to use:**
- When updating existing templates
- When deprecating old patterns
- When choosing which template version to use
- When tracking pattern evolution

**Versioning workflow:**
1. Create template v1.0
2. Use in projects, track success rate
3. Identify improvements → v1.1
4. Test v1.1, compare to v1.0
5. If v1.1 proves better, mark v1.0 deprecated
6. Update recommended version

**Code pattern:**
```python
class TemplateVersionManager:
    def tag_version(self, template_id: str, version: str, notes: str):
        """Tag a template version with changelog"""

    def get_stable_version(self, template_id: str):
        """Get recommended version"""

    def deprecate(self, template_id: str, version: str, reason: str):
        """Mark version as deprecated"""
```

**Version metadata:**
```yaml
auth_saas_backend:
  stable: v2.1
  versions:
    v2.1:
      success_rate: 0.92
      usage_count: 15
      notes: "Added role-based access"
    v2.0:
      success_rate: 0.87
      usage_count: 23
      deprecated: true
      reason: "v2.1 has better RBAC"
```

**Related atoms:** `devcto_template_structure`, `devcto_learning_loop`

---

## Atom: devcto_implementation_phases

**Source:** CLAUDE.md / Implementation Phases
**Summary:** DevCTO is built in 7 phases: (0) Learning foundation, (1) Design, (2) Scaffold, (3) Core loop, (4) Guardrails, (5) Templates, (6) App builder, (7) Continuous learning. Each phase has clear milestones.

**When to use:**
- When planning DevCTO development
- When tracking project progress
- When explaining DevCTO evolution
- When onboarding new contributors

**Phase summary:**
- **Phase 0:** Build KB in Agent-Factory with core patterns
- **Phase 1:** Design DevCTO repo structure and architecture
- **Phase 2:** Create skeleton repository with basic structure
- **Phase 3:** Implement digest → analyze → act → learn loop
- **Phase 4:** Add safety guardrails and validation
- **Phase 5:** Build reusable template library
- **Phase 6:** Spec-driven app generation
- **Phase 7:** Continuous KB updates and pattern evolution

**Current phase indicators:**
```python
# Check what's implemented
has_kb_client = os.path.exists("src/kb_client/client.py")
has_orchestrator = os.path.exists("src/orchestrator/orchestrator.py")
has_guardrails = os.path.exists("config/guardrails.yaml")
has_templates = os.path.exists("src/templates/library.json")
```

**Milestone validation:**
- Phase 3: `./scripts/run_once.sh` works end-to-end
- Phase 4: Guardrails block unsafe changes
- Phase 5: 3-5 proven templates in library
- Phase 6: Generate working app from spec

**Related atoms:** `devcto_project_overview`, `devcto_repo_structure`

---

## Summary

These 14 atoms capture the core knowledge from CLAUDE.md:

1. **devcto_project_overview** - What DevCTO is
2. **devcto_core_loop** - How it works
3. **devcto_repo_structure** - Where code lives
4. **devcto_kb_integration** - How it learns
5. **devcto_guardrails_philosophy** - How it stays safe
6. **devcto_headless_exec** - How it executes changes
7. **devcto_learning_loop** - How it improves
8. **devcto_digest_tools** - How it analyzes repos
9. **devcto_analyzer_pattern** - How it identifies issues
10. **devcto_executor_pattern** - How it applies fixes
11. **devcto_non_coder_safety** - How it serves non-technical users
12. **devcto_template_structure** - How it stores patterns
13. **devcto_pattern_versioning** - How patterns evolve
14. **devcto_implementation_phases** - How to build it

Each atom includes: source, summary, when to use, code examples, and related atoms for navigation.
