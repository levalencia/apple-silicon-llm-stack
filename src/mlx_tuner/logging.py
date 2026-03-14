import logging
import sys
from pathlib import Path

import structlog
from structlog.processors import JSONRenderer, TimeStamper, add_log_level


def configure_logging(env: str = "development", log_dir: Path | None = None) -> None:
    """Configure structured logging for the application."""

    processors = [
        add_log_level,
        TimeStamper(fmt="iso"),
        structlog.contextvars.merge_contextvars,
    ]

    if env == "production":
        processors.append(JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer())

    # Determine log level
    log_level = logging.DEBUG if env == "development" else logging.INFO

    # Configure structlog
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Configure stdlib logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=log_level,
    )

    # Create log directory if specified
    if log_dir:
        log_dir.mkdir(parents=True, exist_ok=True)


def get_logger(name: str) -> structlog.BoundLogger:
    """Get a configured logger instance."""
    return structlog.get_logger(name)
