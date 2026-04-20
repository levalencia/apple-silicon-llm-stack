# MLX Tuner - Testing Guide

## Test Overview

| Category | Count | Location |
|----------|-------|----------|
| Unit Tests | 20 | `tests/` |
| Test Files | 4 | `test_config.py`, `test_loaders.py`, `test_lora.py`, `test_gguf.py` |

## Running Tests

### Quick Run

```bash
# Activate virtual environment
source /Users/luisvalencia/Documents/AdvancedLLMApp/.venv/bin/activate

# Run all tests
cd /Users/luisvalencia/Documents/mlx-tuner
python -m pytest
```

### Verbose Output

```bash
python -m pytest -v
```

### With Coverage

```bash
python -m pytest --cov=src/mlx_tuner --cov-report=html
```

### Specific Test File

```bash
python -m pytest tests/test_config.py -v
```

### Specific Test

```bash
python -m pytest tests/test_config.py::test_default_model_config -v
```

## Test Structure

```
tests/
├── conftest.py              # Shared fixtures
├── test_config.py           # Configuration tests (6 tests)
├── test_loaders.py          # Data loader tests (5 tests)
├── test_lora.py             # LoRA implementation tests (5 tests)
└── test_gguf.py             # GGUF converter tests (4 tests)
```

## Test Descriptions

### test_config.py

Tests for configuration management:

| Test | Description |
|------|-------------|
| `test_default_model_config` | Verify default model configuration |
| `test_default_lora_config` | Verify default LoRA settings |
| `test_lora_alpha_ratio` | Test alpha-to-rank ratio calculation |
| `test_default_training_config` | Verify default training parameters |
| `test_app_config` | Test complete app configuration |
| `test_env_override` | Test environment variable overrides |

### test_loaders.py

Tests for data loading:

| Test | Description |
|------|-------------|
| `test_jsonl_loader_valid` | Load valid JSONL file |
| `test_jsonl_loader_validate` | Validate JSONL data structure |
| `test_jsonl_loader_empty_lines` | Handle empty lines gracefully |
| `test_jsonl_loader_invalid_json` | Handle malformed JSON |
| `test_jsonl_loader_not_found` | Handle missing files |

### test_lora.py

Tests for LoRA implementation:

| Test | Description |
|------|-------------|
| `test_rs_lora_scaling_standard` | Test standard RSLoRA scaling |
| `test_rs_lora_scaling_different` | Test different rank/alpha values |
| `test_rs_lora_scaling_matches_standard` | Verify scaling matches formula |
| `test_apply_lora_default_params` | Test default LoRA application |
| `test_apply_lora_custom_target_modules` | Test custom target modules |

### test_gguf.py

Tests for GGUF conversion:

| Test | Description |
|------|-------------|
| `test_build_gguf_filename` | Test GGUF filename generation |
| `test_gguf_converter_default_quantization` | Test default quantization |
| `test_gguf_converter_custom_quantization` | Test custom quantization |
| `test_gguf_converter_imatrix` | Test importance matrix |

## Writing Tests

### Basic Test Structure

```python
# tests/test_example.py
import pytest
from mlx_tuner.module import function_to_test

def test_basic_functionality():
    """Description of what this test does."""
    result = function_to_test(input_value)
    assert result == expected_value
```

### Using Fixtures

```python
# tests/conftest.py
import pytest

@pytest.fixture
def sample_config():
    return {
        "model": "SmolLM-135M",
        "lora_rank": 8,
    }

# tests/test_example.py
def test_with_fixture(sample_config):
    assert sample_config["lora_rank"] == 8
```

### Parameterized Tests

```python
@pytest.mark.parametrize("rank,alpha,expected_scale", [
    (8, 8, 10.0),
    (16, 16, 10.0),
    (4, 8, 20.0),
])
def test_lora_scaling(rank, alpha, expected_scale):
    from mlx_tuner.training.lora import rs_lora_scaling
    scale = rs_lora_scaling(rank, alpha)
    assert scale == expected_scale
```

### Mocking External Dependencies

```python
from unittest.mock import patch

@patch("mlx_tuner.models.loader.mlx")
def test_model_loading(mock_mlx):
    # Mock MLX behavior
    mock_mlx.load.return_value = MockModel()
    
    # Test
    from mlx_tuner.models.loader import load_model
    model = load_model("test-model")
    
    # Assert
    assert isinstance(model, MockModel)
```

## Test Best Practices

### 1. Test One Thing Per Test

```python
# ❌ Bad - testing multiple things
def test_config():
    assert config.model == "SmolLM"
    assert config.lora_rank == 8
    assert config.learning_rate == 2e-4

# ✅ Good - one assertion per test
def test_default_model():
    assert config.model == "SmolLM"

def test_default_lora_rank():
    assert config.lora_rank == 8

def test_default_learning_rate():
    assert config.learning_rate == 2e-4
```

### 2. Use Descriptive Names

```python
# ❌ Bad
def test1(): ...

# ✅ Good
def test_jsonl_loader_throws_on_missing_file(): ...
```

### 3. Follow AAA Pattern

```python
def test_something():
    # Arrange
    setup_state()
    
    # Act
    result = action()
    
    # Assert
    assert result == expected
```

### 4. Test Edge Cases

```python
def test_empty_jsonl_file(tmp_path):
    """Handle empty JSONL file."""
    file = tmp_path / "empty.jsonl"
    file.write_text("")
    
    loader = JSONLLoader()
    data = loader.load(str(file))
    
    assert data == []
```

## CI/CD Integration

### GitHub Actions Example

```yaml
# .github/workflows/test.yml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: macos-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          python -m venv venv
          source venv/bin/activate
          pip install -e .
          pip install pytest pytest-cov
      
      - name: Run tests
        run: |
          source venv/bin/activate
          pytest --cov=src --cov-report=xml
```

## Coverage Reports

### Generate HTML Report

```bash
python -m pytest --cov=src/mlx_tuner --cov-report=html
open htmlcov/index.html
```

### Generate XML for CI

```bash
python -m pytest --cov=src/mlx_tuner --cov-report=xml
```

### Coverage Targets

| Module | Target |
|--------|--------|
| config.py | 100% |
| data/loaders.py | 90% |
| training/lora.py | 90% |
| convert/gguf_converter.py | 85% |

## Debugging Failed Tests

### Show Local Variables

```bash
pytest -l
```

### Drop into PDB on Failure

```bash
pytest --pdb
```

### Show Test Summary

```bash
pytest -v --tb=short
```

### Run Only Last Failed Tests

```bash
pytest --lf
```
