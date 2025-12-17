#!/bin/bash
# start_kb_api.sh - Start Agent-Factory Knowledge Base API
#
# This script starts the Agent-Factory KB API server if it's not already running.
# The KB API provides vector search and retrieval of DevCTO learning atoms.
#
# Usage:
#   ./scripts/start_kb_api.sh
#
# The API will be available at: http://localhost:8000
# Logs are written to: /tmp/kb_api.log

AGENT_FACTORY_PATH="../../Agent Factory/agent_factory"
KB_API_URL="http://localhost:8000"
LOG_FILE="/tmp/kb_api.log"

echo "========================================="
echo "DevCTO - KB API Startup Helper"
echo "========================================="
echo ""

# Step 1: Check if API is already running
echo "[1/4] Checking if KB API is already running..."
if curl -s "$KB_API_URL/health" &> /dev/null; then
    echo "  ✅ KB API already running at $KB_API_URL"
    echo ""
    curl -s "$KB_API_URL/health" | head -1
    exit 0
else
    echo "  ℹ️  KB API not running, will start it now"
fi

echo ""

# Step 2: Verify Agent-Factory repository exists
echo "[2/4] Locating Agent-Factory repository..."
if [ ! -d "$AGENT_FACTORY_PATH" ]; then
    echo "  ❌ Agent-Factory not found at: $AGENT_FACTORY_PATH"
    echo ""
    echo "  Expected directory structure:"
    echo "    repos/"
    echo "    ├── CodeBang/           (current repo)"
    echo "    │   └── scripts/        (you are here)"
    echo "    └── Agent Factory/"
    echo "        └── agent_factory/  (looking for this)"
    echo ""
    echo "  To fix:"
    echo "    cd .."
    echo "    git clone <agent-factory-url> 'Agent Factory'"
    echo ""
    exit 1
else
    echo "  ✅ Agent-Factory found at: $AGENT_FACTORY_PATH"
fi

echo ""

# Step 3: Check if .env is configured
echo "[3/4] Checking environment configuration..."
if [ ! -f "$AGENT_FACTORY_PATH/../.env" ]; then
    echo "  ⚠️  Warning: Agent-Factory .env not found"
    echo "     KB API may fail to connect to database"
    echo "     Continuing anyway..."
else
    echo "  ✅ Environment configuration found"
fi

echo ""

# Step 4: Start the KB API server
echo "[4/4] Starting KB API server..."

# Navigate to Agent-Factory directory
cd "$AGENT_FACTORY_PATH" || {
    echo "  ❌ Failed to navigate to Agent-Factory directory"
    exit 1
}

# Determine how to start the server (poetry vs pip)
if [ -f "pyproject.toml" ] && command -v poetry &> /dev/null; then
    echo "  Using poetry to start API..."
    nohup poetry run uvicorn agent_factory.api.kb_api:app \
        --host 0.0.0.0 --port 8000 > "$LOG_FILE" 2>&1 &
    API_PID=$!
elif command -v uvicorn &> /dev/null; then
    echo "  Using uvicorn directly..."
    nohup uvicorn agent_factory.api.kb_api:app \
        --host 0.0.0.0 --port 8000 > "$LOG_FILE" 2>&1 &
    API_PID=$!
else
    echo "  ❌ Neither poetry nor uvicorn found"
    echo ""
    echo "  Install with:"
    echo "    pip install uvicorn"
    echo "  Or:"
    echo "    poetry install"
    exit 1
fi

echo "  Started API server (PID: $API_PID)"
echo "  Waiting for startup (3 seconds)..."
sleep 3

echo ""

# Verify the server started successfully
echo "Verifying server health..."
if curl -s "$KB_API_URL/health" &> /dev/null; then
    echo "  ✅ KB API started successfully!"
    echo ""
    echo "  API URL: $KB_API_URL"
    echo "  Logs:    $LOG_FILE"
    echo ""
    echo "  Available endpoints:"
    echo "    GET  /health              - Health check"
    echo "    POST /api/kb/search       - Vector search"
    echo "    GET  /api/kb/atom         - Get atom by ID"
    echo "    GET  /api/kb/stats        - KB statistics"
    echo ""
    echo "  Test with:"
    echo "    curl $KB_API_URL/health"
else
    echo "  ❌ KB API failed to start"
    echo ""
    echo "  Check logs for errors:"
    echo "    tail -50 $LOG_FILE"
    echo ""
    echo "  Common issues:"
    echo "    - Missing .env file in Agent-Factory"
    echo "    - Database connection failed"
    echo "    - Port 8000 already in use"
    exit 1
fi

echo "========================================="
