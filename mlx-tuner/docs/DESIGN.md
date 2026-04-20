# MLX Tuner - Design Patterns & SOLID Principles

## Design Patterns Used

### 1. Protocol-Based Dependency Injection

**Problem**: Tight coupling between components makes testing difficult.

**Solution**: Define protocol interfaces that describe what a class can do, not how it does it.

```python
# protocols.py
from typing import Protocol

class ModelLoaderProto(Protocol):
    """Protocol for model loading."""
    
    def load(self, name: str) -> "Model": ...
    def load_lora(self, base: "Model", adapter_path: str) -> "Model": ...

class DataLoaderProto(Protocol):
    """Protocol for data loading."""
    
    def load(self, path: str) -> list[dict]: ...
    def validate(self, data: list[dict]) -> bool: ...

class LoggerProto(Protocol):
    """Protocol for logging."""
    
    def info(self, msg: str, **kwargs) -> None: ...
    def error(self, msg: str, **kwargs) -> None: ...
```

**Usage in Production**:
```python
# training/trainer.py
class Trainer:
    def __init__(
        self,
        model_loader: ModelLoaderProto,
        data_loader: DataLoaderProto,
        logger: LoggerProto,
    ):
        self.model_loader = model_loader
        self.data_loader = data_loader
        self.logger = logger
```

**Usage in Tests**:
```python
# tests/test_trainer.py
class MockModelLoader:
    def load(self, name: str) -> MockModel:
        return MockModel()

class MockDataLoader:
    def load(self, path: str) -> list[dict]:
        return [{"text": "test"}]
    
    def validate(self, data: list[dict]) -> bool:
        return True

def test_trainer():
    trainer = Trainer(
        model_loader=MockModelLoader(),
        data_loader=MockDataLoader(),
        logger=MockLogger(),
    )
```

### 2. Factory Pattern for Model Creation

**Problem**: Complex object construction with many parameters.

**Solution**: Centralize model creation in factory functions.

```python
# models/loader.py
def create_model(
    name: str,
    adapter_path: str | None = None,
    lazy_load: bool = False,
) -> Model:
    """Factory function for creating models."""
    
    model = load_base_model(name, lazy_load)
    
    if adapter_path:
        model = load_adapter(model, adapter_path)
    
    return model
```

### 3. Strategy Pattern for Data Loading

**Problem**: Multiple data formats need different loading strategies.

**Solution**: Implement a common interface for all data loaders.

```python
# data/loaders.py
class JSONLLoader:
    """Strategy for JSONL format."""
    
    def load(self, path: str) -> list[dict]:
        with open(path) as f:
            return [json.loads(line) for line in f]
    
    def validate(self, data: list[dict]) -> bool:
        return all("text" in item for item in data)


class CSVLoader:
    """Strategy for CSV format."""
    
    def load(self, path: str) -> list[dict]:
        import csv
        with open(path) as f:
            return list(csv.DictReader(f))
    
    def validate(self, data: list[dict]) -> bool:
        return all("text" in item for item in data)


def get_loader(format: str) -> DataLoaderProto:
    """Factory for data loaders."""
    loaders = {
        "jsonl": JSONLLoader(),
        "csv": CSVLoader(),
    }
    return loaders[format]
```

### 4. Template Method Pattern for Training

**Problem**: Training loop has fixed structure but customizable steps.

**Solution**: Define skeleton in base class, let subclasses override specific steps.

```python
# training/trainer.py
class BaseTrainer:
    """Template for training."""
    
    def train(self, config: TrainConfig):
        self.setup()
        self.load_data()
        self.load_model()
        
        for step in range(config.steps):
            batch = self.get_batch()
            loss = self.forward_backward(batch)
            self.log_metrics(step, loss)
            
        self.save_checkpoint()
    
    # Override these in subclasses
    def setup(self): ...
    def get_batch(self): ...
    def forward_backward(self, batch): ...


class MLXTrainer(BaseTrainer):
    """MLX-specific training implementation."""
    
    def forward_backward(self, batch):
        # MLX-specific implementation
        ...
```

### 5. Builder Pattern for Configuration

**Problem**: Complex configuration with many optional parameters.

**Solution**: Fluent builder interface for configuration.

```python
# While we use Pydantic, the pattern is similar:
from pydantic import BaseModel, Field

class ModelConfig(BaseModel):
    name: str = "SmolLM-135M"
    path: str | None = None
    trust_remote_code: bool = False
    
    class Config:
        extra = "forbid"
```

## SOLID Principles Implementation

### Single Responsibility Principle (SRP)

Each module has one reason to change:

| Module | Responsibility | Reason to Change |
|--------|---------------|------------------|
| `config.py` | Configuration | New config options |
| `logging.py` | Logging setup | Logging format changes |
| `data/loaders.py` | Data loading | New data formats |
| `training/lora.py` | LoRA computation | LoRA algorithm changes |
| `convert/gguf.py` | Conversion | New output formats |

### Open/Closed Principle (OCP)

Open for extension, closed for modification:

```python
# Add new data formats without changing existing code:
class DataLoaderProto(Protocol):
    def load(self, path: str) -> list[dict]: ...

class ParquetLoader:
    """New loader for Parquet format."""
    
    def load(self, path: str) -> list[dict]:
        import pandas as pd
        return pd.read_parquet(path).to_dict("records")
```

### Liskov Substitution Principle (LSP)

Any implementation of a protocol can be substituted:

```python
# All these are interchangeable:
loader1: DataLoaderProto = JSONLLoader()
loader2: DataLoaderProto = CSVLoader()
loader3: DataLoaderProto = ParquetLoader()

# Can use any in trainer:
trainer = Trainer(model_loader=..., data_loader=loader1, ...)
trainer = Trainer(model_loader=..., data_loader=loader2, ...)
```

### Interface Segregation Principle (ISP)

Small, focused protocols:

```python
# Instead of one large interface:
# ❌ Bad
class LargeInterface(Protocol):
    def load(self): ...
    def save(self): ...
    def validate(self): ...
    def transform(self): ...

# ✅ Good - small focused interfaces
class Loader(Protocol):
    def load(self): ...

class Saver(Protocol):
    def save(self): ...

class Validator(Protocol):
    def validate(self): ...
```

### Dependency Inversion Principle (DIP)

Depend on abstractions, not concretions:

```python
# ❌ Bad - depends on concrete class
class Trainer:
    def __init__(self):
        self.model_loader = MLXModelLoader()  # Hard dependency

# ✅ Good - depends on protocol
class Trainer:
    def __init__(self, model_loader: ModelLoaderProto):
        self.model_loader = model_loader  # Depends on abstraction
```

## Testing Strategy

### Unit Tests

Test individual components in isolation:

```python
# tests/test_lora.py
def test_rs_lora_scaling_standard():
    """Test RSLoRA scaling formula."""
    rank = 8
    alpha = 8
    scale = rs_lora_scaling(rank, alpha)
    assert scale == 10.0
```

### Integration Tests

Test component interactions:

```python
# tests/test_loaders.py
def test_jsonl_loader_valid(tmp_path):
    """Test JSONL loader with valid data."""
    test_file = tmp_path / "test.jsonl"
    test_file.write_text('{"text": "hello"}\n{"text": "world"}')
    
    loader = JSONLLoader()
    data = loader.load(str(test_file))
    
    assert len(data) == 2
    assert data[0]["text"] == "hello"
```

### Mocking Strategy

Use mocks for external dependencies:

```python
# Mock MLX to avoid GPU calls in tests
@patch("mlx_tuner.models.loader.mlx")
def test_model_loading(mock_mlx):
    mock_mlx.load.return_value = MockModel()
    loader = MLXModelLoader()
    model = loader.load("test-model")
    assert isinstance(model, MockModel)
```

## Error Handling Patterns

### Custom Exception Hierarchy

```python
class MLXTunerError(Exception):
    """Base exception for all errors."""
    pass

class ModelLoadError(MLXTunerError):
    """Model loading failed."""
    pass

class DataLoadError(MLXTunerError):
    """Data loading failed."""
    pass

class TrainingError(MLXTunerError):
    """Training failed."""
    pass

class ConversionError(MLXTunerError):
    """Model conversion failed."""
    pass
```

### Error Context

```python
try:
    model = loader.load(model_name)
except ModelLoadError as e:
    raise ModelLoadError(
        f"Failed to load model: {model_name}"
    ) from e
```
