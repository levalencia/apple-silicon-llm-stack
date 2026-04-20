# MLX Tuner Agent Instructions

You are an expert Python developer working on the `mlx-tuner` repository. This project is an advanced fine-tuning pipeline for Large Language Models using Apple's MLX framework.

## 1. Build, Lint, and Test Commands

When you modify code, always self-verify using these commands from the `mlx-tuner` directory:

- **Setup**: `pip install -e .[dev]` (Always work within a virtual environment)
- **Lint**: `make lint` (Runs Ruff: `ruff check src/ tests/`)
- **Format**: `make fmt` (Runs Ruff: `ruff format src/ tests/`)
- **Type Check**: `pyright` (Strict typing is enforced)
- **Test All**: `make test` or `pytest tests/ -v`
- **Run Single Test**: `pytest tests/test_file.py::test_function_name -v`
- **Full Verification**: `make check` (Runs format, lint, and test)

## 2. Architectural Guidelines

- **Protocol-Based Dependency Injection**: (ADR-001) Tight coupling is strictly forbidden. Define `Protocol` interfaces in `src/mlx_tuner/protocols.py` that describe what a class can do. Inject these protocols into business logic to facilitate easy mocking and testing.
- **Configuration Layer**: Use `pydantic-settings` to manage configurations securely (parsing `.env` files).
- **Core Pipeline**: Operations follow a clear sequence: Data Loading -> Model Loading -> Training (LoRA via `mlx_lm`) -> Converting (to GGUF). Ensure code maps to these boundaries.

## 3. Code Style & Best Practices

### Formatting & Typing
- **Target Python Version**: 3.11+.
- **Ruff Compliance**: Line length is 100 characters. `ruff` is configured to ignore `E501` but handle import sorting automatically (`I` rule).
- **Strict Typing**: Pyright strict mode is enabled. *Every* function signature (arguments and return types) and class attribute must be explicitly typed.
- **Naming Conventions**: Use `snake_case` for variables, properties, modules, and functions. Use `PascalCase` for classes. Use `ALL_CAPS` for constants.

### Logging and Error Handling
- **Logging**: Use `structlog` for structured logging. Avoid standard `print` statements.
- **Error Handling**: Raise custom exceptions for specific module failures (e.g., `GGUFConversionError`) rather than generic `Exception` blocks. 

### MLX/Metal Constraints
- Memory is shared on Apple Silicon, but MLX operations should be lazily evaluated (`mlx.core.eval()`). Pay attention to when operations are actually compiled and executed.

## 4. Agent Operations
- Read `docs/ARCHITECTURE.md` and `docs/DESIGN.md` if you are modifying core training or data loading modules.
- Use `glob` and `grep` extensively to find relevant `Protocol` definitions before writing implementations.
- Proactively run single tests to verify bug fixes immediately.
