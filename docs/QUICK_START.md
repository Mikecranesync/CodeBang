# DevCTO Cloud Dev Box - Quick Start

Get up and running in 5 minutes.

---

## Prerequisites

- ✅ Linux VM with SSH access
- ✅ Python 3.7+
- ✅ Claude Code CLI installed
- ✅ GitHub account

---

## First Time Setup (One-Time)

```bash
# 1. SSH into your VM
ssh user@your-vm-ip

# 2. Clone repositories
mkdir ~/repos && cd ~/repos
git clone https://github.com/YOUR_USERNAME/CodeBang.git CodeBang
git clone https://github.com/YOUR_USERNAME/Agent-Factory.git "Agent Factory"

# 3. Run setup script
cd CodeBang
./scripts/setup_vm.sh

# 4. (Optional) Configure KB
cd "../Agent Factory"
cp .env.example .env
nano .env  # Add: OPENAI_API_KEY, SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY
```

**Expected time:** 2-3 minutes

---

## Daily Usage

### Option 1: Work on CodeBang (Default)

```bash
ssh user@your-vm-ip
cd ~/repos/CodeBang
./scripts/start_claude.sh
```

Claude starts with full context from:
- CLAUDE.md
- DEVCTO_CLAUDE_ATOMS.md
- DevCTO_Complete_Build_Plan.md

### Option 2: Work on CodeBang + KB API

```bash
cd ~/repos/CodeBang
./scripts/start_claude.sh codebang --with-kb
```

Automatically starts Agent-Factory KB API before launching Claude.

### Option 3: Work on Agent-Factory

```bash
cd ~/repos/CodeBang
./scripts/start_claude.sh agent-factory
```

---

## Common Commands

```bash
# Get help
./scripts/start_claude.sh --help

# Re-run setup (if needed)
./scripts/setup_vm.sh

# Manually start KB API
./scripts/start_kb_api.sh

# Check KB API status
curl http://localhost:8000/health

# View KB API logs
tail -50 /tmp/kb_api.log
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Claude CLI not found" | Install from https://docs.anthropic.com/claude-code/installation |
| "Agent-Factory not found" | Clone to `~/repos/Agent Factory/` |
| "KB API failed to start" | Check `/tmp/kb_api.log`, verify .env exists |
| "Permission denied" | Run `chmod +x scripts/*.sh` |
| Scripts don't work | Verify directory structure: `~/repos/CodeBang/` and `~/repos/Agent Factory/` |

See [full troubleshooting guide](./TROUBLESHOOTING.md) for more.

---

## What's Next?

1. **Read the full guide:** [CLOUD_DEV_BOX_GUIDE.md](./CLOUD_DEV_BOX_GUIDE.md)
2. **Understand DevCTO architecture:** [../CLAUDE.md](../CLAUDE.md)
3. **Learn about the atoms:** [../DEVCTO_CLAUDE_ATOMS.md](../DEVCTO_CLAUDE_ATOMS.md)
4. **Follow the build plan:** [../DevCTO_Complete_Build_Plan.md](../DevCTO_Complete_Build_Plan.md)

---

## Directory Structure

```
~/repos/
├── CodeBang/
│   ├── scripts/
│   │   ├── setup_vm.sh          ← One-time setup
│   │   ├── start_claude.sh      ← Main launcher
│   │   └── start_kb_api.sh      ← KB API helper
│   ├── docs/
│   │   ├── CLOUD_DEV_BOX_GUIDE.md   ← Full guide
│   │   ├── QUICK_START.md           ← This file
│   │   └── TROUBLESHOOTING.md       ← Troubleshooting
│   ├── CLAUDE.md
│   ├── DEVCTO_CLAUDE_ATOMS.md
│   └── DevCTO_Complete_Build_Plan.md
│
└── Agent Factory/
    ├── agent_factory/
    │   └── api/
    │       └── kb_api.py        ← KB API server
    └── .env                     ← API keys (create this)
```

---

## Quick Reference Card

**Print this out or save to your notes:**

```bash
# === FIRST TIME SETUP ===
ssh user@VM_IP
mkdir ~/repos && cd ~/repos
git clone <codebang-url> CodeBang
git clone <agent-factory-url> "Agent Factory"
cd CodeBang && ./scripts/setup_vm.sh

# === DAILY USAGE ===
ssh user@VM_IP
cd ~/repos/CodeBang

# Basic
./scripts/start_claude.sh

# With KB
./scripts/start_claude.sh codebang --with-kb

# Agent-Factory
./scripts/start_claude.sh agent-factory

# === TROUBLESHOOTING ===
# Logs:        tail -50 /tmp/kb_api.log
# API status:  curl localhost:8000/health
# Re-setup:    ./scripts/setup_vm.sh
# Help:        ./scripts/start_claude.sh --help
```

---

**Version:** 1.0
**Last Updated:** 2025-12-16

For detailed documentation, see [CLOUD_DEV_BOX_GUIDE.md](./CLOUD_DEV_BOX_GUIDE.md)
