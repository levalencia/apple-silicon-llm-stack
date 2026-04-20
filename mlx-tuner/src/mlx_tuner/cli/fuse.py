"""Fuse command CLI."""

import argparse
import sys
from pathlib import Path

from mlx_tuner.config import ModelConfig, LoRAConfig, OutputConfig
from mlx_tuner.logging import get_logger

logger = get_logger(__name__)


def fuse(args: argparse.Namespace) -> int:
    """Fuse LoRA adapters with base model.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success)
    """
    output_cfg = OutputConfig(output_dir=Path(args.adapter_dir))

    logger.info("Fusing LoRA adapters", output_dir=str(output_cfg.output_dir))

    print(f"[1/2] Loading adapters from: {output_cfg.output_dir}")
    print("[2/2] Fusing with base model...")

    print("\nNote: This is a fuse scaffold.")
    print("Full implementation would merge LoRA weights into base model.")
    print("See mlx-lm or peft documentation for merge methods.")

    return 0


def main() -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Fuse LoRA adapters with base model")
    parser.add_argument(
        "--adapter-dir",
        type=str,
        default="./adapters",
        help="Directory containing LoRA adapters",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="./models/fused",
        help="Output directory for fused model",
    )

    args = parser.parse_args()
    return fuse(args)


if __name__ == "__main__":
    sys.exit(main())