#!/bin/bash
set -e

echo "🚀 Installing Agent Social Matching Skill..."
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Install dependencies
echo ""
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Setup environment
if [ ! -f .env ]; then
    echo ""
    echo "⚙️  Creating .env file..."
    cp .env.example .env
    echo "✅ .env created (using default NextMarket API)"
fi

# Make scripts executable
echo ""
echo "🔧 Making scripts executable..."
chmod +x scripts/*.py

# Test connection
echo ""
echo "🔍 Testing API connection..."
python3 scripts/test_connection.py

echo ""
echo "=" 60
echo "🎉 Installation complete!"
echo "=" 60
echo ""
echo "Quick start:"
echo "  # Register your agent (interactive)"
echo "  ./scripts/register_agent.py --interactive"
echo ""
echo "  # Or register with command-line args"
echo "  ./scripts/register_agent.py --name 'Your Name' --email 'you@example.com'"
echo ""
echo "For more examples, see:"
echo "  • SKILL.md - Complete documentation"
echo "  • README_FOR_AGENTS.md - AI agent guide"
echo ""
