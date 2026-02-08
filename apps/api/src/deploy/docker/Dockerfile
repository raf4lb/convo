# Imagem Python oficial, multiarch (inclusive linux/arm64)
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependências básicas para compilação de algumas libs Python
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl build-essential \
 && rm -rf /var/lib/apt/lists/*

# Instala o UV (script oficial multiarch)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Adiciona ~/.local/bin ao PATH
ENV PATH="/root/.local/bin:${PATH}"

# Copia arquivos de dependência
COPY pyproject.toml uv.lock ./

# Instala dependências
RUN uv sync --no-dev --frozen --no-install-project

# Copia o restante da aplicação
COPY . ./
RUN rm -r ./.venv

EXPOSE 5000

# Inicia o servidor Flask (via gunicorn)
CMD ["uv", "run", "gunicorn", "--bind", "0.0.0.0:5000", "main:app", "--workers", "2", "--threads", "2"]
