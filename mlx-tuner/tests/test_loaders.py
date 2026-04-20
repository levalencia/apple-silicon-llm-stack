"""Tests for data loaders."""

import json
from pathlib import Path

import pytest

from mlx_tuner.data.loaders import JSONLDatasetLoader


def test_jsonl_loader_valid(tmp_path):
    """Test JSONL loader with valid data."""
    data_file = tmp_path / "test.jsonl"

    with open(data_file, "w") as f:
        f.write(json.dumps({"messages": [{"role": "user", "content": "Hello"}]}) + "\n")
        f.write(json.dumps({"messages": [{"role": "user", "content": "World"}]}) + "\n")

    loader = JSONLDatasetLoader()
    data = loader.load(data_file)

    assert len(data) == 2
    assert data[0]["messages"][0]["role"] == "user"


def test_jsonl_loader_validate():
    """Test JSONL validation."""
    loader = JSONLDatasetLoader()

    valid_data = [{"messages": [{"role": "user", "content": "test"}]}]
    assert loader.validate(valid_data) is True

    invalid_data = [{"text": "no messages key"}]
    assert loader.validate(invalid_data) is False

    assert loader.validate([]) is False


def test_jsonl_loader_empty_lines(tmp_path):
    """Test JSONL loader handles empty lines."""
    data_file = tmp_path / "test.jsonl"

    with open(data_file, "w") as f:
        f.write(json.dumps({"messages": [{"role": "user", "content": "Hello"}]}) + "\n")
        f.write("\n")
        f.write(json.dumps({"messages": [{"role": "user", "content": "World"}]}) + "\n")

    loader = JSONLDatasetLoader()
    data = loader.load(data_file)

    assert len(data) == 2


def test_jsonl_loader_invalid_json(tmp_path):
    """Test JSONL loader skips invalid JSON."""
    data_file = tmp_path / "test.jsonl"

    with open(data_file, "w") as f:
        f.write(json.dumps({"messages": [{"role": "user", "content": "Hello"}]}) + "\n")
        f.write("invalid json\n")
        f.write(json.dumps({"messages": [{"role": "user", "content": "World"}]}) + "\n")

    loader = JSONLDatasetLoader()
    data = loader.load(data_file)

    assert len(data) == 2


def test_jsonl_loader_not_found():
    """Test JSONL loader raises error for missing file."""
    loader = JSONLDatasetLoader()

    with pytest.raises(FileNotFoundError):
        loader.load(Path("/nonexistent/file.jsonl"))
