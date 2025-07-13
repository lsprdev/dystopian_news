######################## 1. BUILD ########################
FROM python:3.13-slim AS builder

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Ferramentas mínimas para compilar wheels nativas
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Poetry 2.x (compatível com PEP 621)
RUN pip install --no-cache-dir "poetry~=2.1"

# ── Manifestos (já estão na raiz do contexto) ───────────
COPY pyproject.toml poetry.lock* ./

# Instala todas as dependências padrão, sem venv
RUN poetry config virtualenvs.create false && \
    poetry install --no-root --no-ansi --no-interaction

# Código-fonte do backend
COPY . .

######################## 2. RUNTIME ########################
FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# libpq5 para psycopg2-binary
RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq5 && \
    rm -rf /var/lib/apt/lists/*

# Copia libs + app
COPY --from=builder /usr/local /usr/local
COPY --from=builder /app /app

EXPOSE 8000
ENV PORT=8000
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
