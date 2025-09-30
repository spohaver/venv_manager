#!/bin/bash
# Quick installation script for venv-manager

set -e

echo "🐍 Installing Virtual Environment Manager..."

# Check if git is available
if ! command -v git &> /dev/null; then
    echo "❌ Git is required but not installed. Please install git first."
    exit 1
fi

# Check if python is available
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "❌ Python is required but not installed. Please install Python 3.6+ first."
    exit 1
fi

# Default installation directory
INSTALL_DIR="$HOME/venv-manager"

# Allow custom installation directory
if [ ! -z "$1" ]; then
    INSTALL_DIR="$1"
fi

echo "📁 Installing to: $INSTALL_DIR"

# Clone the repository
if [ -d "$INSTALL_DIR" ]; then
    echo "⚠️  Directory $INSTALL_DIR already exists. Updating..."
    cd "$INSTALL_DIR"
    git pull
else
    echo "⬇️  Cloning repository..."
    git clone https://github.com/spohaver/venv-manager.git "$INSTALL_DIR"
    cd "$INSTALL_DIR"
fi

# Make scripts executable
chmod +x venv-manager setupvenv.py

echo "✅ Installation complete!"
echo ""
echo "🚀 Quick start:"
echo "   cd $INSTALL_DIR"
echo "   ./venv-manager --help"
echo ""
echo "💡 For global access, add to your PATH:"
echo "   export PATH=\"$INSTALL_DIR:\$PATH\""
echo "   # Add the above line to your ~/.bashrc or ~/.zshrc"
echo ""
echo "📚 Documentation: https://github.com/spohaver/venv-manager"