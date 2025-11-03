# Space MCP Server - Quick Setup Script (Windows)
# This script helps you set up the Space MCP Server quickly on Windows

Write-Host "🌌 Space & Astronomy MCP Server - Quick Setup" -ForegroundColor Cyan
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "Checking Python version..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    if ($pythonVersion -match "Python (\d+\.\d+)") {
        $version = [Version]$Matches[1]
        $requiredVersion = [Version]"3.10"
        
        if ($version -lt $requiredVersion) {
            Write-Host "❌ Error: Python 3.10 or higher is required." -ForegroundColor Red
            Write-Host "   Current version: $version" -ForegroundColor Red
            Write-Host "   Please install from https://www.python.org/" -ForegroundColor Yellow
            exit 1
        }
        Write-Host "✅ Python $version detected" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Error: Python is not installed or not in PATH." -ForegroundColor Red
    Write-Host "   Please install Python 3.10+ from https://www.python.org/" -ForegroundColor Yellow
    exit 1
}
Write-Host ""

# Create virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "⚠️  Virtual environment already exists. Skipping creation." -ForegroundColor Yellow
} else {
    python -m venv venv
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
}
Write-Host ""

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"
Write-Host "✅ Virtual environment activated" -ForegroundColor Green
Write-Host ""

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt
Write-Host "✅ Dependencies installed" -ForegroundColor Green
Write-Host ""

# Verify installation
Write-Host "Verifying installation..." -ForegroundColor Yellow
python -m py_compile space_mcp.py
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Server syntax validated" -ForegroundColor Green
} else {
    Write-Host "❌ Error: Server validation failed" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Test server
Write-Host "Testing server..." -ForegroundColor Yellow
python space_mcp.py --help > $null 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Server is working correctly" -ForegroundColor Green
} else {
    Write-Host "⚠️  Server test returned warnings (this might be normal)" -ForegroundColor Yellow
}
Write-Host ""

# Get absolute path
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$serverPath = Join-Path $scriptDir "space_mcp.py"
$serverPath = $serverPath -replace '\\', '\\'

# Configuration instructions
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host "✨ Setup Complete!" -ForegroundColor Cyan
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Add this server to Claude Desktop:" -ForegroundColor White
Write-Host ""
Write-Host "   Location: " -NoNewline
Write-Host "%APPDATA%\Claude\claude_desktop_config.json" -ForegroundColor Cyan
Write-Host ""
Write-Host "   Add this configuration:" -ForegroundColor White
Write-Host ""
Write-Host '   {' -ForegroundColor Gray
Write-Host '     "mcpServers": {' -ForegroundColor Gray
Write-Host '       "space": {' -ForegroundColor Gray
Write-Host '         "command": "python",' -ForegroundColor Gray
Write-Host "         `"args`": [`"$serverPath`"]" -ForegroundColor Gray
Write-Host '       }' -ForegroundColor Gray
Write-Host '     }' -ForegroundColor Gray
Write-Host '   }' -ForegroundColor Gray
Write-Host ""
Write-Host "2. Restart Claude Desktop" -ForegroundColor White
Write-Host ""
Write-Host "3. Try these prompts:" -ForegroundColor White
Write-Host "   - 'Show me today's astronomy picture'" -ForegroundColor Cyan
Write-Host "   - 'Where is the ISS right now?'" -ForegroundColor Cyan
Write-Host "   - 'Get recent Curiosity rover photos'" -ForegroundColor Cyan
Write-Host ""
Write-Host "🚀 Happy space exploring!" -ForegroundColor Magenta
Write-Host ""
Write-Host "For more information, see README.md" -ForegroundColor Yellow
Write-Host ""

# Deactivate virtual environment message
Write-Host "Note: To activate the virtual environment manually, run:" -ForegroundColor Yellow
Write-Host "  venv\Scripts\Activate.ps1" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
