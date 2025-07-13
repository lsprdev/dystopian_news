######################## 1. BUILD ########################
FROM python:3.13-slim AS builder

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Compiladores e headers p/ wheels nativas
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Poetry 2.x (compatível com PEP 621)
RUN pip install --no-cache-dir "poetry~=2.1"

# Copia manifestos antes para cache
COPY pyproject.toml poetry.lock* ./

# Instala TODAS as dependências padrão, sem venv
RUN poetry config virtualenvs.create false && \
    poetry install --no-root --no-ansi --no-interaction

# Copia o resto do código-fonte
COPY . .

######################## 2. RUNTIME ########################
FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# libpq5 é necessária em tempo de execução para psycopg2-binary
RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq5 && \
    rm -rf /var/lib/apt/lists/*

# Copia dependências Python + código
COPY --from=builder /usr/local /usr/local
COPY --from=builder /app /app

EXPOSE 8000
ENV PORT=8000
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
