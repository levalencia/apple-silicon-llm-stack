# Stage 1: Builder
FROM python:3.11-slim-bookworm AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install uv

WORKDIR /app
COPY mlx-tuner/pyproject.toml .
RUN uv pip install --system --no-cache -e .

# Stage 2: Production
FROM python:3.11-slim-bookworm AS production

RUN apt-get update && apt-get install -y --no-install-recommends \
    libomp-dev \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 1000 appuser
WORKDIR /app

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY --chown=appuser:appuser mlx-tuner/data ./data
COPY --chown=appuser:appuser mlx-tuner/configs ./configs

USER appuser

ENV PYTHONUNBUFFERED=1
ENV APP_ENV=production

CMD ["python", "-m", "mlx_tuner", "--help"]
