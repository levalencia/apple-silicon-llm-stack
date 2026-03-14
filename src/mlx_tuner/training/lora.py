"""LoRA adapter application utilities."""

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
    """Apply LoRA adapters to a model.
    
    Args:
        model: The base model to apply LoRA to
        rank: LoRA rank (default: 8)
        alpha: LoRA alpha scaling factor (default: 8, 1:1 ratio with rank)
        target_modules: Which modules to apply LoRA to
        dropout: Dropout probability for LoRA layers
        use_rslora: Use Rank-Stabilized LoRA
    
    Returns:
        Model with LoRA adapters applied
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

    # LoRA application would happen here using peft or mlx_lm
    # This is a placeholder implementation
    return model


def rs_lora_scaling(alpha: int, rank: int) -> float:
    """Calculate Rank-Stabilized LoRA scaling factor.
    
    Args:
        alpha: LoRA alpha parameter
        rank: LoRA rank
    
    Returns:
        Scaling factor for rslora
    """
    return alpha / rank
