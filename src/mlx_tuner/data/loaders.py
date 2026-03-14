"""Data loading utilities."""

import json
from pathlib import Path
from typing import Any

from mlx_tuner.logging import get_logger

logger = get_logger(__name__)


class JSONLDatasetLoader:
    """Load datasets from JSONL format files."""

    def __init__(self, chat_template: str = "chatml"):
        self.chat_template = chat_template

    def load(self, path: Path) -> list[dict[str, Any]]:
        """Load JSONL dataset from path."""
        if not path.exists():
            logger.error("Dataset file not found", path=str(path))
            raise FileNotFoundError(f"Dataset not found: {path}")

        data = []
        with open(path, encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    data.append(json.loads(line))
                except json.JSONDecodeError as e:
                    logger.warning("Skipping invalid JSON line", line_num=line_num, error=str(e))

        logger.info("Loaded dataset", path=str(path), count=len(data))
        return data

    def validate(self, data: list[dict[str, Any]]) -> bool:
        """Validate dataset has required fields."""
        if not data:
            return False

        for i, item in enumerate(data):
            if not isinstance(item, dict):
                logger.error("Invalid item type", index=i, type=type(item))
                return False
            if "messages" not in item:
                logger.error("Missing required field", index=i, field="messages")
                return False
            if not isinstance(item["messages"], list):
                logger.error("Messages must be a list", index=i)
                return False

        return True


class HuggingFaceDatasetLoader:
    """Load datasets from Hugging Face Hub."""

    def __init__(self, name: str, split: str = "train"):
        self.name = name
        self.split = split

    def load(self, path: Path | None = None) -> list[dict[str, Any]]:
        """Load dataset from Hugging Face."""
        # This would use the datasets library
        # For now, return empty list as placeholder
        logger.info("Loading from HuggingFace", name=self.name, split=self.split)
        return []

    def validate(self, data: list[dict[str, Any]]) -> bool:
        """Validate dataset format."""
        return len(data) > 0
