FROM python:3.13-slim

# Recommended environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_SYSTEM_PYTHON=1

WORKDIR /app

# Minimum system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv (official binary)
RUN curl -Ls https://astral.sh/uv/install.sh | sh \
    && mv /root/.local/bin/uv /usr/local/bin/uv

# Copy only dependency files first (efficient caching)
COPY pyproject.toml uv.lock ./

# Install dependencies (fast and repeatable)
RUN uv sync --frozen

# Copy the rest of the application
COPY . .

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
