#!/bin/bash
# setup_vm.sh - One-time VM setup for DevCTO cloud dev box
#
# This script prepares a fresh cloud VM for DevCTO development by:
# 1. Checking Claude Code CLI installation
# 2. Installing required Python dependencies
# 3. Verifying Agent-Factory environment configuration
#
# Usage:
#   ./scripts/setup_vm.sh
#
# Requirements:
#   - bash
#   - Python 3.7+ with pip
#   - Internet connection for package downloads

set -e  # Exit on any error

echo "========================================="
echo "DevCTO Cloud Dev Box - VM Setup"
echo "========================================="
echo ""

# Step 1: Check if Claude Code CLI is installed
echo "[1/3] Checking Claude Code CLI..."
if ! command -v claude &> /dev/null; then
    echo "  ❌ Claude Code CLI not found"
    echo ""
    echo "  Please install Claude Code CLI manually:"
    echo "  https://docs.anthropic.com/claude-code/installation"
    echo ""
    echo "  After installation, run this script again."
    exit 1
else
    echo "  ✅ Claude Code CLI installed"
    claude --version 2>&1 | head -1 | sed 's/^/     /'
fi

echo ""

# Step 2: Install Python dependencies
echo "[2/3] Installing Python dependencies..."
if ! command -v pip &> /dev/null; then
    echo "  ❌ pip not found - please install Python 3 with pip"
    exit 1
fi

# Install required packages quietly
pip install -q python-dotenv openai requests pyyaml 2>&1 || {
    echo "  ⚠️  Some packages may have already been installed"
}

echo "  ✅ Python dependencies installed:"
echo "     - python-dotenv (environment variables)"
echo "     - openai (embeddings generation)"
echo "     - requests (HTTP client)"
echo "     - pyyaml (config parsing)"

echo ""

# Step 3: Check Agent-Factory .env configuration
echo "[3/3] Checking Agent-Factory configuration..."

AGENT_FACTORY_PATH="../Agent Factory"
ENV_FILE="$AGENT_FACTORY_PATH/.env"
ENV_EXAMPLE="$AGENT_FACTORY_PATH/.env.example"

if [ -d "$AGENT_FACTORY_PATH" ]; then
    if [ -f "$ENV_FILE" ]; then
        echo "  ✅ Agent-Factory .env found"
        echo "     Located at: $ENV_FILE"
    else
        echo "  ⚠️  Agent-Factory .env not found"
        echo ""
        echo "  To use Knowledge Base features, create .env:"
        echo "     cd '$AGENT_FACTORY_PATH'"
        if [ -f "$ENV_EXAMPLE" ]; then
            echo "     cp .env.example .env"
        else
            echo "     touch .env"
        fi
        echo "     # Edit .env with your API keys:"
        echo "     #   - OPENAI_API_KEY=sk-..."
        echo "     #   - SUPABASE_URL=https://..."
        echo "     #   - SUPABASE_SERVICE_ROLE_KEY=..."
        echo ""
        echo "  (You can skip this if not using KB features yet)"
    fi
else
    echo "  ⚠️  Agent-Factory repository not found at: $AGENT_FACTORY_PATH"
    echo ""
    echo "  If you want to use Knowledge Base features, clone Agent-Factory:"
    echo "     cd .."
    echo "     git clone <agent-factory-repo-url> 'Agent Factory'"
    echo ""
    echo "  (You can skip this if only working on CodeBang)"
fi

echo ""
echo "========================================="
echo "✅ Setup Complete!"
echo "========================================="
echo ""
echo "Next steps:"
echo "  1. Start Claude Code:"
echo "     ./scripts/start_claude.sh"
echo ""
echo "  2. Work on CodeBang with KB support:"
echo "     ./scripts/start_claude.sh codebang --with-kb"
echo ""
echo "  3. Work on Agent-Factory:"
echo "     ./scripts/start_claude.sh agent-factory"
echo ""
echo "For help: ./scripts/start_claude.sh --help"
echo "========================================="
