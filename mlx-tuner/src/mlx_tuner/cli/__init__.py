"""CLI module for mlx-tuner."""

from mlx_tuner.cli.__main__ import main
from mlx_tuner.cli.train import train
from mlx_tuner.cli.fuse import fuse
from mlx_tuner.cli.convert import convert

__all__ = ["main", "train", "fuse", "convert"]