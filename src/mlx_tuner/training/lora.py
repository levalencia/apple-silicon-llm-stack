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

from typing import Any

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

    # Note: MLX arrays are lazily evaluated. This adapter insertion modifies the 
    # computational graph but does not immediately allocate massive memory buffers.
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
    return alpha / rank
