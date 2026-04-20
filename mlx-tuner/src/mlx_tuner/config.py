from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ModelConfig(BaseSettings):
    """Model configuration settings."""

    name: str = "SmolLM-135M"
    base_path: Path = Field(default=Path("./models"))
    context_length: int = 2048
    flash_attention: bool = True

    model_config = SettingsConfigDict(env_prefix="MODEL_")


class LoRAConfig(BaseSettings):
    """LoRA fine-tuning configuration."""

    rank: int = 8
    alpha: int = 8  # 1:1 ratio with rank - conservative and stable
    target_modules: list[str] = Field(
        default=["q_proj", "k_proj", "v_proj", "o_proj"]
    )
    dropout: float = 0.05
    use_rslora: bool = True  # Rank-Stabilized LoRA

    model_config = SettingsConfigDict(env_prefix="LORA_")


class TrainingConfig(BaseSettings):
    """Training configuration."""

    batch_size: int = 2
    learning_rate: float = 2e-4  # 5-10x higher than full fine-tune
    warmup_steps: int = 50  # ~5% of typical training
    gradient_checkpointing: bool = True
    gradient_clip: float = 1.0
    weight_decay: float = 0.01
    max_steps: int = 1000
    eval_steps: int = 100
    save_steps: int = 200
    early_stopping_patience: int = 3
    seed: int = 42

    model_config = SettingsConfigDict(env_prefix="TRAIN_")


class DataConfig(BaseSettings):
    """Data configuration."""

    train_path: Path = Field(default=Path("./data/train.jsonl"))
    valid_path: Path = Field(default=Path("./data/valid.jsonl"))
    test_path: Path = Field(default=Path("./data/test.jsonl"))
    chat_template: str = "chatml"  # chatml, alpaca, llama3

    model_config = SettingsConfigDict(env_prefix="DATA_")


class OutputConfig(BaseSettings):
    """Output configuration."""

    output_dir: Path = Field(default=Path("./adapters"))
    fused_dir: Path = Field(default=Path("./models/fused"))
    gguf_dir: Path = Field(default=Path("./models/gguf"))
    quantization: str = "Q4_K_M"  # Q4_K_M, Q5_K_M, Q6_K, Q8_0

    model_config = SettingsConfigDict(env_prefix="OUTPUT_")


class GGUFConfig(BaseSettings):
    """GGUF conversion configuration."""

    quantization: str = "Q4_K_M"
    use_imatrix: bool = True  # Importance matrix quantization
    imatrix_samples: int = 200

    model_config = SettingsConfigDict(env_prefix="GGUF_")


class LoggingConfig(BaseSettings):
    """Logging configuration."""

    level: str = "INFO"
    format: str = "json"  # json or console
    log_dir: Path = Field(default=Path("./logs"))

    model_config = SettingsConfigDict(env_prefix="LOG_")


class AppConfig(BaseSettings):
    """Main application configuration."""

    model: ModelConfig = Field(default_factory=ModelConfig)
    lora: LoRAConfig = Field(default_factory=LoRAConfig)
    training: TrainingConfig = Field(default_factory=TrainingConfig)
    data: DataConfig = Field(default_factory=DataConfig)
    output: OutputConfig = Field(default_factory=OutputConfig)
    gguf: GGUFConfig = Field(default_factory=GGUFConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)

    model_config = SettingsConfigDict(
        env_prefix="APP_",
        env_nested_delimiter="__",
        extra="ignore"
    )
