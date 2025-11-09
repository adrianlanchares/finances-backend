FROM python:3.11-slim

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

# Update and install dependencies
RUN apt-get update && apt-get install -y curl
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
COPY pyproject.toml  ./
RUN uv sync

COPY . .

# Update database and run
CMD uv run python -m finances_backend.manage makemigrations --noinput && \
    uv run python -m finances_backend.manage migrate --noinput && \
    uv run python -m finances_backend.manage runserver 0.0.0.0:8000
