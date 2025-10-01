#!/usr/bin/env python3
"""
Python Virtual Environment Setup Script

This script creates and manages Python virtual environments with automatic
package installation from requirements.txt files.
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path
import venv
import tempfile
import shutil
from datetime import datetime
import json


class VirtualEnvironmentSetup:
    """Handles virtual environment creation and management."""

    def __init__(self, venv_name: str, base_dir: Path, requirements_file: Path):
        self.venv_name = venv_name
        self.base_dir = base_dir
        self.requirements_file = requirements_file
        self.venv_path = base_dir / venv_name
        self.venvlocation_file = Path.cwd() / ".venvlocation"

    def check_venv_module(self) -> bool:
        """Check if the venv module is available."""
        try:
            import venv

            return True
        except ImportError:
            print("Error: Python venv module is not available.")
            print("Please install it using your system package manager.")
            print("For Ubuntu/Debian: sudo apt install python3-venv")
            print("For CentOS/RHEL: sudo yum install python3-venv")
            return False

    def create_venv_location_file(self) -> None:
        """Create .venvlocation file to track virtual environment path."""
        try:
            with open(self.venvlocation_file, "w") as f:
                f.write(str(self.venv_path) + "\n")
            print(f"Created {self.venvlocation_file}")
        except IOError as e:
            print(f"Warning: Could not create .venvlocation file: {e}")

    def get_installed_packages(self) -> set:
        """Get list of currently installed packages in the virtual environment."""
        pip_executable = self.venv_path / "bin" / "pip"
        try:
            result = subprocess.run(
                [str(pip_executable), "freeze"],
                capture_output=True,
                text=True,
                check=True,
            )
            return (
                set(result.stdout.strip().split("\n"))
                if result.stdout.strip()
                else set()
            )
        except subprocess.CalledProcessError as e:
            print(f"Error getting installed packages: {e}")
            return set()

    def get_required_packages(self) -> set:
        """Get list of required packages from requirements.txt."""
        if not self.requirements_file.exists():
            print(f"Requirements file {self.requirements_file} not found.")
            return set()

        try:
            with open(self.requirements_file, "r") as f:
                # Filter out comments and empty lines
                packages = set()
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        packages.add(line)
                return packages
        except IOError as e:
            print(f"Error reading requirements file: {e}")
            return set()

    def install_packages(self) -> bool:
        """Install packages from requirements.txt."""
        if not self.requirements_file.exists():
            print(
                f"No requirements.txt found at {self.requirements_file}, skipping package installation."
            )
            return True

        pip_executable = self.venv_path / "bin" / "pip"

        try:
            # Upgrade pip first
            print("Upgrading pip...")
            subprocess.run([str(pip_executable), "install", "-U", "pip"], check=True)

            # Install packages from requirements.txt
            print(f"Installing packages from {self.requirements_file}...")
            subprocess.run(
                [str(pip_executable), "install", "-r", str(self.requirements_file)],
                check=True,
            )

            return True
        except subprocess.CalledProcessError as e:
            print(f"Error installing packages: {e}")
            return False

    def create_virtual_environment(self) -> bool:
        """Create a new virtual environment."""
        try:
            # Ensure base directory exists
            self.base_dir.mkdir(parents=True, exist_ok=True)
            print(f"Created base directory: {self.base_dir}")

            print(f"Creating virtual environment in {self.venv_path}")
            venv.create(self.venv_path, with_pip=True)

            # Create .venvlocation file
            self.create_venv_location_file()

            # Install packages
            return self.install_packages()

        except Exception as e:
            print(f"Error creating virtual environment: {e}")
            return False

    def update_virtual_environment(self) -> bool:
        """Update existing virtual environment packages if needed."""
        print("Virtual environment already exists, checking packages...")

        # Create .venvlocation file if it doesn't exist
        if not self.venvlocation_file.exists():
            self.create_venv_location_file()

        # Compare installed vs required packages
        installed = self.get_installed_packages()
        required = self.get_required_packages()

        if not required:
            print("No requirements.txt found or it's empty.")
            return True

        # Simple check - if packages don't match, reinstall
        # This is a simplified comparison; in practice, version matching would be more complex
        if installed != required:
            print("Package requirements have changed, installing/updating packages...")
            return self.install_packages()
        else:
            print("All required packages are already installed.")
            return True

    def setup(self) -> bool:
        """Main setup method."""
        if not self.check_venv_module():
            return False

        # Check if virtual environment already exists
        activate_script = self.venv_path / "bin" / "activate"

        if activate_script.exists():
            success = self.update_virtual_environment()
        else:
            success = self.create_virtual_environment()

        if success:
            print("\nVirtual Environment setup completed!")
            print(f"Virtual environment location: {self.venv_path}")
            print(f"To activate: source {activate_script}")
            print(f"To deactivate: deactivate")

            # Create a simple activation script
            self.create_activation_script()

        return success

    def create_activation_script(self) -> None:
        """Create a simple activation script similar to venv_shell."""
        script_path = Path.cwd() / "venv_shell"
        try:
            with open(script_path, "w") as f:
                f.write(
                    f"""#!/bin/bash
# Automatically generated virtual environment activation script
# This script opens a NEW shell with the virtual environment activated
echo "Starting new shell with virtual environment '{self.venv_path.name}' activated..."
echo "Type 'exit' to return to your original shell."
echo "Virtual environment path: {self.venv_path}"
echo ""
cd "{Path.cwd()}"
source {self.venv_path}/bin/activate
exec "$SHELL"
"""
                )
            script_path.chmod(0o755)
            print(f"Created activation script: {script_path}")
            print(
                "Run './venv_shell' to activate the virtual environment in a NEW shell"
            )
            print("(Type 'exit' in the new shell to return to your current shell)")
        except IOError as e:
            print(f"Warning: Could not create activation script: {e}")

    def get_venv_info(self) -> dict:
        """Get information about the virtual environment."""
        if not self.venv_path.exists():
            return {}

        info = {
            "name": self.venv_name,
            "path": str(self.venv_path),
            "created": None,
            "size": None,
            "python_version": None,
            "packages_count": 0,
            "packages": [],
        }

        try:
            # Get creation time (approximate)
            stat = self.venv_path.stat()
            info["created"] = datetime.fromtimestamp(stat.st_ctime).strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            # Get directory size
            size = sum(
                f.stat().st_size for f in self.venv_path.rglob("*") if f.is_file()
            )
            info["size"] = self._format_size(size)

            # Get Python version
            python_executable = self.venv_path / "bin" / "python"
            if python_executable.exists():
                result = subprocess.run(
                    [str(python_executable), "--version"],
                    capture_output=True,
                    text=True,
                )
                if result.returncode == 0:
                    info["python_version"] = result.stdout.strip()

            # Get installed packages
            packages = self.get_installed_packages()
            info["packages_count"] = len(packages)
            info["packages"] = sorted(list(packages))

        except Exception as e:
            print(f"Warning: Could not get complete info for {self.venv_name}: {e}")

        return info

    @staticmethod
    def _format_size(size_bytes: int) -> str:
        """Format size in bytes to human readable format."""
        for unit in ["B", "KB", "MB", "GB"]:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"

    def remove_environment(self, force: bool = False) -> bool:
        """Remove the virtual environment."""
        if not self.venv_path.exists():
            print(
                f"Virtual environment '{self.venv_name}' does not exist at {self.venv_path}"
            )
            return False

        if not force:
            # Show environment info before deletion
            info = self.get_venv_info()
            print(f"\nEnvironment to be deleted:")
            print(f"  Name: {info.get('name', 'Unknown')}")
            print(f"  Path: {info.get('path', 'Unknown')}")
            print(f"  Size: {info.get('size', 'Unknown')}")
            print(f"  Created: {info.get('created', 'Unknown')}")
            print(f"  Packages: {info.get('packages_count', 0)}")

            response = input(
                f"\nAre you sure you want to delete '{self.venv_name}'? [y/N]: "
            )
            if response.lower() not in ["y", "yes"]:
                print("Deletion cancelled.")
                return False

        try:
            # Remove the virtual environment directory
            shutil.rmtree(self.venv_path)
            print(f"Successfully removed virtual environment '{self.venv_name}'")

            # Remove .venvlocation file if it points to this environment
            if self.venvlocation_file.exists():
                try:
                    with open(self.venvlocation_file, "r") as f:
                        stored_path = f.read().strip()
                    if Path(stored_path) == self.venv_path:
                        self.venvlocation_file.unlink()
                        print("Removed .venvlocation file")
                except Exception as e:
                    print(f"Warning: Could not remove .venvlocation file: {e}")

            # Remove venv_shell if it exists and points to this environment
            venv_shell = Path.cwd() / "venv_shell"
            if venv_shell.exists():
                try:
                    with open(venv_shell, "r") as f:
                        content = f.read()
                    if str(self.venv_path) in content:
                        venv_shell.unlink()
                        print("Removed venv_shell activation script")
                except Exception as e:
                    print(f"Warning: Could not remove venv_shell script: {e}")

            return True

        except Exception as e:
            print(f"Error removing virtual environment: {e}")
            return False

    @staticmethod
    def list_environments(base_dir: Path, detailed: bool = False) -> None:
        """List all virtual environments in the base directory."""
        if not base_dir.exists():
            print(f"Base directory {base_dir} does not exist.")
            return

        # Find all virtual environment directories
        venv_dirs = []
        for item in base_dir.iterdir():
            if item.is_dir():
                # Check if it looks like a virtual environment
                if (item / "bin" / "activate").exists() or (
                    item / "Scripts" / "activate.bat"
                ).exists():
                    venv_dirs.append(item)

        if not venv_dirs:
            print(f"No virtual environments found in {base_dir}")
            return

        print(f"\nVirtual environments in {base_dir}:")
        print("=" * 60)

        for venv_dir in sorted(venv_dirs):
            dummy_setup = VirtualEnvironmentSetup(
                venv_dir.name, base_dir, Path.cwd() / "requirements.txt"
            )

            if detailed:
                info = dummy_setup.get_venv_info()
                print(f"\nName: {info.get('name', 'Unknown')}")
                print(f"Path: {info.get('path', 'Unknown')}")
                print(f"Created: {info.get('created', 'Unknown')}")
                print(f"Size: {info.get('size', 'Unknown')}")
                print(f"Python: {info.get('python_version', 'Unknown')}")
                print(f"Packages: {info.get('packages_count', 0)}")
                if info.get("packages"):
                    print("Installed packages:")
                    for pkg in info["packages"][:10]:  # Show first 10 packages
                        print(f"  - {pkg}")
                    if len(info["packages"]) > 10:
                        print(f"  ... and {len(info['packages']) - 10} more")
                print("-" * 40)
            else:
                info = dummy_setup.get_venv_info()
                print(
                    f"  {info.get('name', 'Unknown'):20} | "
                    f"{info.get('size', 'Unknown'):8} | "
                    f"{info.get('created', 'Unknown'):19} | "
                    f"{info.get('packages_count', 0):3} packages"
                )

        if not detailed:
            print(f"\nFound {len(venv_dirs)} virtual environment(s)")
            print("Use --detailed flag for more information")


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Manage Python virtual environments with automatic package installation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Commands:
  create (default)  Create or update a virtual environment
  list             List all virtual environments  
  remove           Remove a virtual environment

Examples:
  %(prog)s                                    # Create venv using current directory name
  %(prog)s --name myproject                   # Create venv named 'myproject'
  %(prog)s --base-dir /opt/venvs              # Use custom base directory
  %(prog)s --requirements /path/to/reqs.txt  # Use custom requirements file
  %(prog)s list                               # List all virtual environments
  %(prog)s list --detailed                    # List with detailed information
  %(prog)s remove --name myproject            # Remove specific environment
  %(prog)s remove --name myproject --force    # Remove without confirmation
        """,
    )

    # Subcommands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Create command (default)
    create_parser = subparsers.add_parser(
        "create", help="Create or update virtual environment"
    )
    create_parser.add_argument(
        "--name",
        "-n",
        type=str,
        help="Name of the virtual environment (default: current directory name)",
    )
    create_parser.add_argument(
        "--base-dir",
        "-b",
        type=Path,
        help="Base directory for virtual environments (default: ~/virtual_environments)",
    )
    create_parser.add_argument(
        "--requirements",
        "-r",
        type=Path,
        help="Path to requirements.txt file (default: ./requirements.txt)",
    )
    create_parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose output"
    )

    # List command
    list_parser = subparsers.add_parser("list", help="List virtual environments")
    list_parser.add_argument(
        "--base-dir",
        "-b",
        type=Path,
        help="Base directory for virtual environments (default: ~/virtual_environments)",
    )
    list_parser.add_argument(
        "--detailed",
        "-d",
        action="store_true",
        help="Show detailed information about each environment",
    )

    # Remove command
    remove_parser = subparsers.add_parser("remove", help="Remove virtual environment")
    remove_parser.add_argument(
        "--name",
        "-n",
        type=str,
        required=True,
        help="Name of the virtual environment to remove",
    )
    remove_parser.add_argument(
        "--base-dir",
        "-b",
        type=Path,
        help="Base directory for virtual environments (default: ~/virtual_environments)",
    )
    remove_parser.add_argument(
        "--force", "-f", action="store_true", help="Remove without confirmation prompt"
    )

    # For backward compatibility - if no subcommand is used, treat as create
    # We'll handle this in the main function

    return parser.parse_args()


def main() -> int:
    """Main function."""
    # Handle backward compatibility - if sys.argv doesn't contain known subcommands,
    # treat it as the old create mode
    subcommands = ["list", "remove", "create"]
    has_subcommand = any(cmd in sys.argv for cmd in subcommands)

    if not has_subcommand:
        # Backward compatibility mode - parse as old-style arguments
        return main_create_legacy()

    args = parse_arguments()

    # Set defaults
    base_dir = args.base_dir or Path.home() / "virtual_environments"

    try:
        command = args.command

        if command == "list":
            VirtualEnvironmentSetup.list_environments(base_dir, args.detailed)
            return 0

        elif command == "remove":
            venv_name = args.name
            if not venv_name:
                print("Error: Virtual environment name is required for remove command")
                return 1

            requirements_file = (
                Path.cwd() / "requirements.txt"
            )  # Dummy for remove operation
            venv_setup = VirtualEnvironmentSetup(venv_name, base_dir, requirements_file)
            success = venv_setup.remove_environment(args.force)
            return 0 if success else 1

        elif command == "create":
            # Original create functionality
            venv_name = args.name or Path.cwd().name
            requirements_file = args.requirements or Path.cwd() / "requirements.txt"

            if hasattr(args, "verbose") and args.verbose:
                print(f"Command: {command}")
                print(f"Virtual environment name: {venv_name}")
                print(f"Base directory: {base_dir}")
                print(f"Requirements file: {requirements_file}")
                print()

            # Create and run setup
            venv_setup = VirtualEnvironmentSetup(venv_name, base_dir, requirements_file)
            success = venv_setup.setup()
            return 0 if success else 1

        else:
            print(f"Unknown command: {command}")
            return 1

    except KeyboardInterrupt:
        print(f"\nOperation interrupted by user.")
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1


def main_create_legacy() -> int:
    """Main function for backward compatibility (create mode without subcommands)."""
    # Create a simple parser for backward compatibility
    parser = argparse.ArgumentParser(
        description="Set up Python virtual environments with automatic package installation",
        add_help=False,  # We'll handle help manually
    )

    parser.add_argument("--name", "-n", type=str)
    parser.add_argument("--base-dir", "-b", type=Path)
    parser.add_argument("--requirements", "-r", type=Path)
    parser.add_argument("--verbose", "-v", action="store_true")
    parser.add_argument("--help", "-h", action="store_true")

    # Parse known args to avoid errors with new subcommands
    args, unknown = parser.parse_known_args()

    if args.help:
        print_legacy_help()
        return 0

    # Set defaults
    venv_name = args.name or Path.cwd().name
    base_dir = args.base_dir or Path.home() / "virtual_environments"
    requirements_file = args.requirements or Path.cwd() / "requirements.txt"

    if args.verbose:
        print(f"Virtual environment name: {venv_name}")
        print(f"Base directory: {base_dir}")
        print(f"Requirements file: {requirements_file}")
        print()

    # Create and run setup
    venv_setup = VirtualEnvironmentSetup(venv_name, base_dir, requirements_file)

    try:
        success = venv_setup.setup()
        return 0 if success else 1
    except KeyboardInterrupt:
        print("\nSetup interrupted by user.")
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1


def print_legacy_help():
    """Print help for legacy mode."""
    print(
        """Python Virtual Environment Setup Tool

Usage: setupvenv.py [OPTIONS]

Create or update a Python virtual environment with automatic package installation.

Options:
  -n, --name NAME              Name of virtual environment (default: current directory name)
  -b, --base-dir PATH          Base directory for environments (default: ~/virtual_environments)  
  -r, --requirements PATH      Requirements file (default: ./requirements.txt)
  -v, --verbose               Enable verbose output
  -h, --help                  Show this help message

New Commands (use 'setupvenv.py COMMAND --help' for details):
  setupvenv.py create         Create or update virtual environment (default)
  setupvenv.py list           List all virtual environments
  setupvenv.py remove         Remove a virtual environment

Examples:
  setupvenv.py                               # Create using current directory name
  setupvenv.py --name myproject              # Create named environment
  setupvenv.py list                          # List all environments
  setupvenv.py remove --name myproject       # Remove environment"""
    )


if __name__ == "__main__":
    sys.exit(main())
