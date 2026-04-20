from pathlib import Path
from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class DatasetLoader(Protocol):
    """Protocol for dataset loading implementations."""

    def load(self, path: Path) -> list[dict[str, Any]]:
        """Load dataset from path."""
        ...

    def validate(self, data: list[dict[str, Any]]) -> bool:
        """Validate dataset format."""
        ...


@runtime_checkable
class ModelLoader(Protocol):
    """Protocol for model loading implementations."""

    def load(self, model_path: Path): ...
    def get_tokenizer(self): ...


@runtime_checkable
class Trainer(Protocol):
    """Protocol for training implementations."""

    def train(self, model: Any, dataset: Any, config: Any) -> None: ...
    def evaluate(self, model: Any, dataset: Any) -> dict[str, Any]: ...


@runtime_checkable
class GGUFConverter(Protocol):
    """Protocol for GGUF conversion implementations."""

    def convert(
        self, model_path: Path, output_path: Path, quantization: str
    ) -> Path: ...


@runtime_checkable
class CheckpointManager(Protocol):
    """Protocol for checkpoint management."""

    def save(self, model: Any, path: Path) -> None: ...
    def load(self, path: Path) -> Any: ...
    def list_checkpoints(self, dir: Path) -> list[Path]: ...


@runtime_checkable
class LossFunction(Protocol):
    """Protocol for loss computation."""

    def compute(self, logits: Any, targets: Any) -> float: ...


@runtime_checkable
class Quantizer(Protocol):
    """Protocol for model quantization."""

    def quantize(self, model: Any, bits: int) -> None: ...
    def dequantize(self, model: Any) -> None: ...
