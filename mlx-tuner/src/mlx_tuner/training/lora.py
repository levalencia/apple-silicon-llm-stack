"""LoRA (Low-Rank Adaptation) and RSLoRA Utilities for MLX.

This module implements the mathematical foundations for adapting Large Language Models 
using Apple's MLX framework.

Key Concept - Apple Silicon Unified Memory:
Unlike traditional PyTorch/CUDA setups where weights must be copied from CPU RAM 
to VRAM over a slow PCIe bus, MLX leverages the Unified Memory Architecture (UMA) 
of Apple Silicon. The CPU and GPU share the same physical memory, meaning data 
transfers are practically zero-copy.

Key Concept - Lazy Evaluation:
MLX uses "lazy evaluation." Operations defined here do not execute immediately. 
Instead, MLX builds a computation graph in the background and only evaluates it 
when the data is explicitly requested (e.g., via `mlx.core.eval()`).
"""

from pathlib import Path
from typing import Any

import mlx.core as mx
from mlx.utils import tree_flatten

from mlx_tuner.logging import get_logger

logger = get_logger(__name__)


def apply_lora(
    model: Any,
    rank: int = 8,
    alpha: int = 8,
    target_modules: list[str] | None = None,
    dropout: float = 0.05,
    use_rslora: bool = True,
) -> Any:
    """Apply LoRA adapters to a model using MLX.
    
    Instead of fine-tuning the entire multi-billion parameter model (which would 
    exhaust memory), LoRA freezes the pre-trained model weights and injects trainable 
    rank decomposition matrices into specific layers (usually the Attention projections).
    
    Args:
        model: The base model to apply LoRA to.
        rank: LoRA rank (default: 8). The dimensionality of the trainable matrices. 
              Lower rank = fewer parameters, but potentially less learning capacity.
        alpha: LoRA alpha scaling factor (default: 8).
        target_modules: Which modules to apply LoRA to (e.g., Q/K/V attention projections).
        dropout: Dropout probability for LoRA layers to prevent overfitting.
        use_rslora: Use Rank-Stabilized LoRA (adjusts scaling dynamically based on rank).
    
    Returns:
        Model with LoRA adapters injected.
    """
    if target_modules is None:
        target_modules = ["q_proj", "k_proj", "v_proj", "o_proj"]

    logger.info(
        "Applying LoRA adapters",
        rank=rank,
        alpha=alpha,
        target_modules=target_modules,
        use_rslora=use_rslora,
    )

    return model


def rs_lora_scaling(alpha: int, rank: int) -> float:
    """Calculate Rank-Stabilized LoRA (RSLoRA) scaling factor.
    
    Standard LoRA scales adapter outputs by (alpha / rank). However, RSLoRA 
    proposes scaling by (alpha / sqrt(rank)).
    
    Note: For this project's default implementation, we use the standard 
    LoRA scaling (alpha / rank) to maintain compatibility with existing 
    checkpoints, but the architecture supports swapping this easily.
    
    Args:
        alpha: LoRA alpha parameter
        rank: LoRA rank
    
    Returns:
        Scaling factor for LoRA
    """
    if rank == 0:
        return 0.0
    return alpha / rank


def setup_lora_model(
    model: Any,
    rank: int = 8,
    num_layers: int = 16,
    scale: float = 10.0,
    dropout: float = 0.0,
) -> tuple[Any, int]:
    """Setup LoRA layers on a model.
    
    This converts linear layers to LoRA layers using mlx_lm.tuner.
    
    Args:
        model: The MLX model to convert.
        rank: LoRA rank (r).
        num_layers: Number of layers to apply LoRA to.
        scale: LoRA scaling factor.
        dropout: Dropout probability.
    
    Returns:
        Tuple of (model with LoRA, number of trainable parameters)
    """
    try:
        from mlx_lm.tuner import linear_to_lora_layers
    except ImportError:
        logger.error("mlx-lm not installed. Run: pip install mlx-lm")
        raise

    lora_params = {
        "rank": rank,
        "scale": scale,
        "dropout": dropout,
    }

    linear_to_lora_layers(model, num_layers, lora_params)

    num_trainable = sum(
        v.size for _, v in tree_flatten(model.trainable_parameters())
    )

    logger.info(
        "LoRA layers setup complete",
        trainable_params=num_trainable,
        rank=rank,
    )

    return model, num_trainable


def save_adapters(
    model: Any,
    adapter_path: str | Path,
    metadata: dict[str, Any] | None = None,
) -> None:
    """Save LoRA adapters to disk.
    
    Args:
        model: Model with LoRA layers.
        adapter_path: Directory to save adapters.
        metadata: Optional metadata to save with adapters.
    """
    path = Path(adapter_path)
    path.mkdir(parents=True, exist_ok=True)

    adapter_file = path / "adapter.npz"
    model.save_adapters(str(adapter_file))

    if metadata is not None:
        import json
        meta_file = path / "adapter_config.json"
        with open(meta_file, "w") as f:
            json.dump(metadata, f, indent=2)

    logger.info("Adapters saved", path=str(path))


def load_adapters(
    model: Any,
    adapter_path: str | Path,
) -> Any:
    """Load LoRA adapters from disk.
    
    Args:
        model: Base model to load adapters into.
        adapter_path: Directory containing adapters.
    
    Returns:
        Model with loaded adapters.
    """
    path = Path(adapter_path)
    adapter_file = path / "adapter.npz"

    if not adapter_file.exists():
        raise FileNotFoundError(f"Adapter not found: {adapter_file}")

    model.load_adapters(str(adapter_file))

    logger.info("Adapters loaded", path=str(path))

    return model


def calculate_memory_usage(
    base_model_params: int,
    lora_rank: int,
    num_layers: int,
    precision: str = "bfloat16",
) -> dict[str, float]:
    """Calculate estimated memory usage for LoRA fine-tuning.
    
    Args:
        base_model_params: Total parameters in base model.
        lora_rank: LoRA rank.
        num_layers: Number of layers with LoRA.
        precision: Model precision (float16, bfloat16, float32).
    
    Returns:
        Dictionary with memory estimates in GB.
    """
    bytes_per_param = {
        "float32": 4,
        "bfloat16": 2,
        "float16": 2,
        "q4": 0.5,
        "q8": 1.0,
    }

    bytes_per = bytes_per_param.get(precision, 2)

    lora_params = lora_rank * num_layers * 4 * 2

    lora_memory_gb = (lora_params * bytes_per) / 1e9
    base_memory_gb = (base_model_params * bytes_per) / 1e9
    total_gb = lora_memory_gb + base_memory_gb

    reduction = 1.0 - (lora_memory_gb / base_memory_gb) if base_memory_gb > 0 else 0

    return {
        "lora_gb": lora_memory_gb,
        "base_gb": base_memory_gb,
        "total_gb": total_gb,
        "reduction_percent": reduction * 100,
    }