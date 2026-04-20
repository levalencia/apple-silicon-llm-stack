"""CLI entry point."""

import sys

from mlx_tuner.cli.train import main as train
from mlx_tuner.cli.fuse import main as fuse
from mlx_tuner.cli.convert import main as convert


def main() -> int:
    """Main CLI dispatcher."""
    if len(sys.argv) < 2:
        print("Usage: mlx-tuner <command>")
        print("Commands: train, fuse, convert")
        return 1

    command = sys.argv[1]
    subcommand = sys.argv[2:]
    sys.argv = ["mlx-tuner"] + subcommand

    if command == "train":
        return train()
    elif command == "fuse":
        return fuse()
    elif command == "convert":
        return convert()
    else:
        print(f"Unknown command: {command}")
        print("Commands: train, fuse, convert")
        return 1


if __name__ == "__main__":
    sys.exit(main())