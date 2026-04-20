"""Tests for LoRA module."""

from mlx_tuner.training.lora import apply_lora, rs_lora_scaling


def test_rs_lora_scaling_standard():
    """Test rslora scaling equals 1.0 when alpha = rank."""
    scaling = rs_lora_scaling(alpha=8, rank=8)
    assert scaling == 1.0


def test_rs_lora_scaling_different():
    """Test rslora scaling with different alpha/rank."""
    scaling = rs_lora_scaling(alpha=16, rank=8)
    assert scaling == 2.0


def test_rs_lora_scaling_matches_standard():
    """Test rslora scaling produces equivalent results to standard at alpha=r."""
    # When alpha = rank, rslora scaling should be 1.0
    # This produces the same result as standard LoRA
    for rank in [4, 8, 16, 32]:
        scaling = rs_lora_scaling(alpha=rank, rank=rank)
        assert scaling == 1.0


def test_apply_lora_default_params():
    """Test LoRA application with default parameters."""
    # This tests that apply_lora runs without error
    # We pass None as model since we don't have a real MLX model
    result = apply_lora(None, rank=8, alpha=8)
    assert result is None


def test_apply_lora_custom_target_modules():
    """Test LoRA application with custom target modules."""
    result = apply_lora(
        None,
        rank=8,
        alpha=8,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]
    )
    assert result is None
