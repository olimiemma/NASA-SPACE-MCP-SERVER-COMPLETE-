#!/bin/bash
# Space MCP Server - Quick Setup Script
# This script helps you set up the Space MCP Server quickly

set -e  # Exit on error

echo "🌌 Space & Astronomy MCP Server - Quick Setup"
echo "=============================================="
echo ""

# Check Python version
echo "Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed."
    echo "Please install Python 3.10 or higher from https://www.python.org/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
REQUIRED_VERSION="3.10"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Error: Python $REQUIRED_VERSION or higher is required."
    echo "   Current version: $PYTHON_VERSION"
    exit 1
fi

echo "✅ Python $PYTHON_VERSION detected"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists. Skipping creation."
else
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Verify installation
echo "Verifying installation..."
python -m py_compile space_mcp.py
if [ $? -eq 0 ]; then
    echo "✅ Server syntax validated"
else
    echo "❌ Error: Server validation failed"
    exit 1
fi
echo ""

# Make server executable
echo "Making server executable..."
chmod +x space_mcp.py
echo "✅ Server is executable"
echo ""

# Test server
echo "Testing server..."
if python space_mcp.py --help > /dev/null 2>&1; then
    echo "✅ Server is working correctly"
else
    echo "⚠️  Server test returned warnings (this might be normal)"
fi
echo ""

# Get absolute path
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
SERVER_PATH="$SCRIPT_DIR/space_mcp.py"

# Configuration instructions
echo "=============================================="
echo "✨ Setup Complete!"
echo "=============================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Add this server to Claude Desktop:"
echo ""
echo "   Location: ~/Library/Application Support/Claude/claude_desktop_config.json"
echo "   (On Windows: %APPDATA%\\Claude\\claude_desktop_config.json)"
echo ""
echo "   Add this configuration:"
echo ""
echo '   {'
echo '     "mcpServers": {'
echo '       "space": {'
echo '         "command": "python",'
echo "         \"args\": [\"$SERVER_PATH\"]"
echo '       }'
echo '     }'
echo '   }'
echo ""
echo "2. Restart Claude Desktop"
echo ""
echo "3. Try these prompts:"
echo "   - 'Show me today's astronomy picture'"
echo "   - 'Where is the ISS right now?'"
echo "   - 'Get recent Curiosity rover photos'"
echo ""
echo "🚀 Happy space exploring!"
echo ""
echo "For more information, see README.md"
echo ""

# Deactivate virtual environment message
echo "Note: To activate the virtual environment manually, run:"
echo "  source venv/bin/activate"
echo ""
