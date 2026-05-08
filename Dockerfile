FROM python:3.13-slim

WORKDIR /app

# Copiar arquivos de dependências
COPY pyproject.toml uv.lock ./

# Instalar UV e dependências
RUN pip install uv && \
    uv sync --frozen

# Copiar código
COPY src/ ./src/

# Executar ingestão
CMD ["uv", "run", "python", "src/ingest_data.py"]