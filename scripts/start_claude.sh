#!/bin/bash
# start_claude.sh - Start Claude Code with DevCTO context
#
# This is the main entry point for working with DevCTO on a cloud dev box.
# It starts Claude Code in the selected repository with proper context files.
#
# Usage:
#   ./scripts/start_claude.sh [REPO] [OPTIONS]
#
# Arguments:
#   REPO        Repository to work in (default: codebang)
#               - codebang: DevCTO bootstrap repository
#               - agent-factory: Agent-Factory KB infrastructure
#
# Options:
#   --with-kb   Start KB API before launching Claude (for KB integration)
#   --help      Show this help message
#
# Examples:
#   ./scripts/start_claude.sh
#   ./scripts/start_claude.sh codebang --with-kb
#   ./scripts/start_claude.sh agent-factory

# Parse arguments
REPO="${1:-codebang}"
START_KB=false

# Show help
if [[ "$*" == *"--help"* ]] || [[ "$1" == "-h" ]]; then
    echo "DevCTO Cloud Dev Box - Claude Code Launcher"
    echo ""
    echo "Usage: $0 [REPO] [OPTIONS]"
    echo ""
    echo "Repositories:"
    echo "  codebang       Start in CodeBang (DevCTO bootstrap)"
    echo "  agent-factory  Start in Agent-Factory (KB infrastructure)"
    echo ""
    echo "Options:"
    echo "  --with-kb      Start KB API before launching Claude"
    echo "  --help, -h     Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0                        # Work on CodeBang"
    echo "  $0 codebang --with-kb     # Work on CodeBang with KB API"
    echo "  $0 agent-factory          # Work on Agent-Factory"
    echo ""
    exit 0
fi

# Check for --with-kb flag
if [[ "$*" == *"--with-kb"* ]]; then
    START_KB=true
fi

echo "========================================="
echo "DevCTO Cloud Dev Box - Starting Claude"
echo "========================================="
echo ""

# Optional: Start KB API if requested
if [ "$START_KB" = true ]; then
    echo "Starting KB API..."
    echo ""

    SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
    "$SCRIPT_DIR/start_kb_api.sh" || {
        echo ""
        echo "⚠️  Warning: KB API failed to start"
        echo "   Continuing anyway - you can start it manually later"
        echo ""
        sleep 2
    }
    echo ""
fi

# Navigate to selected repo and start Claude
if [ "$REPO" = "codebang" ]; then
    # Navigate to CodeBang root (parent of scripts/)
    cd "$(dirname "$0")/.." || {
        echo "❌ Failed to navigate to CodeBang directory"
        exit 1
    }

    echo "Repository: CodeBang (DevCTO Bootstrap)"
    echo "Location:   $(pwd)"
    echo ""
    echo "Context files available to Claude:"
    echo "  📄 CLAUDE.md                     - Architecture & bootstrapping rule"
    echo "  📚 DEVCTO_CLAUDE_ATOMS.md        - 14 learning atoms"
    echo "  📋 DevCTO_Complete_Build_Plan.md - 7-phase implementation roadmap"
    echo "  🔧 kb_client_example.py          - KB client reference"
    echo "  📖 NEXT_STEPS.md                 - Action plan for next phase"
    echo ""
    echo "Starting Claude Code in 2 seconds..."
    echo "========================================="
    sleep 2

    # Start Claude Code (interactive mode)
    claude

elif [ "$REPO" = "agent-factory" ]; then
    # Navigate to Agent-Factory (sibling directory)
    AGENT_FACTORY_PATH="$(dirname "$0")/../../Agent Factory/agent_factory"

    if [ ! -d "$AGENT_FACTORY_PATH" ]; then
        echo "❌ Agent-Factory not found"
        echo ""
        echo "Expected path: $AGENT_FACTORY_PATH"
        echo ""
        echo "Directory structure should be:"
        echo "  repos/"
        echo "  ├── CodeBang/"
        echo "  └── Agent Factory/"
        echo "      └── agent_factory/  ← Looking for this"
        echo ""
        echo "Clone Agent-Factory:"
        echo "  cd .."
        echo "  git clone <agent-factory-url> 'Agent Factory'"
        echo ""
        exit 1
    fi

    cd "$AGENT_FACTORY_PATH" || {
        echo "❌ Failed to navigate to Agent-Factory directory"
        exit 1
    }

    echo "Repository: Agent-Factory"
    echo "Location:   $(pwd)"
    echo ""
    echo "Context:"
    echo "  🔌 KB API endpoints (agent_factory/api/kb_api.py)"
    echo "  💾 Database infrastructure (memory/storage.py)"
    echo "  🧠 Knowledge atoms table schema"
    echo "  🔧 Multi-provider database manager"
    echo ""
    echo "Starting Claude Code in 2 seconds..."
    echo "========================================="
    sleep 2

    # Start Claude Code (interactive mode)
    claude

else
    echo "❌ Unknown repository: '$REPO'"
    echo ""
    echo "Valid options:"
    echo "  - codebang"
    echo "  - agent-factory"
    echo ""
    echo "Usage: $0 [codebang|agent-factory] [--with-kb]"
    echo ""
    echo "For help: $0 --help"
    exit 1
fi
