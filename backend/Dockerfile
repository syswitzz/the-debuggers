FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install uv package manager
RUN pip install --no-cache-dir uv

# Copy dependency manifests for layer caching
COPY pyproject.toml uv.lock ./

# Install runtime dependencies
RUN uv sync --frozen --no-dev

# Copy application code after dependencies are installed
COPY . .

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
