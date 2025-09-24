# Multi-stage Docker build for Simple Groq App with UV optimizations
# Following UV's official Docker best practices

FROM python:3.10-slim

# Set environment variables for optimal UV behavior
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_CACHE_DIR=/root/.cache/uv/python

# Create app directory
WORKDIR /app

# Install system dependencies required for compilation
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Download the latest installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

# Verify UV installation
RUN uv --version

# Copy UV configuration files first for better caching
COPY pyproject.toml uv.lock* ./

# Install Python and dependencies with cache mount and optimizations
RUN --mount=type=cache,target=/root/.cache/uv \
    uv python install && \
    uv sync --compile-bytecode --no-dev && \
    uv run python -c "from PIL import Image; print('Pillow working correctly')"

# Copy application code
COPY . .

# Expose ports
EXPOSE 8000 8501

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Default command using UV run
CMD ["uv", "run", "python", "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]