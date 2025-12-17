# Cloud Dev Box User Guide

Complete guide to setting up and using the DevCTO cloud development environment.

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [First-Time Setup](#first-time-setup)
4. [Daily Usage](#daily-usage)
5. [Script Reference](#script-reference)
6. [Troubleshooting](#troubleshooting)
7. [Advanced Usage](#advanced-usage)

---

## Overview

The DevCTO cloud dev box allows you to work on DevCTO and Agent-Factory from anywhere via SSH:

- **From your laptop:** SSH into the VM and run Claude Code
- **From your Android phone:** Use Termux or JuiceSSH to work on the go
- **Minimal setup:** Run 1-2 commands to get started
- **Full context:** Claude automatically sees all DevCTO documentation and atoms

**Architecture:**
```
Your Device (Laptop/Android)
    │
    └─ SSH ──────────────> Cloud VM (Linux)
                                │
                      ┌─────────┴─────────┐
                      │                   │
                 CodeBang            Agent-Factory
                      │                   │
                 scripts/            KB API (optional)
                      │
              start_claude.sh ──> Launches Claude Code
```

---

## Prerequisites

### What You Need

1. **Cloud VM** (any provider):
   - Linux OS (Ubuntu 20.04+ recommended)
   - At least 2GB RAM
   - SSH access enabled
   - Bash shell
   - Python 3.7+ installed

2. **On Your Local Machine:**
   - SSH client (built into Linux/Mac, use PuTTY on Windows)
   - Git (for cloning repos)

3. **Accounts/Keys:**
   - GitHub account (to clone repos)
   - Anthropic API key (for Claude Code)
   - OpenAI API key (if using KB features)
   - Supabase credentials (if using KB features)

### Recommended VM Providers

- **Free Tier Options:**
  - Google Cloud (free tier: 1 f1-micro instance)
  - AWS (free tier: 1 t2.micro for 12 months)
  - Oracle Cloud (always free: 2 micro instances)

- **Paid Options:**
  - DigitalOcean ($5/month for basic droplet)
  - Linode ($5/month)
  - Vultr ($5/month)

---

## First-Time Setup

### Step 1: Provision Your VM

1. **Create a VM** on your chosen provider
2. **Configure SSH access:**
   ```bash
   # On your local machine, create SSH key if you don't have one
   ssh-keygen -t ed25519 -C "your_email@example.com"

   # Copy your public key to the VM
   ssh-copy-id user@your-vm-ip
   ```

3. **Test SSH connection:**
   ```bash
   ssh user@your-vm-ip
   # If successful, you should see the VM shell
   ```

### Step 2: Install Claude Code CLI on VM

```bash
# SSH into your VM
ssh user@your-vm-ip

# Install Claude Code CLI (follow official docs)
# Visit: https://docs.anthropic.com/claude-code/installation

# Verify installation
claude --version
```

### Step 3: Clone Repositories

```bash
# Create repos directory
mkdir -p ~/repos && cd ~/repos

# Clone CodeBang
git clone https://github.com/YOUR_USERNAME/CodeBang.git CodeBang

# Clone Agent-Factory
git clone https://github.com/YOUR_USERNAME/Agent-Factory.git "Agent Factory"

# Verify
ls -la
# Should see: CodeBang/ and Agent Factory/
```

### Step 4: Run One-Time Setup

```bash
cd ~/repos/CodeBang
./scripts/setup_vm.sh
```

**What this does:**
- ✅ Checks Claude Code CLI installation
- ✅ Installs Python dependencies (python-dotenv, openai, requests, pyyaml)
- ✅ Verifies Agent-Factory .env configuration
- ✅ Shows next steps

**Expected output:**
```
=========================================
DevCTO Cloud Dev Box - VM Setup
=========================================

[1/3] Checking Claude Code CLI...
  ✅ Claude Code CLI installed
     Claude Code v1.x.x

[2/3] Installing Python dependencies...
  ✅ Python dependencies installed:
     - python-dotenv (environment variables)
     - openai (embeddings generation)
     - requests (HTTP client)
     - pyyaml (config parsing)

[3/3] Checking Agent-Factory configuration...
  ⚠️  Agent-Factory .env not found

  To use Knowledge Base features, create .env:
     cd '../Agent Factory'
     cp .env.example .env
     # Edit .env with your API keys

=========================================
✅ Setup Complete!
=========================================
```

### Step 5: Configure Environment (Optional)

**If you want to use Knowledge Base features:**

```bash
cd ~/repos/"Agent Factory"

# Copy example .env
cp .env.example .env

# Edit with your API keys
nano .env

# Add these keys:
# OPENAI_API_KEY=sk-proj-...
# SUPABASE_URL=https://....supabase.co
# SUPABASE_SERVICE_ROLE_KEY=...
```

**If you're only working on CodeBang without KB:**
- Skip this step
- The scripts will work fine without it

---

## Daily Usage

### Working on CodeBang (Default)

```bash
# SSH into VM
ssh user@your-vm-ip

# Navigate to CodeBang
cd ~/repos/CodeBang

# Start Claude Code
./scripts/start_claude.sh
```

**What happens:**
1. Script navigates to CodeBang root
2. Shows available context files
3. Starts Claude Code in interactive mode
4. Claude automatically reads CLAUDE.md and has full context

**Context files Claude sees:**
- `CLAUDE.md` - Architecture and bootstrapping rule
- `DEVCTO_CLAUDE_ATOMS.md` - 14 learning atoms
- `DevCTO_Complete_Build_Plan.md` - 7-phase roadmap
- `kb_client_example.py` - KB client reference

### Working on CodeBang with KB API

```bash
cd ~/repos/CodeBang
./scripts/start_claude.sh codebang --with-kb
```

**What happens:**
1. Script checks if KB API is running at http://localhost:8000
2. If not running, starts Agent-Factory KB API in background
3. Waits for API to be ready (health check)
4. Then starts Claude Code with full context

**Use this when:**
- You need to query DevCTO learning atoms
- You're testing KB integration
- You're working on KB-dependent features

### Working on Agent-Factory

```bash
cd ~/repos/CodeBang
./scripts/start_claude.sh agent-factory
```

**What happens:**
1. Script navigates to Agent-Factory repository
2. Shows KB API context
3. Starts Claude Code

**Use this when:**
- Working on KB API endpoints
- Debugging database issues
- Adding new atom ingestion features

### Getting Help

```bash
./scripts/start_claude.sh --help
```

**Output:**
```
DevCTO Cloud Dev Box - Claude Code Launcher

Usage: ./scripts/start_claude.sh [REPO] [OPTIONS]

Repositories:
  codebang       Start in CodeBang (DevCTO bootstrap)
  agent-factory  Start in Agent-Factory (KB infrastructure)

Options:
  --with-kb      Start KB API before launching Claude
  --help, -h     Show this help message

Examples:
  ./scripts/start_claude.sh                        # Work on CodeBang
  ./scripts/start_claude.sh codebang --with-kb     # Work on CodeBang with KB API
  ./scripts/start_claude.sh agent-factory          # Work on Agent-Factory
```

---

## Script Reference

### `setup_vm.sh` - One-Time VM Setup

**Purpose:** Prepare a fresh cloud VM for DevCTO development

**Location:** `CodeBang/scripts/setup_vm.sh`

**Usage:**
```bash
./scripts/setup_vm.sh
```

**What it checks:**
1. Claude Code CLI installed (`claude --version`)
2. Python dependencies installed
3. Agent-Factory .env exists (for KB features)

**When to run:**
- First time on a new VM
- After reinstalling OS
- If dependencies are missing

**Idempotent:** Safe to run multiple times

### `start_kb_api.sh` - KB API Startup Helper

**Purpose:** Start Agent-Factory Knowledge Base API

**Location:** `CodeBang/scripts/start_kb_api.sh`

**Usage:**
```bash
./scripts/start_kb_api.sh
```

**What it does:**
1. Checks if API already running (http://localhost:8000/health)
2. If not, locates Agent-Factory repository
3. Starts uvicorn server (auto-detects poetry vs pip)
4. Waits 3 seconds for startup
5. Verifies health check passes
6. Shows endpoint documentation

**Logs:** `/tmp/kb_api.log`

**When to use:**
- Manually start KB API without starting Claude
- Debugging KB API issues
- Testing API endpoints

**Called automatically by:** `start_claude.sh --with-kb`

### `start_claude.sh` - Main Entry Point

**Purpose:** Unified launcher for Claude Code sessions

**Location:** `CodeBang/scripts/start_claude.sh`

**Usage:**
```bash
./scripts/start_claude.sh [REPO] [OPTIONS]
```

**Arguments:**
- `REPO` (optional, default: `codebang`)
  - `codebang` - Work in CodeBang repository
  - `agent-factory` - Work in Agent-Factory repository

**Options:**
- `--with-kb` - Start KB API before launching Claude
- `--help` - Show help message

**Examples:**
```bash
# Default: Work on CodeBang
./scripts/start_claude.sh

# Work on CodeBang with KB API
./scripts/start_claude.sh codebang --with-kb

# Work on Agent-Factory
./scripts/start_claude.sh agent-factory

# Get help
./scripts/start_claude.sh --help
```

**What it does:**
1. Parses arguments
2. Optionally starts KB API (if `--with-kb`)
3. Navigates to selected repository
4. Shows context files available
5. Starts Claude Code in interactive mode

**Exit codes:**
- `0` - Success
- `1` - Error (missing repo, invalid args, etc.)

---

## Troubleshooting

### Issue: "Claude Code CLI not found"

**Error:**
```
[1/3] Checking Claude Code CLI...
  ❌ Claude Code CLI not found
```

**Solution:**
```bash
# Install Claude Code CLI following official docs
# Visit: https://docs.anthropic.com/claude-code/installation

# Verify installation
claude --version
```

### Issue: "Agent-Factory not found"

**Error:**
```
❌ Agent-Factory not found at: ../../Agent Factory/agent_factory

Expected directory structure:
  repos/
  ├── CodeBang/
  └── Agent Factory/
```

**Solution:**
```bash
cd ~/repos
git clone https://github.com/YOUR_USERNAME/Agent-Factory.git "Agent Factory"

# Verify structure
ls -la
# Should show both: CodeBang/ and Agent Factory/
```

### Issue: "KB API failed to start"

**Error:**
```
[4/4] Starting KB API server...
  ❌ KB API failed to start
  Check logs: /tmp/kb_api.log
```

**Solution:**
```bash
# Check the logs
tail -50 /tmp/kb_api.log

# Common causes:
# 1. Missing .env file
cd ~/repos/"Agent Factory"
cp .env.example .env
nano .env  # Add your API keys

# 2. Port 8000 already in use
sudo lsof -i :8000  # See what's using the port
# Kill the process or use a different port

# 3. Missing uvicorn
pip install uvicorn

# Retry
cd ~/repos/CodeBang
./scripts/start_kb_api.sh
```

### Issue: "pip: command not found"

**Error:**
```
  ❌ pip not found - please install Python 3 with pip
```

**Solution:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3-pip

# Verify
pip --version
python3 --version
```

### Issue: SSH connection refused

**Error:**
```
ssh: connect to host X.X.X.X port 22: Connection refused
```

**Solution:**
```bash
# Check VM is running (in cloud provider dashboard)
# Verify SSH is enabled on VM
# Check firewall allows port 22

# Test from VM provider's console first
# Then retry from your machine
```

### Issue: Permission denied (scripts not executable)

**Error:**
```
bash: ./scripts/start_claude.sh: Permission denied
```

**Solution:**
```bash
cd ~/repos/CodeBang
chmod +x scripts/*.sh

# Verify
ls -la scripts/
# Should show: -rwxr-xr-x (executable)
```

---

## Advanced Usage

### Running from Android (Termux)

1. **Install Termux** from F-Droid (not Play Store)

2. **Install SSH client:**
   ```bash
   pkg update
   pkg install openssh
   ```

3. **Connect to VM:**
   ```bash
   ssh user@your-vm-ip
   ```

4. **Use normally:**
   ```bash
   cd ~/repos/CodeBang
   ./scripts/start_claude.sh
   ```

**Tips:**
- Use Termux:Styling for better keyboard
- Enable extra keys row in settings
- Use tmux for persistent sessions

### Using tmux for Persistent Sessions

**Why:** Keep Claude Code running even if SSH disconnects

```bash
# Install tmux on VM
sudo apt install tmux

# Start tmux session
tmux new -s devcto

# Start Claude inside tmux
cd ~/repos/CodeBang
./scripts/start_claude.sh

# Detach: Press Ctrl+B, then D

# Reconnect later
ssh user@your-vm-ip
tmux attach -t devcto
```

### Checking KB API Status

```bash
# Check if running
curl http://localhost:8000/health

# Get statistics
curl http://localhost:8000/api/kb/stats

# Search atoms
curl -X POST http://localhost:8000/api/kb/search \
  -H "Content-Type: application/json" \
  -d '{"query": "devcto core loop", "top_k": 5}'

# Get specific atom
curl http://localhost:8000/api/kb/atom?atom_id=devcto_core_loop
```

### Manually Starting KB API

```bash
cd ~/repos/CodeBang
./scripts/start_kb_api.sh

# Check logs
tail -f /tmp/kb_api.log

# Stop API (find PID)
ps aux | grep uvicorn
kill <PID>
```

### Using Different Ports

**Edit `start_kb_api.sh`:**
```bash
nano ~/repos/CodeBang/scripts/start_kb_api.sh

# Change line:
KB_API_URL="http://localhost:8000"
# To:
KB_API_URL="http://localhost:8080"

# Also update uvicorn command:
--port 8000
# To:
--port 8080
```

### Setting Up SSH Keys for GitHub

```bash
# On VM, generate SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# Copy public key
cat ~/.ssh/id_ed25519.pub

# Add to GitHub:
# 1. Go to github.com/settings/keys
# 2. Click "New SSH key"
# 3. Paste your public key

# Test
ssh -T git@github.com
```

### Customizing Scripts

All scripts are simple bash with comments. Feel free to modify:

```bash
# Open in editor
nano ~/repos/CodeBang/scripts/start_claude.sh

# Add custom pre-launch checks
# Change default repository
# Adjust wait times
# Add logging
```

---

## Best Practices

### Security

1. **Don't commit .env files:**
   ```bash
   # Already in .gitignore, but verify:
   cat ~/repos/CodeBang/.gitignore
   # Should contain: .env
   ```

2. **Use SSH keys, not passwords:**
   ```bash
   ssh-copy-id user@your-vm-ip
   ```

3. **Regularly update VM:**
   ```bash
   sudo apt update && sudo apt upgrade
   ```

### Performance

1. **Use tmux for long sessions:**
   - Survives SSH disconnects
   - Can check back on progress

2. **Monitor VM resources:**
   ```bash
   htop  # Install with: sudo apt install htop
   df -h  # Check disk space
   ```

3. **Clean up logs periodically:**
   ```bash
   # KB API logs can grow large
   echo > /tmp/kb_api.log
   ```

### Workflow

1. **Start your day:**
   ```bash
   ssh user@your-vm-ip
   cd ~/repos/CodeBang
   ./scripts/start_claude.sh codebang --with-kb
   ```

2. **Work on tasks:**
   - Claude has full context from CLAUDE.md
   - Can query KB for patterns
   - Follow bootstrapping rule

3. **End your day:**
   - Commit your work
   - Push to GitHub
   - KB API will keep running (or restart next time)

---

## Quick Reference Card

### One-Time Setup
```bash
ssh user@your-vm-ip
mkdir ~/repos && cd ~/repos
git clone <url> CodeBang
git clone <url> "Agent Factory"
cd CodeBang
./scripts/setup_vm.sh
```

### Daily Commands
```bash
# Basic
./scripts/start_claude.sh

# With KB
./scripts/start_claude.sh codebang --with-kb

# Agent-Factory
./scripts/start_claude.sh agent-factory
```

### Troubleshooting
```bash
# Check setup
./scripts/setup_vm.sh

# Test KB API
curl http://localhost:8000/health

# View KB logs
tail -50 /tmp/kb_api.log

# Restart KB API
./scripts/start_kb_api.sh
```

---

## Documentation Index

**In `CodeBang/`:**
- `CLAUDE.md` - Architecture and bootstrapping rule
- `DEVCTO_CLAUDE_ATOMS.md` - 14 learning atoms
- `DevCTO_Complete_Build_Plan.md` - 7-phase roadmap
- `README.md` - Project overview
- `docs/CLOUD_DEV_BOX_GUIDE.md` - This guide
- `docs/QUICK_START.md` - Quick reference
- `docs/TROUBLESHOOTING.md` - Troubleshooting guide

**Scripts:**
- `scripts/setup_vm.sh` - One-time VM setup
- `scripts/start_kb_api.sh` - KB API helper
- `scripts/start_claude.sh` - Main launcher

---

## Getting Help

1. **Check this guide** - Most issues covered in Troubleshooting
2. **Run with --help:** `./scripts/start_claude.sh --help`
3. **Check logs:** `tail -50 /tmp/kb_api.log`
4. **Verify setup:** `./scripts/setup_vm.sh`
5. **GitHub Issues:** Report bugs or request features

---

## Updates and Maintenance

### Updating Scripts

```bash
cd ~/repos/CodeBang
git pull origin main

# Make scripts executable (if needed)
chmod +x scripts/*.sh
```

### Updating Dependencies

```bash
# Update Python packages
pip install --upgrade python-dotenv openai requests pyyaml

# Update Claude Code CLI
# (Follow official update procedure)
```

### Backing Up Configuration

```bash
# Backup .env files
cp ~/repos/"Agent Factory"/.env ~/backups/agent-factory-env.bak

# Backup custom scripts (if modified)
cp ~/repos/CodeBang/scripts/*.sh ~/backups/
```

---

**Version:** 1.0
**Last Updated:** 2025-12-16
**Maintained by:** DevCTO Bootstrap Team
