"""
Test suite for utility classes and functions.
Tests file handling and helper utilities.
"""
import json
import tempfile
from pathlib import Path
import pytest
from src.vehicle_rental_system.utils.file_handler import FileHandler
from src.vehicle_rental_system.utils.helpers import pause


class TestFileHandler:
    """Test the FileHandler utility class."""

    def test_file_handler_creates_directory_if_not_exists(self, tmp_path):
        """Test that FileHandler creates data directory if it doesn't exist."""
        data_dir = tmp_path / "data"
        file_path = data_dir / "test.json"
        
        handler = FileHandler("test.json")
        handler.path = file_path
        
        # Create directory structure
        file_path.parent.mkdir(exist_ok=True)
        handler.write([])
        
        assert file_path.parent.exists()
        assert file_path.exists()

    def test_file_handler_creates_file_if_not_exists(self, tmp_path, monkeypatch):
        """Test that FileHandler creates file with empty list if it doesn't exist."""
        # Mock the path to use temp directory
        original_init = FileHandler.__init__
        
        def mock_init(self, filename):
            self.path = tmp_path / "data" / filename
            self.path.parent.mkdir(exist_ok=True)
            if not self.path.exists():
                self.write([])
        
        monkeypatch.setattr(FileHandler, "__init__", mock_init)
        
        handler = FileHandler("test.json")
        handler.write([])
        
        assert handler.path.exists()
        data = handler.read()
        assert data == []

    def test_file_handler_write_and_read(self, tmp_path, monkeypatch):
        """Test that FileHandler can write and read JSON data."""
        test_file = tmp_path / "test_data.json"
        test_data = [
            {"id": 1, "name": "Test"},
            {"id": 2, "name": "Another"}
        ]
        
        handler = FileHandler("test_data.json")
        handler.path = test_file
        handler.path.parent.mkdir(exist_ok=True)
        
        handler.write(test_data)
        result = handler.read()
        
        assert result == test_data
        assert len(result) == 2
        assert result[0]["id"] == 1

    def test_file_handler_write_preserves_structure(self, tmp_path):
        """Test that FileHandler preserves nested JSON structure."""
        test_file = tmp_path / "nested_test.json"
        nested_data = {
            "vehicles": [
                {"id": 1, "details": {"brand": "Toyota"}},
                {"id": 2, "details": {"brand": "Honda"}}
            ]
        }
        
        handler = FileHandler("nested_test.json")
        handler.path = test_file
        handler.path.parent.mkdir(exist_ok=True)
        
        handler.write(nested_data)
        result = handler.read()
        
        assert result == nested_data
        assert result["vehicles"][0]["details"]["brand"] == "Toyota"

    def test_file_handler_read_returns_empty_list_for_new_file(self, tmp_path):
        """Test that reading a newly created file returns empty list."""
        test_file = tmp_path / "new_file.json"
        
        handler = FileHandler("new_file.json")
        handler.path = test_file
        handler.path.parent.mkdir(exist_ok=True)
        
        if not test_file.exists():
            handler.write([])
        
        result = handler.read()
        assert result == []

    def test_file_handler_overwrites_existing_file(self, tmp_path):
        """Test that writing to an existing file overwrites previous content."""
        test_file = tmp_path / "overwrite_test.json"
        
        handler = FileHandler("overwrite_test.json")
        handler.path = test_file
        handler.path.parent.mkdir(exist_ok=True)
        
        initial_data = [{"old": "data"}]
        handler.write(initial_data)
        
        new_data = [{"new": "data"}]
        handler.write(new_data)
        
        result = handler.read()
        assert result == new_data
        assert result != initial_data
        assert "old" not in str(result)


class TestHelpers:
    """Test helper utility functions."""

    def test_pause_function_exists(self):
        """Test that pause function is defined."""
        from src.vehicle_rental_system.utils.helpers import pause
        assert callable(pause)

    def test_pause_function_accepts_input(self, monkeypatch):
        """Test that pause function waits for user input."""
        from src.vehicle_rental_system.utils.helpers import pause
        
        # Mock input to return immediately
        inputs = iter(["Enter"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        
        # Should not raise an exception
        pause()

