.PHONY: help install fmt lint check test test-cov train fuse convert docker-build clean

help:
	@echo "MLX Tuner - Available targets:"
	@echo ""
	@echo "  install         Install dependencies"
	@echo "  fmt             Format code with ruff"
	@echo "  lint            Lint code with ruff"
	@echo "  check           Run all checks (fmt + lint + test)"
	@echo "  test            Run tests with pytest"
	@echo "  test-cov        Run tests with coverage"
	@echo "  train           Run training"
	@echo "  fuse            Fuse LoRA adapters with base model"
	@echo "  convert         Convert to GGUF format"
	@echo "  docker-build    Build Docker image"
	@echo "  clean           Clean build artifacts"

install:
	@echo "Installing dependencies..."
ifneq ($(wildcard .venv),)
	@echo "Using existing .venv"
	.venv/bin/pip install -e .
else
	@echo "Creating venv..."
	python3 -m venv .venv && .venv/bin/pip install -e .
endif
	@echo "Note: In zsh, use: pip install -e \".[dev]\""

fmt:
	@echo "Formatting code..."
	ruff format src/ tests/

lint:
	@echo "Linting code..."
	ruff check src/ tests/

check: fmt lint test

test:
	@echo "Running tests..."
	pytest tests/ -v

test-cov:
	@echo "Running tests with coverage..."
	pytest tests/ --cov=src/mlx_tuner --cov-report=html --cov-report=term

VENV_PYTHON = $(shell if [ -d .venv ]; then echo ".venv/bin/python"; else echo "python"; fi)

train:
	@echo "Running training..."
	$(VENV_PYTHON) -m mlx_tuner.cli train --model SmolLM-135M --data ./data/train.jsonl

fuse:
	@echo "Fusing LoRA adapters..."
	$(VENV_PYTHON) -m mlx_tuner.cli fuse --adapter-dir ./adapters

convert:
	@echo "Converting to GGUF..."
	$(VENV_PYTHON) -m mlx_tuner.cli convert --model ./fused --quantization Q4_K_M

docker-build:
	@echo "Building Docker image..."
	docker build -t mlx-tuner:latest .

clean:
	@echo "Cleaning build artifacts..."
	rm -rf build/ dist/ *.egg-info
	rm -rf .pytest_cache .coverage htmlcov
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
