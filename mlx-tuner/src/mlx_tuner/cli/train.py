"""Training command CLI."""

import argparse
import sys
from pathlib import Path

from mlx_tuner.config import ModelConfig, LoRAConfig, TrainingConfig, DataConfig
from mlx_tuner.logging import get_logger

logger = get_logger(__name__)


def train(args: argparse.Namespace) -> int:
    """Run training.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success)
    """
    model_cfg = ModelConfig(name=args.model)
    lora_cfg = LoRAConfig()
    training_cfg = TrainingConfig(max_steps=args.steps)
    data_cfg = DataConfig(train_path=Path(args.data))

    logger.info(
        "Starting training",
        model=model_cfg.name,
        lora_rank=lora_cfg.rank,
        lora_alpha=lora_cfg.alpha,
        data=str(data_cfg.train_path),
        max_steps=training_cfg.max_steps,
    )

    try:
        from mlx_lm import load, generate
    except ImportError:
        print("Error: mlx-lm not installed. Run: pip install mlx-lm")
        return 1

    print(f"[1/4] Loading model: {model_cfg.name}")
    print(f"[2/4] Loading data: {data_cfg.train_path}")
    print(f"[3/4] Configuring LoRA (rank={lora_cfg.rank}, alpha={lora_cfg.alpha})")
    print(f"[4/4] Training for {training_cfg.max_steps} steps...")

    print("\nNote: This is a training scaffold.")
    print("Full training requires mlx-lm integration with actual dataset loading.")
    print("See https://github.com/ml-explore/mlx for official examples.")

    return 0


def main() -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Train an LLM with LoRA")
    parser.add_argument(
        "--model",
        type=str,
        default="SmolLM-135M",
        help="Model name from HuggingFace",
    )
    parser.add_argument(
        "--data",
        type=str,
        default="./data/train.jsonl",
        help="Training data JSONL file",
    )
    parser.add_argument(
        "--steps",
        type=int,
        default=100,
        help="Number of training steps",
    )

    args = parser.parse_args()
    return train(args)


if __name__ == "__main__":
    sys.exit(main())