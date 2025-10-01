"""
Comprehensive tests for the venv-manager functionality
"""

import pytest
import tempfile
import shutil
import subprocess
import os
import json
from pathlib import Path


class TestVenvManager:
    """Test cases for the venv-manager functionality"""

    def setup_method(self):
        """Set up test environment"""
        self.test_dir = Path(tempfile.mkdtemp())
        self.venv_base = self.test_dir / "test_venvs"
        self.script_dir = Path(__file__).parent.parent

    def teardown_method(self):
        """Clean up test environment"""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def run_venv_manager(self, args, expect_success=True):
        """Helper to run venv-manager command"""
        cmd = [str(self.script_dir / "venv-manager")] + args
        result = subprocess.run(
            cmd, capture_output=True, text=True, cwd=self.script_dir
        )

        if expect_success:
            if result.returncode != 0:
                print(f"Command failed: {' '.join(cmd)}")
                print(f"STDOUT: {result.stdout}")
                print(f"STDERR: {result.stderr}")
            assert result.returncode == 0, f"Command failed: {result.stderr}"

        return result

    def test_script_exists(self):
        """Test that the main script files exist"""
        assert (self.script_dir / "venv-manager").exists()
        assert (self.script_dir / "setupvenv.py").exists()
        assert (self.script_dir / "setupvenv.sh").exists()

    def test_script_is_executable(self):
        """Test that the main scripts are executable"""
        venv_manager = self.script_dir / "venv-manager"
        assert os.access(venv_manager, os.X_OK)

    def test_help_command(self):
        """Test that help command works"""
        result = self.run_venv_manager(["--help"])
        assert (
            "Virtual Environment" in result.stdout or "usage:" in result.stdout.lower()
        )

    def test_help_subcommands(self):
        """Test help for subcommands"""
        for cmd in ["create", "list", "remove"]:
            result = self.run_venv_manager([cmd, "--help"])
            assert "help" in result.stdout.lower() or "usage" in result.stdout.lower()

    def test_list_empty(self):
        """Test listing when no environments exist"""
        result = self.run_venv_manager(["list", "--base-dir", str(self.venv_base)])
        assert "Found 0 virtual environment" in result.stdout

    def test_create_environment(self):
        """Test creating a virtual environment"""
        env_name = "test-create-env"
        result = self.run_venv_manager(
            [
                "create",
                "--name",
                env_name,
                "--base-dir",
                str(self.venv_base),
                "--verbose",
            ]
        )

        assert "Virtual Environment setup completed" in result.stdout
        assert (self.venv_base / env_name).exists()
        assert (self.venv_base / env_name / "bin" / "activate").exists()

    def test_create_and_list(self):
        """Test creating environment and then listing it"""
        env_name = "test-list-env"

        # Create environment
        self.run_venv_manager(
            ["create", "--name", env_name, "--base-dir", str(self.venv_base)]
        )

        # List environments
        result = self.run_venv_manager(["list", "--base-dir", str(self.venv_base)])
        assert env_name in result.stdout
        assert "Found 1 virtual environment" in result.stdout

    def test_list_detailed(self):
        """Test detailed listing"""
        env_name = "test-detailed-env"

        # Create environment
        self.run_venv_manager(
            ["create", "--name", env_name, "--base-dir", str(self.venv_base)]
        )

        # List detailed
        result = self.run_venv_manager(
            ["list", "--base-dir", str(self.venv_base), "--detailed"]
        )
        assert env_name in result.stdout
        assert "Python version:" in result.stdout

    def test_remove_environment(self):
        """Test removing a virtual environment"""
        env_name = "test-remove-env"

        # Create environment
        self.run_venv_manager(
            ["create", "--name", env_name, "--base-dir", str(self.venv_base)]
        )

        # Verify it exists
        assert (self.venv_base / env_name).exists()

        # Remove it forcefully
        self.run_venv_manager(
            ["remove", "--name", env_name, "--base-dir", str(self.venv_base), "--force"]
        )

        # Verify it's gone
        assert not (self.venv_base / env_name).exists()

    def test_remove_nonexistent(self):
        """Test removing a non-existent environment"""
        result = self.run_venv_manager(
            [
                "remove",
                "--name",
                "nonexistent-env",
                "--base-dir",
                str(self.venv_base),
                "--force",
            ],
            expect_success=False,
        )

        assert result.returncode != 0
        assert (
            "not found" in result.stderr.lower()
            or "does not exist" in result.stderr.lower()
        )

    def test_activation_script_creation(self):
        """Test that activation script is created"""
        env_name = "test-activation-env"

        # Create environment
        result = self.run_venv_manager(
            ["create", "--name", env_name, "--base-dir", str(self.venv_base)]
        )

        # Check activation script was created
        assert "Created activation script" in result.stdout
        venv_shell_path = self.script_dir / "venv_shell"
        assert venv_shell_path.exists()

        # Check script content
        content = venv_shell_path.read_text()
        assert f"{self.venv_base}/{env_name}/bin/activate" in content
        assert "exec" in content

    def test_custom_requirements_file(self):
        """Test using a custom requirements file"""
        env_name = "test-custom-req-env"
        req_file = self.test_dir / "custom_requirements.txt"

        # Create custom requirements file
        req_file.write_text("requests>=2.25.0\n")

        # Create environment with custom requirements
        self.run_venv_manager(
            [
                "create",
                "--name",
                env_name,
                "--base-dir",
                str(self.venv_base),
                "--requirements",
                str(req_file),
            ]
        )

        # Environment should be created
        assert (self.venv_base / env_name).exists()

    def test_backward_compatibility(self):
        """Test backward compatibility - default behavior"""
        # Test that running without subcommand works (defaults to create)
        result = self.run_venv_manager(
            ["--name", "test-compat-env", "--base-dir", str(self.venv_base)]
        )

        assert "Virtual Environment setup completed" in result.stdout
        assert (self.venv_base / "test-compat-env").exists()

    def test_version_detection(self):
        """Test that the script can detect Python version"""
        env_name = "test-version-env"

        result = self.run_venv_manager(
            [
                "create",
                "--name",
                env_name,
                "--base-dir",
                str(self.venv_base),
                "--verbose",
            ]
        )

        # Should mention Python version somewhere in verbose output
        assert "python" in result.stdout.lower()


class TestFileStructure:
    """Test the project file structure and requirements"""

    def setup_method(self):
        self.project_root = Path(__file__).parent.parent

    def test_required_files_exist(self):
        """Test that all required project files exist"""
        required_files = [
            "venv-manager",
            "setupvenv.py",
            "setupvenv.sh",
            "requirements.txt",
            "requirements-dev.txt",
            "README.md",
            "LICENSE",
            "CHANGELOG.md",
            "CONTRIBUTING.md",
            ".gitignore",
            "setup.py",
            "Makefile",
        ]

        for filename in required_files:
            assert (
                self.project_root / filename
            ).exists(), f"Missing required file: {filename}"

    def test_github_workflow_exists(self):
        """Test that GitHub workflow exists"""
        workflow_file = self.project_root / ".github" / "workflows" / "ci.yml"
        assert workflow_file.exists()

    def test_requirements_files_valid(self):
        """Test that requirements files are valid"""
        req_files = ["requirements.txt", "requirements-dev.txt"]

        for req_file in req_files:
            path = self.project_root / req_file
            content = path.read_text()

            # Should not be empty and should have valid format
            assert content.strip()
            lines = [
                line.strip()
                for line in content.split("\n")
                if line.strip() and not line.startswith("#")
            ]
            assert len(lines) > 0, f"{req_file} appears to have no actual requirements"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
