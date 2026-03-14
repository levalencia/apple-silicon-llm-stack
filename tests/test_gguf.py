"""Tests for GGUF conversion."""

from mlx_tuner.convert.gguf_converter import GGUFConverter, build_gguf_filename


def test_build_gguf_filename():
    """Test GGUF filename building."""
    filename = build_gguf_filename("SmolLM-135M", "Q4_K_M")
    assert filename == "SmolLM-135M-Q4_K_M.gguf"

    filename = build_gguf_filename("TinyLlama", "Q8_0")
    assert filename == "TinyLlama-Q8_0.gguf"


def test_gguf_converter_default_quantization():
    """Test GGUF converter default quantization."""
    converter = GGUFConverter()
    assert converter.quantization == "Q4_K_M"


def test_gguf_converter_custom_quantization():
    """Test GGUF converter custom quantization."""
    converter = GGUFConverter(quantization="Q8_0")
    assert converter.quantization == "Q8_0"


def test_gguf_converter_imatrix():
    """Test GGUF converter importance matrix setting."""
    converter = GGUFConverter(use_imatrix=True)
    assert converter.use_imatrix is True

    converter = GGUFConverter(use_imatrix=False)
    assert converter.use_imatrix is False
