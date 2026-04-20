"""Tests for config module."""

from mlx_tuner.config import (
    AppConfig,
    LoRAConfig,
    ModelConfig,
    TrainingConfig,
)


def test_default_model_config():
    """Test default model configuration."""
    config = ModelConfig()
    assert config.name == "SmolLM-135M"
    assert config.context_length == 2048
    assert config.flash_attention is True


def test_default_lora_config():
    """Test default LoRA configuration."""
    config = LoRAConfig()
    assert config.rank == 8
    assert config.alpha == 8  # 1:1 ratio
    assert config.use_rslora is True
    assert "q_proj" in config.target_modules


def test_lora_alpha_ratio():
    """Test LoRA alpha to rank ratio."""
    config = LoRAConfig(rank=16, alpha=16)
    assert config.alpha / config.rank == 1.0


def test_default_training_config():
    """Test default training configuration."""
    config = TrainingConfig()
    assert config.batch_size == 2
    assert config.learning_rate == 2e-4
    assert config.gradient_checkpointing is True


def test_app_config():
    """Test full app configuration."""
    config = AppConfig()
    assert config.model.name == "SmolLM-135M"
    assert config.lora.rank == 8
    assert config.training.batch_size == 2


def test_env_override():
    """Test environment variable override."""
    import os
    os.environ["MODEL_NAME"] = "TinyLlama-1.1B"

    config = ModelConfig()
    assert config.name == "TinyLlama-1.1B"

    del os.environ["MODEL_NAME"]
