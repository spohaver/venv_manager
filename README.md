# 🐍 Virtual Environment Manager

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)

A comprehensive Python virtual environment manager that simplifies creating, managing, and activating Python virtual environments with automatic package installation.

## ✨ Features

- 🚀 **Easy Creation**: Create virtual environments with a single command
- 📦 **Auto Package Installation**: Automatically installs packages from requirements.txt
- 📋 **Environment Listing**: View all virtual environments with detailed information
- 🗑️ **Clean Removal**: Remove environments with confirmation prompts
- 🐚 **Shell Integration**: Drop into activated environments with `venv_shell`
- 🔄 **Backward Compatible**: Works with existing bash scripts
- 🎯 **Cross-Platform**: Works on Linux, macOS, and Windows

## 🚀 Quick Start

### Installation

#### Quick Install (Recommended)
```bash
curl -sSL https://raw.githubusercontent.com/spohaver/venv-manager/main/install.sh | bash
```

#### Manual Installation
1. Clone the repository:
```bash
git clone https://github.com/spohaver/venv-manager.git
cd venv-manager
```

2. Make the script executable:
```bash
chmod +x venv-manager
```

3. (Optional) Add to PATH for global access:
```bash
echo 'export PATH="$HOME/venv-manager:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Basic Usage

```bash
# Create a virtual environment (uses current directory name)
./venv-manager

# Create with specific name
./venv-manager --name myproject

# List all environments
./venv-manager list

# Remove an environment
./venv-manager remove --name myproject
```

## 📚 Available Tools

### 🎯 venv-manager (Main Tool)
The comprehensive Python-based virtual environment manager with full lifecycle management.

**Features:**
- Automatic venv module detection with helpful error messages
- Flexible directory structure with sensible defaults
- Intelligent package management and comparison
- Cross-platform compatibility
- Comprehensive error handling
- Object-oriented design for maintainability

**Usage:**
```bash
# CREATE VIRTUAL ENVIRONMENTS
# Basic usage - uses current directory name as venv name
./venv-manager

# Specify virtual environment name
./venv-manager --name myproject

# Use custom base directory
./venv-manager --base-dir /opt/venvs

# Use custom requirements file
./venv-manager --requirements requirements-dev.txt

# Combine options with verbose output
./venv-manager --name myproject --base-dir ~/venvs --requirements requirements-dev.txt --verbose

# Explicit create command (same as above)
./venv-manager create --name myproject

# LIST VIRTUAL ENVIRONMENTS
# Basic list - shows summary
./venv-manager list

# Detailed list - shows full information
./venv-manager list --detailed

# List from custom base directory
./venv-manager list --base-dir /opt/venvs

# REMOVE VIRTUAL ENVIRONMENTS
# Remove with confirmation prompt
./venv-manager remove --name myproject

# Force remove without confirmation
./venv-manager remove --name myproject --force

# Remove from custom base directory
./venv-manager remove --name myproject --base-dir /opt/venvs
```

**Commands:**
- `create` (default): Create or update a virtual environment
- `list`: List all virtual environments with summary information
- `remove`: Remove a virtual environment

**Automatic Shell Activation:**
When you create a virtual environment, the script automatically creates a `venv_shell` script that you can use to activate the environment in a new shell:

```bash
# After creating an environment, use this to activate it in a new shell
./venv_shell
```

This is especially useful for dropping into an activated environment without manually running the `source` command.

**Command Line Options:**

**Create Command:**
- `--name, -n`: Name of the virtual environment (default: current directory name)
- `--base-dir, -b`: Base directory for virtual environments (default: ~/virtual_environments)
- `--requirements, -r`: Path to requirements.txt file (default: ./requirements.txt)
- `--verbose, -v`: Enable verbose output

**List Command:**
- `--base-dir, -b`: Base directory for virtual environments (default: ~/virtual_environments)
- `--detailed, -d`: Show detailed information about each environment

**Remove Command:**
- `--name, -n`: Name of the virtual environment to remove (required)
- `--base-dir, -b`: Base directory for virtual environments (default: ~/virtual_environments)
- `--force, -f`: Remove without confirmation prompt

### 2. setupvenv.sh (Legacy - Bash Version)
The original bash script for basic virtual environment setup.

**Usage:**
```bash
# Default location (~/virtual_environments)
./setupvenv.sh

# Custom location
./setupvenv.sh ~/custom/venv/path
```

## Quick Start

1. **Add required Python modules to requirements.txt**
   ```bash
   # Create requirements.txt manually or from existing environment
   pip freeze > requirements.txt
   ```

2. **Run the setup script**
   ```bash
   # Using the Python version (recommended)
   ./setupvenv.py
   
   # Or using the bash version
   ./setupvenv.sh
   ```

3. **Activate the virtual environment**
   ```bash
   # Use the generated activation script
   ./venv_shell
   
   # Or activate manually
   source ~/virtual_environments/$(basename $PWD)/bin/activate
   ```

## Requirements

- **Python 3.6+** with venv module installed
- **For Ubuntu/Debian:** `sudo apt install python3-venv`
- **For CentOS/RHEL:** `sudo yum install python3-venv`
- **For macOS/Windows:** venv is included with Python 3.3+

## Files Created

- `~/virtual_environments/{project_name}/`: Virtual environment directory (or custom base directory)
- `.venvlocation`: Tracks the virtual environment path
- `venv_shell`: Shell script for easy activation

## Tips

- **Quick requirements.txt generation:** `pip freeze > requirements.txt`
- **View current packages:** `pip list` or `pip freeze`
- **Update existing environment:** Just run the setup script again
- **Check virtual environment location:** `cat .venvlocation`

## Advanced Features

### Environment Management

The Python script provides comprehensive environment management capabilities:

- **List all environments**: See all virtual environments with their sizes, creation dates, and package counts
- **Detailed environment info**: View Python version, installed packages, and full environment details
- **Safe removal**: Interactive confirmation before deletion with environment details preview
- **Force removal**: Skip confirmation for automated scripts
- **Cross-directory management**: Work with virtual environments in different base directories

### Example Workflows

**Development Setup:**
```bash
# Set up a new project environment
./setupvenv.py --name myproject --requirements requirements-dev.txt

# Check all your environments
./setupvenv.py list --detailed

# Work on the project...
source ~/virtual_environments/myproject/bin/activate

# Clean up when done
./setupvenv.py remove --name myproject
```

**Environment Maintenance:**
```bash
# See what environments exist and their sizes
./setupvenv.py list

# Clean up old environments
./setupvenv.py remove --name old-project --force
./setupvenv.py remove --name another-old-project --force

# Check remaining environments
./setupvenv.py list --detailed
```

## Migration from Bash to Python Script

If you're currently using the bash version and want to switch to the Python version:

1. The Python script will detect existing virtual environments created by the bash script
2. It maintains compatibility with the same directory structure
3. All existing `.venvlocation` files will continue to work
4. The `venv_shell` activation script remains the same
5. New `list` and `remove` commands work with existing environments

## Comparison: Bash vs Python Script

| Feature | setupvenv.sh | setupvenv.py |
|---------|--------------|--------------|
| **Create environments** | ✅ Basic | ✅ Advanced with validation |
| **List environments** | ❌ | ✅ Summary and detailed views |
| **Remove environments** | ❌ | ✅ With confirmation and force options |
| **Environment info** | ❌ | ✅ Size, packages, Python version |
| **Argument parsing** | Positional only | Named arguments with help |
| **Error handling** | Basic | Comprehensive with helpful messages |
| **Cross-platform** | Linux/macOS only | Linux/macOS/Windows |
| **Package comparison** | Simple diff | Intelligent comparison |
| **Documentation** | Comments | Docstrings + help text |
| **Maintainability** | Moderate | High (OOP structure) |
| **Dependencies** | bash, python3 | python3 only |
| **Backward compatibility** | N/A | ✅ Maintains compatibility with bash version |

## 📚 Documentation

- **[CHANGELOG.md](CHANGELOG.md)** - Complete project history and version notes
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Guide for contributors
- **[LICENSE](LICENSE)** - MIT License details

## 🏗️ Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and guidelines.

Quick development setup:
```bash
make install  # Install development dependencies
make test     # Run tests
make demo     # Try out the tool
```