######################## 1. BUILD ########################
FROM python:3.13-slim AS builder

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Ferramentas mínimas para compilar wheels nativas
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Poetry 2.x (compatível com PEP 621 do pyproject)
RUN pip install --no-cache-dir "poetry~=2.1"

# ──⬇⬇──────── Cópia dos manifests (via caminho relativo ao repositório) ──⬇⬇──
COPY backend/pyproject.toml backend/poetry.lock* ./
# ──⬆⬆───────────────────────────────────────────────────────────────────────⬆⬆──

# Instala todas as dependências padrão (sem criar venv)
RUN poetry config virtualenvs.create false && \
    poetry install --no-root --no-ansi --no-interaction

# ──⬇⬇──────── Cópia do código-fonte do backend ──⬇⬇──
COPY backend/. .
# ──⬆⬆────────────────────────────────────────────⬆⬆──

######################## 2. RUNTIME ########################
FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# libpq5 é necessária em tempo de execução para psycopg2-binary
RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq5 && \
    rm -rf /var/lib/apt/lists/*

# Copia dependências Python e código compilado
COPY --from=builder /usr/local /usr/local
COPY --from=builder /app /app

EXPOSE 8000
ENV PORT=8000
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
