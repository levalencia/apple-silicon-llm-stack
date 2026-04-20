"""Training command CLI using mlx-lm with YAML config.

This module provides LoRA fine-tuning using Apple's MLX-LM framework.
For full training to work, you need:
1. A model from HuggingFace (e.g., HuggingFaceTB/SmolLM-135M)
2. Training data in a directory with train.jsonl, valid.jsonl (optional), test.jsonl (optional)
3. mlx-lm properly installed

Data Format (train.jsonl, valid.jsonl):
Each line should be a JSON object with either:
- {"messages": [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]}
- {"text": "The full text for completion training..."}

Example data preparation:
    echo '{"messages": [{"role": "user", "content": "Hello"}, {"role": "assistant", "content": "Hi there!"}]}' > data/train.jsonl
"""

import argparse
import subprocess
import sys
from pathlib import Path

from mlx_tuner.config import LoRAConfig, TrainingConfig
from mlx_tuner.logging import get_logger

logger = get_logger(__name__)


def prepare_data(source_path: Path, dest_dir: Path) -> Path:
    """Prepare training data in mlx-lm format.
    
    Args:
        source_path: Source data file or directory
        dest_dir: Destination directory
    
    Returns:
        Path to data directory
    """
    import shutil
    
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    if source_path.is_file():
        target = dest_dir / "train.jsonl"
        shutil.copy(source_path, target)
        logger.info("Copied training data", src=str(source_path), dst=str(target))
        return dest_dir
    elif source_path.is_dir():
        shutil.copytree(source_path, dest_dir, dirs_exist_ok=True)
        logger.info("Copied data directory", src=str(source_path), dst=str(dest_dir))
        return dest_dir
    
    raise ValueError(f"Invalid data path: {source_path}")


def train(args: argparse.Namespace) -> int:
    """Run training via mlx-lm CLI.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success)
    """
    model_name = args.model
    data_path = Path(args.data)
    adapter_path = Path(args.adapter_dir)

    lora_cfg = LoRAConfig(rank=args.rank, alpha=args.alpha)
    training_cfg = TrainingConfig(
        max_steps=args.steps,
        batch_size=args.batch_size,
    )

    adapter_path.mkdir(parents=True, exist_ok=True)

    logger.info(
        "Starting training",
        model=model_name,
        lora_rank=lora_cfg.rank,
        lora_alpha=lora_cfg.alpha,
        data=str(data_path),
        max_steps=training_cfg.max_steps,
    )

    print(f"[1/5] Model: {model_name}")
    print(f"[2/5] Data: {data_path}")
    print(f"[3/5] LoRA: rank={lora_cfg.rank}, alpha={lora_cfg.alpha}")
    
    prepared_data = prepare_data(data_path, adapter_path / "data")
    print(f"[4/5] Prepared data: {prepared_data}")

    import yaml
    
    lora_config = {
        "model": model_name,
        "train": True,
        "fine_tune_type": "lora",
        "data": str(prepared_data),
        "num_layers": args.layers,
        "batch_size": training_cfg.batch_size,
        "iters": training_cfg.max_steps,
        "lora_parameters": {
            "rank": lora_cfg.rank,
            "scale": lora_cfg.alpha,
            "dropout": lora_cfg.dropout,
        },
        "adapter_path": str(adapter_path),
        "optimizer": "adamw",
        "seed": 42,
    }

    config_path = adapter_path / "config.yaml"
    config_path.write_text(yaml.dump(lora_config))

    cmd = [
        sys.executable,
        "-m", "mlx_lm", "lora",
        "-c", str(config_path),
    ]

    print(f"[5/5] Starting training...\n")
    print(f"Config file: {config_path}")
    print(f"Run: {' '.join(cmd)}\n")

    try:
        result = subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"\nTraining failed with exit code: {e.returncode}")
        print(f"\nTroubleshooting:")
        print(f"  1. Check data format: each line in train.jsonl should be:")
        print(f"     {{'messages': [{{'role': 'user', 'content': '...'}}, {{'role': 'assistant', 'content': '...'}}]}}")
        print(f"  2. Or use text format: {{'text': 'Completion text...'}}")
        print(f"  3. Ensure you have at least 10 training examples")
        return 1

    print(f"\n✓ Training complete!")
    print(f"  - Adapter path: {adapter_path}")
    print(f"  - Config: {config_path}")

    return 0


def main() -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Train an LLM with LoRA on Apple Silicon using MLX-LM",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --model HuggingFaceTB/SmolLM-135M --data ./data --steps 100 --rank 8
  %(prog)s --model meta-llama/Llama-3.2-1B-Instruct --rank 16 --steps 500

Data Format (train.jsonl):
  {"messages": [{"role": "user", "content": "Hello"}, {"role": "assistant", "content": "Hi!"}]}
  {"text": "Completion training text here..."}

Memory Notes:
  - 24GB M4 Pro: batch_size=1, rank=8-16 recommended
  - 48GB+: batch_size=2-4, rank=16-32
  - Smaller models (135M-1B) work best for development
        """,
    )
    parser.add_argument(
        "--model",
        type=str,
        default="HuggingFaceTB/SmolLM-135M",
        help="Model name from HuggingFace",
    )
    parser.add_argument(
        "--data",
        type=str,
        default="./data",
        help="Training data directory with train.jsonl (or file path)",
    )
    parser.add_argument(
        "--steps",
        type=int,
        default=100,
        help="Number of training steps",
    )
    parser.add_argument(
        "--rank",
        type=int,
        default=8,
        help="LoRA rank (default: 8)",
    )
    parser.add_argument(
        "--alpha",
        type=int,
        default=8,
        help="LoRA alpha/scale (default: 8)",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=1,
        help="Batch size (default: 1)",
    )
    parser.add_argument(
        "--layers",
        type=int,
        default=16,
        help="Number of layers for LoRA (default: 16)",
    )
    parser.add_argument(
        "--adapter-dir",
        type=str,
        default="./adapters",
        help="Output directory for adapters",
    )

    a = parser.parse_args()
    return train(a)


if __name__ == "__main__":
    sys.exit(main())