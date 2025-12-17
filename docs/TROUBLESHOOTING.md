# Cloud Dev Box Troubleshooting Guide

Solutions to common issues when setting up and using the DevCTO cloud development environment.

---

## Table of Contents

1. [Setup Issues](#setup-issues)
2. [Script Execution Issues](#script-execution-issues)
3. [KB API Issues](#kb-api-issues)
4. [SSH and Connectivity Issues](#ssh-and-connectivity-issues)
5. [Claude Code Issues](#claude-code-issues)
6. [Environment and Dependencies](#environment-and-dependencies)
7. [Diagnostic Commands](#diagnostic-commands)

---

## Setup Issues

### Claude Code CLI Not Found

**Symptoms:**
```
[1/3] Checking Claude Code CLI...
  ❌ Claude Code CLI not found

  Please install Claude Code CLI manually:
  https://docs.anthropic.com/claude-code/installation
```

**Cause:** Claude Code CLI is not installed on the VM.

**Solution:**
```bash
# Follow official installation guide
# Visit: https://docs.anthropic.com/claude-code/installation

# After installation, verify
claude --version

# Re-run setup
cd ~/repos/CodeBang
./scripts/setup_vm.sh
```

**Alternative:** Check if it's installed but not in PATH:
```bash
# Find claude binary
which claude
find ~ -name "claude" 2>/dev/null

# Add to PATH if found
export PATH="$PATH:/path/to/claude/directory"
# Add to ~/.bashrc to make permanent
```

---

### Agent-Factory Repository Not Found

**Symptoms:**
```
❌ Agent-Factory not found at: ../../Agent Factory/agent_factory

Expected directory structure:
  repos/
  ├── CodeBang/
  └── Agent Factory/
      └── agent_factory/
```

**Cause:** Agent-Factory not cloned or wrong location.

**Solution:**
```bash
# Navigate to repos directory
cd ~/repos

# Clone Agent-Factory
git clone https://github.com/YOUR_USERNAME/Agent-Factory.git "Agent Factory"

# Verify structure
ls -la
# Should show:
#   drwxr-xr-x  CodeBang/
#   drwxr-xr-x  Agent Factory/

# Verify nested structure
ls -la "Agent Factory"/
# Should contain: agent_factory/ directory

# Try again
cd ~/repos/CodeBang
./scripts/start_claude.sh agent-factory
```

**Note:** The directory name must be exactly `Agent Factory` (with space).

---

### Python Dependencies Installation Failed

**Symptoms:**
```
[2/3] Installing Python dependencies...
  ERROR: Could not install packages due to an OSError
```

**Causes:**
1. No internet connection
2. pip not installed
3. Permission issues
4. Disk space full

**Solutions:**

**Check internet:**
```bash
ping -c 3 google.com
curl -I https://pypi.org
```

**Install/upgrade pip:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3-pip

# Verify
pip --version
python3 --version
```

**Use --user flag if permission issues:**
```bash
pip install --user python-dotenv openai requests pyyaml
```

**Check disk space:**
```bash
df -h
# If disk is full, clean up:
sudo apt clean
sudo apt autoremove
```

---

## Script Execution Issues

### Permission Denied

**Symptoms:**
```bash
./scripts/start_claude.sh
bash: ./scripts/start_claude.sh: Permission denied
```

**Cause:** Scripts are not executable.

**Solution:**
```bash
cd ~/repos/CodeBang

# Make all scripts executable
chmod +x scripts/*.sh

# Verify
ls -la scripts/
# Should show: -rwxr-xr-x (note the 'x')

# Try again
./scripts/start_claude.sh
```

---

### Script Not Found

**Symptoms:**
```bash
./scripts/start_claude.sh
bash: ./scripts/start_claude.sh: No such file or directory
```

**Cause:** Wrong directory or scripts not pulled from git.

**Solution:**
```bash
# Verify you're in CodeBang root
pwd
# Should be: /home/USER/repos/CodeBang

# If not, navigate there
cd ~/repos/CodeBang

# Check if scripts exist
ls -la scripts/
# Should show: setup_vm.sh, start_claude.sh, start_kb_api.sh

# If scripts missing, pull from git
git pull origin main

# If still missing, verify you cloned the right repo
git remote -v
```

---

### "Command not found" in Script

**Symptoms:**
Script runs but fails with "command not found" errors.

**Common missing commands and solutions:**

**curl:**
```bash
sudo apt install curl
```

**git:**
```bash
sudo apt install git
```

**nano:**
```bash
sudo apt install nano
```

**python3:**
```bash
sudo apt install python3
```

---

## KB API Issues

### KB API Failed to Start

**Symptoms:**
```
[4/4] Starting KB API server...
  Started API server (PID: 12345)
  Waiting for startup (3 seconds)...

Verifying server health...
  ❌ KB API failed to start

  Check logs: /tmp/kb_api.log
```

**Diagnostic steps:**

**1. Check logs:**
```bash
tail -50 /tmp/kb_api.log
```

**2. Common error patterns:**

**Error: "No module named 'agent_factory'"**
```bash
# Agent-Factory not in Python path
cd ~/repos/"Agent Factory"/agent_factory
pwd
# Make note of path

# Set PYTHONPATH
export PYTHONPATH="~/repos/Agent Factory:$PYTHONPATH"

# Or use poetry
cd ~/repos/"Agent Factory"
poetry install
poetry run uvicorn agent_factory.api.kb_api:app --port 8000
```

**Error: "Address already in use"**
```bash
# Port 8000 is occupied
sudo lsof -i :8000
# Shows: COMMAND   PID  USER
#        uvicorn  1234  youruser

# Kill the process
kill 1234

# Or use different port (edit start_kb_api.sh)
```

**Error: "connection to database failed"**
```bash
# Missing or invalid .env file
cd ~/repos/"Agent Factory"

# Check if .env exists
ls -la .env

# If missing, create it
cp .env.example .env
nano .env

# Add required keys:
# OPENAI_API_KEY=sk-...
# SUPABASE_URL=https://...
# SUPABASE_SERVICE_ROLE_KEY=...

# Restart KB API
cd ~/repos/CodeBang
./scripts/start_kb_api.sh
```

---

### KB API Health Check Fails

**Symptoms:**
```bash
curl http://localhost:8000/health
curl: (7) Failed to connect to localhost port 8000: Connection refused
```

**Diagnostic:**
```bash
# Check if process is running
ps aux | grep uvicorn

# Check if port is listening
sudo netstat -tlnp | grep 8000

# Check logs for crash
tail -100 /tmp/kb_api.log
```

**Solutions:**

**Process not running:**
```bash
./scripts/start_kb_api.sh
```

**Process running but not responding:**
```bash
# Kill and restart
pkill -f uvicorn
./scripts/start_kb_api.sh
```

**Different port:**
```bash
# If API is on different port, edit script
nano ~/repos/CodeBang/scripts/start_kb_api.sh
# Change KB_API_URL="http://localhost:8000"
# To:    KB_API_URL="http://localhost:8080"
```

---

### KB API Returns 500 Errors

**Symptoms:**
```bash
curl http://localhost:8000/api/kb/search
{"detail":"Internal Server Error"}
```

**Diagnostic:**
```bash
# Check detailed logs
tail -100 /tmp/kb_api.log | grep -A 10 "ERROR"

# Common causes:
# 1. Database not accessible
# 2. Missing environment variables
# 3. Invalid data in database
```

**Solutions:**

**Test database connection:**
```bash
cd ~/repos/"Agent Factory"

# Try connecting directly
python3 -c "
from agent_factory.memory.storage import SupabaseMemoryStorage
storage = SupabaseMemoryStorage()
print('Database connection successful!')
"
```

**Verify environment variables:**
```bash
cd ~/repos/"Agent Factory"
cat .env | grep -v "^#" | grep -v "^$"
# Should show all required keys with values
```

---

## SSH and Connectivity Issues

### SSH Connection Refused

**Symptoms:**
```bash
ssh user@your-vm-ip
ssh: connect to host X.X.X.X port 22: Connection refused
```

**Causes:**
1. VM is not running
2. SSH service not running on VM
3. Firewall blocking port 22
4. Wrong IP address

**Solutions:**

**Check VM status:**
- Log into your cloud provider dashboard
- Verify VM is "Running" or "Active"
- Check VM's public IP address

**Test from provider console:**
- Most cloud providers have web-based console access
- Connect via console and check SSH service:
```bash
sudo systemctl status ssh
sudo systemctl start ssh  # If not running
```

**Check firewall rules:**
```bash
# On VM (via console)
sudo ufw status
# If blocking SSH, allow it:
sudo ufw allow 22/tcp
```

**Verify IP address:**
```bash
# On VM (via console)
ip addr show
curl ifconfig.me  # Shows public IP
```

---

### SSH Connection Times Out

**Symptoms:**
```bash
ssh user@your-vm-ip
# Hangs for a long time, then:
ssh: connect to host X.X.X.X port 22: Connection timed out
```

**Causes:**
1. Firewall/security group blocking
2. Network issue
3. VM is in different region

**Solutions:**

**Check cloud provider security groups:**
- Ensure inbound rule allows TCP port 22 from your IP
- Or allow from 0.0.0.0/0 (less secure but works from anywhere)

**Test network path:**
```bash
ping your-vm-ip
traceroute your-vm-ip
```

**Try different network:**
- Use mobile hotspot vs home WiFi
- Use VPN if behind restrictive firewall

---

### SSH Authentication Failed

**Symptoms:**
```bash
ssh user@your-vm-ip
Permission denied (publickey).
```

**Causes:**
1. SSH key not added to VM
2. Wrong username
3. SSH key not loaded

**Solutions:**

**Copy SSH key to VM:**
```bash
ssh-copy-id user@your-vm-ip
# Enter password when prompted
```

**Verify SSH key is loaded:**
```bash
ssh-add -l
# If empty, add your key:
ssh-add ~/.ssh/id_ed25519
```

**Check username:**
```bash
# Common usernames:
# Ubuntu: ubuntu
# Debian: debian
# CentOS: centos
# Custom: whatever you set during VM creation
```

**Use password authentication (temporarily):**
```bash
ssh -o PreferredAuthentications=password user@your-vm-ip
```

---

## Claude Code Issues

### Claude Code Won't Start

**Symptoms:**
Script runs but Claude doesn't launch, or crashes immediately.

**Diagnostic:**
```bash
# Try running Claude directly
claude --version
claude

# Check for error messages
```

**Common issues:**

**API key not set:**
```bash
# Set Anthropic API key
export ANTHROPIC_API_KEY="sk-ant-..."

# Add to ~/.bashrc for persistence
echo 'export ANTHROPIC_API_KEY="sk-ant-..."' >> ~/.bashrc
```

**Terminal issues:**
```bash
# Set correct terminal
export TERM=xterm-256color

# Or try different terminal emulator
# screen, tmux, etc.
```

---

### Claude Can't Read Files

**Symptoms:**
Claude starts but can't access CLAUDE.md or other context files.

**Diagnostic:**
```bash
# Verify files exist
ls -la ~/repos/CodeBang/CLAUDE.md
ls -la ~/repos/CodeBang/DEVCTO_CLAUDE_ATOMS.md

# Check permissions
ls -la ~/repos/CodeBang/*.md
# Should show: -rw-r--r-- (readable)
```

**Solution:**
```bash
# Make files readable
chmod 644 ~/repos/CodeBang/*.md

# Verify Claude is in correct directory
pwd
# Should be in repo root when Claude starts
```

---

## Environment and Dependencies

### Missing Python Package

**Symptoms:**
```
ModuleNotFoundError: No module named 'dotenv'
```

**Solution:**
```bash
pip install python-dotenv

# Or install all at once
pip install python-dotenv openai requests pyyaml

# Verify
python3 -c "import dotenv; print('OK')"
```

---

### Wrong Python Version

**Symptoms:**
```
SyntaxError: f-string expressions are only supported in Python 3.6+
```

**Solution:**
```bash
# Check Python version
python3 --version
# Should be 3.7 or higher

# If too old, upgrade (Ubuntu):
sudo apt update
sudo apt install python3.9

# Make default
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1
```

---

### Environment Variables Not Set

**Symptoms:**
Scripts reference `$VARIABLE` but it's empty or undefined.

**Diagnostic:**
```bash
# Check if .env exists
ls -la ~/repos/"Agent Factory"/.env

# Check if variables are loaded
cd ~/repos/"Agent Factory"
python3 -c "
import os
from dotenv import load_dotenv
load_dotenv()
print('OPENAI_API_KEY:', os.getenv('OPENAI_API_KEY', 'NOT SET'))
"
```

**Solution:**
```bash
cd ~/repos/"Agent Factory"

# Create .env if missing
cp .env.example .env

# Edit with required values
nano .env

# Verify
cat .env | grep -v "^#" | grep -v "^$"
```

---

## Diagnostic Commands

### System Health Check

```bash
# VM resources
free -h              # Memory
df -h                # Disk space
uptime               # System uptime and load

# Network
ping -c 3 google.com # Internet connectivity
curl ifconfig.me     # Public IP

# Services
ps aux | grep uvicorn  # KB API process
ps aux | grep claude   # Claude process
sudo netstat -tlnp     # Listening ports
```

### Repository Health Check

```bash
cd ~/repos/CodeBang

# Git status
git status
git remote -v

# File integrity
ls -la scripts/
ls -la *.md

# Script permissions
ls -la scripts/*.sh
# Should all show: -rwxr-xr-x
```

### KB API Detailed Diagnostics

```bash
# API health
curl -v http://localhost:8000/health

# API stats
curl http://localhost:8000/api/kb/stats | python3 -m json.tool

# Test search
curl -X POST http://localhost:8000/api/kb/search \
  -H "Content-Type: application/json" \
  -d '{"query": "test", "top_k": 1}' | python3 -m json.tool

# Check logs for errors
grep -i error /tmp/kb_api.log
grep -i exception /tmp/kb_api.log
```

### Python Environment Check

```bash
# Python version
python3 --version

# Installed packages
pip list | grep -E "(dotenv|openai|requests|pyyaml)"

# Import test
python3 << EOF
try:
    import dotenv
    import openai
    import requests
    import yaml
    print("All packages OK")
except ImportError as e:
    print(f"Missing: {e}")
EOF
```

---

## Getting More Help

If you're still stuck after trying these solutions:

1. **Check logs in detail:**
   ```bash
   tail -100 /tmp/kb_api.log
   ```

2. **Run setup again:**
   ```bash
   cd ~/repos/CodeBang
   ./scripts/setup_vm.sh
   ```

3. **Start fresh (last resort):**
   ```bash
   cd ~/repos
   mv CodeBang CodeBang.bak
   git clone <url> CodeBang
   cd CodeBang
   ./scripts/setup_vm.sh
   ```

4. **Report an issue:**
   - GitHub Issues: https://github.com/YOUR_USERNAME/CodeBang/issues
   - Include: OS version, error messages, relevant log output

---

## Appendix: Common Error Messages

| Error Message | Likely Cause | Quick Fix |
|--------------|--------------|-----------|
| "command not found: claude" | Claude CLI not installed | Install from official docs |
| "Permission denied" | Script not executable | `chmod +x scripts/*.sh` |
| "No such file or directory" | Wrong directory | `cd ~/repos/CodeBang` |
| "Agent-Factory not found" | Not cloned or wrong path | Clone to `~/repos/Agent Factory/` |
| "Address already in use" | Port 8000 occupied | Kill process: `pkill -f uvicorn` |
| "Connection refused" | API not running | `./scripts/start_kb_api.sh` |
| "ModuleNotFoundError" | Missing Python package | `pip install <package>` |
| "Invalid API key" | Wrong/missing .env | Check `.env` file |
| "No module named 'agent_factory'" | Wrong Python path | Use poetry or set PYTHONPATH |

---

**Version:** 1.0
**Last Updated:** 2025-12-16

For more help, see [CLOUD_DEV_BOX_GUIDE.md](./CLOUD_DEV_BOX_GUIDE.md)
