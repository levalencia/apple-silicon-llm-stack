"""Convert command CLI."""

import argparse
import sys
from pathlib import Path

from mlx_tuner.config import GGUFConfig
from mlx_tuner.logging import get_logger

logger = get_logger(__name__)


def convert(args: argparse.Namespace) -> int:
    """Convert model to GGUF format.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success)
    """
    gguf_cfg = GGUFConfig(quantization=args.quantization)

    logger.info(
        "Converting to GGUF",
        quantization=gguf_cfg.quantization,
        input_dir=args.model,
    )

    print(f"[1/3] Loading model from: {args.model}")
    print(f"[2/3] Applying quantization: {gguf_cfg.quantization}")
    print("[3/3] Saving to GGUF format...")

    print("\nNote: This is a convert scaffold.")
    print("Full GGUF conversion requires llama.cpp binding or mlx export.")
    print("See https://github.com/ggerganov/llama.cpp for ggufify.")

    return 0


def main() -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Convert model to GGUF format")
    parser.add_argument(
        "--model",
        type=str,
        default="./models/fused",
        help="Input model directory",
    )
    parser.add_argument(
        "--quantization",
        type=str,
        default="Q4_K_M",
        choices=["Q4_K_M", "Q5_K_M", "Q6_K", "Q8_0"],
        help="Quantization type",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="./models/output.gguf",
        help="Output GGUF file path",
    )

    args = parser.parse_args()
    return convert(args)


if __name__ == "__main__":
    sys.exit(main())