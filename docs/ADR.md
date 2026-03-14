# Architecture Decision Records - MLX Tuner

## ADR-001: Use Protocol-Based Dependency Injection

**Date**: 2026-03-13  
**Status**: Accepted

### Context

We need a testable architecture that allows:
- Easy mocking of external dependencies (MLX, file system)
- Swapping implementations without code changes
- Clear interfaces between components

### Decision

Use Python's Protocol class (PEP 544) for dependency injection.

```python
from typing import Protocol

class ModelLoaderProto(Protocol):
    def load(self, name: str) -> Model: ...

class DataLoaderProto(Protocol):
    def load(self, path: str) -> list[dict]: ...
```

### Consequences

**Positive**:
- Clear contracts between components
- Easy mocking in tests
- IDE support via type hints

**Negative**:
- Additional abstraction overhead
- Need to maintain protocol definitions

---

## ADR-002: Use Pydantic for Configuration

**Date**: 2026-03-13  
**Status**: Accepted

### Context

Configuration needs to be:
- Type-safe with validation
- Loadable from environment variables
- Serializable to/from files

### Decision

Use Pydantic with pydantic-settings.

```python
from pydantic_settings import BaseSettings

class AppConfig(BaseSettings):
    model_name: str = "SmolLM-135M"
    lora_rank: int = 8
    
    class Config:
        env_prefix = "APP_"
```

### Consequences

**Positive**:
- Automatic validation
- Environment variable support
- Type coercion

**Negative**:
- Runtime overhead (minimal)
- Additional dependency

---

## ADR-003: Use structlog for Structured Logging

**Date**: 2026-03-13  
**Status**: Accepted

### Context

Production debugging requires:
- JSON output for log aggregation
- Contextual logging with extra fields
- Multiple output handlers

### Decision

Use structlog for all logging.

```python
import structlog

structlog.configure(
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ],
)

log = structlog.get_logger()
log.info("training_start", model="SmolLM-135M", rank=8)
```

### Consequences

**Positive**:
- JSON output for production
- Easy filtering/searching
- Consistent format

**Negative**:
- Less readable in console (use dev renderer for dev)

---

## ADR-004: Use RSLoRA (Rank-Stabilized LoRA)

**Date**: 2026-03-13  
**Status**: Accepted

### Context

Standard LoRA can be unstable with high ranks. We need:
- Stable training at various ranks
- Consistent scaling across configurations

### Decision

Implement RSLoRA scaling formula:

```python
def rs_lora_scaling(rank: int, alpha: int) -> float:
    """RSLoRA scaling factor."""
    return alpha / rank if rank > 0 else 1.0
```

### Consequences

**Positive**:
- More stable training
- Better convergence
- Works well with higher ranks

**Negative**:
- Slightly different from original LoRA paper

---

## ADR-005: Support GGUF Export

**Date**: 2026-03-13  
**Status**: Accepted

### Context

Fine-tuned models need to run efficiently on:
- llama.cpp for inference
- Go gateway (metal-inference-core)
- Various deployment targets

### Decision

Implement GGUF conversion with quantization support:

```python
class GGUFConverter:
    def convert(
        self,
        model_path: str,
        output_path: str,
        quantization: str = "q4_k_m",
    ) -> None:
        """Convert to GGUF with specified quantization."""
```

### Consequences

**Positive**:
- Wide compatibility
- Efficient inference
- Reduced model size

**Negative**:
- Quantization can reduce quality
- Conversion time

---

## ADR-006: Use Makefile for Common Tasks

**Date**: 2026-03-13  
**Status**: Accepted

### Context

Users need simple commands for:
- Installation
- Training
- Evaluation
- Export

### Decision

Provide Makefile with documented targets:

```makefile
install:
	pip install -e .

train:
	python -m mlx_tuner train

fuse:
	python -m mlx_tuner fuse

convert:
	python -m mlx_tuner convert
```

### Consequences

**Positive**:
- Easy to remember commands
- Consistent interface
- Works across platforms

**Negative**:
- Less flexible than direct Python calls

---

## ADR-007: Use pytest for Testing

**Date**: 2026-03-13  
**Status**: Accepted

### Context

Need testing framework with:
- Good fixture support
- Parameterized tests
- Coverage reporting

### Decision

Use pytest.

```bash
pytest tests/ -v --cov=src
```

### Consequences

**Positive**:
- Rich ecosystem
- Good plugin support
- Easy to write tests

**Negative**:
- Additional dependency
