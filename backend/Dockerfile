# Imagen de producción del backend NUMBYTE (FastAPI + Uvicorn).
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# psycopg[binary] ya trae las librerías de PostgreSQL compiladas, por lo que
# no se necesita un compilador. Solo instalamos curl para el healthcheck.
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Railway inyecta la variable PORT en tiempo de ejecución. Se usa la forma
# shell para poder expandir ${PORT}; si no existe, se usa 8000 (local/docker).
CMD uvicorn app.main:aplicacion --host 0.0.0.0 --port ${PORT:-8000}
