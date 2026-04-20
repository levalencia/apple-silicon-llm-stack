"""Training loop implementation using mlx-lm."""

import json
from pathlib import Path
from typing import Any

from mlx_lm.tuner import TrainingArgs, train

from mlx_tuner.config import TrainingConfig
from mlx_tuner.logging import get_logger

logger = get_logger(__name__)


class Trainer:
    """MLX training loop implementation using mlx-lm."""

    def __init__(
        self,
        config: TrainingConfig,
        model: Any | None = None,
        tokenizer: Any | None = None,
    ):
        """Initialize trainer.
        
        Args:
            config: Training configuration.
            model: MLX model (loaded via mlx_lm.load).
            tokenizer: Tokenizer for the model.
        """
        self.config = config
        self.model = model
        self.tokenizer = tokenizer

    def train(
        self,
        model: Any,
        tokenizer: Any,
        train_data: Path,
        adapter_path: Path | None = None,
    ) -> dict[str, Any]:
        """Run training loop.
        
        Args:
            model: MLX model.
            tokenizer: Model tokenizer.
            train_data: Path to training data JSONL file.
            adapter_path: Path to save adapters.
        
        Returns:
            Training results dictionary.
        """
        if adapter_path is None:
            adapter_path = Path("./adapters")
        adapter_path.mkdir(parents=True, exist_ok=True)

        logger.info(
            "Starting LoRA training",
            max_steps=self.config.max_steps,
            batch_size=self.config.batch_size,
            learning_rate=self.config.learning_rate,
            train_data=str(train_data),
        )

        training_args = TrainingArgs(
            adapter_file=str(adapter_path / "adapter.npz"),
            iters=self.config.max_steps,
            batch_size=self.config.batch_size,
            steps_per_eval=self.config.eval_steps,
            seed=self.config.seed,
        )

        try:
            train(
                model=model,
                tokenizer=tokenizer,
                args=training_args,
                train_data=[(str(train_data),)],
            )
        except Exception as e:
            logger.error("Training failed", error=str(e))
            raise

        logger.info("Training completed", adapter_path=str(adapter_path))

        return {
            "adapter_path": str(adapter_path),
            "iters": self.config.max_steps,
            "batch_size": self.config.batch_size,
            "learning_rate": self.config.learning_rate,
        }

    def evaluate(
        self,
        model: Any,
        tokenizer: Any,
        eval_data: Path,
    ) -> dict[str, float]:
        """Evaluate model on dataset.
        
        Args:
            model: MLX model.
            tokenizer: Model tokenizer.
            eval_data: Path to evaluation data.
        
        Returns:
            Evaluation metrics.
        """
        from mlx_lm.tuner import evaluate

        logger.info("Running evaluation", eval_data=str(eval_data))

        training_args = TrainingArgs(
            batch_size=self.config.batch_size,
            iters=1,
        )

        try:
            loss = evaluate(
                model=model,
                tokenizer=tokenizer,
                args=training_args,
                eval_data=[(str(eval_data),)],
            )
        except Exception as e:
            logger.warning("Evaluation failed, returning zeros", error=str(e))
            loss = 0.0

        perplexity = __import__("math").exp(loss) if loss > 0 else float("inf")

        metrics = {
            "loss": loss,
            "perplexity": perplexity,
        }

        logger.info("Evaluation complete", metrics=metrics)

        return metrics


def create_training_config(
    iters: int = 100,
    batch_size: int = 1,
    learning_rate: float = 1e-4,
    warmup_steps: int = 10,
) -> TrainingConfig:
    """Create training configuration.
    
    Args:
        iters: Number of training iterations.
        batch_size: Training batch size.
        learning_rate: Learning rate.
        warmup_steps: Warmup steps.
    
    Returns:
        TrainingConfig instance.
    """
    return TrainingConfig(
        max_steps=iters,
        batch_size=batch_size,
        learning_rate=learning_rate,
        warmup_steps=warmup_steps,
    )


def list_lora_layers(model: Any) -> dict[str, int]:
    """List all linear layers available for LoRA conversion.
    
    Args:
        model: MLX model.
    
    Returns:
        Dictionary mapping layer names to parameter counts.
    """
    layers = {}

    try:
        from mlx.utils import tree_map

        def count_params(name: str, module: Any) -> int:
            if hasattr(module, "weight"):
                return module.weight.size
            return 0

        for name, params in tree_map(
            lambda name, x: (name, x)
        ).items():
            if "linear" in str(type(params)).lower() or hasattr(params, "weight"):
                layers[name] = params.size if hasattr(params, "size") else 0

    except Exception as e:
        logger.warning("Could not list layers", error=str(e))

    return layers