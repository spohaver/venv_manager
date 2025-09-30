"""
Basic tests for VirtualEnvironmentSetup class
"""
import pytest
import tempfile
import shutil
from pathlib import Path
import sys
import os

# Add the parent directory to the path to import the module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    # Import the class from the script (this is a bit hacky but works for testing)
    import subprocess
    result = subprocess.run([
        'python', '-c', 
        'exec(open("setupvenv.py").read()); print("Import successful")'
    ], cwd=os.path.join(os.path.dirname(__file__), '..'), 
    capture_output=True, text=True)
    
    if result.returncode == 0:
        print("Script can be executed successfully")
    else:
        print(f"Script execution failed: {result.stderr}")
except Exception as e:
    print(f"Import test failed: {e}")


class TestVenvManager:
    """Test cases for the venv-manager functionality"""
    
    def setup_method(self):
        """Set up test environment"""
        self.test_dir = Path(tempfile.mkdtemp())
        self.venv_base = self.test_dir / "test_venvs"
        
    def teardown_method(self):
        """Clean up test environment"""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
    
    def test_script_exists(self):
        """Test that the main script files exist"""
        script_dir = Path(__file__).parent.parent
        assert (script_dir / "venv-manager").exists()
        assert (script_dir / "setupvenv.py").exists()
        
    def test_script_is_executable(self):
        """Test that the main scripts are executable"""
        script_dir = Path(__file__).parent.parent
        venv_manager = script_dir / "venv-manager"
        assert os.access(venv_manager, os.X_OK)
        
    def test_help_command(self):
        """Test that help command works"""
        script_dir = Path(__file__).parent.parent
        result = subprocess.run([
            str(script_dir / "venv-manager"), "--help"
        ], capture_output=True, text=True)
        
        assert result.returncode == 0
        assert "Virtual Environment" in result.stdout or "usage:" in result.stdout.lower()


if __name__ == "__main__":
    pytest.main([__file__])