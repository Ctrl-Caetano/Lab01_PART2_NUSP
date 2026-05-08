# Lab01-B: Pipeline de Dados Containerizado

**Disciplina:** Engenharia de Dados e Modelagem - PECE/USP  
**Aluno:** Caetano  
**Dataset:** Spotify Music (1.1M músicas)

## O que é esse projeto

Pipeline de ingestão e validação de dados usando Docker, Python e PostgreSQL. Trabalha com um dataset do Spotify com mais de 1 milhão de músicas, fazendo a ingestão, validação de qualidade e visualizações.

## Arquitetura

O fluxo é simples: dados do CSV vão pro PostgreSQL via Python, depois validamos a qualidade e geramos um dashboard com gráficos.

## Estrutura
Lab01_PART2_NUSP/
├── src/
│   ├── ingest_data.py       # Faz a ingestão dos dados
│   ├── data_quality.py      # Valida a qualidade
│   └── dashboard.py         # Gera os gráficos
├── docs/
│   ├── data_quality_report.html
│   └── dashboard.html
├── Dockerfile
└── pyproject.toml

## Como rodar

### Instalar

```bash
git clone https://github.com/Ctrl-Caetano/Lab01_PART2_NUSP.git
cd Lab01_PART2_NUSP
pip install uv
uv sync
```

### PostgreSQL

Cria o database:

```sql
CREATE DATABASE lab01b;
\c lab01b
CREATE SCHEMA raw;
```

### Executar

```bash
# Ingestão
uv run python src/ingest_data.py

# Validação
uv run python src/data_quality.py

# Dashboard
uv run python src/dashboard.py
```

### Docker

Quando o Docker estiver funcionando:

```bash
docker build -t lab01b-pipeline .
docker run --rm -e DB_HOST=host.docker.internal lab01b-pipeline
```

## Validações

Fiz 6 validações de qualidade nos dados:

1. Track ID não pode ser nulo
2. Popularidade tem que estar entre 0 e 100
3. Ano tem que ser maior que 1900
4. Danceability entre 0 e 1
5. Energy entre 0 e 1
6. Artist name não pode ser nulo

Resultado: 5 de 6 passaram. Só tem 15 artist names nulos de 1.1M linhas, o que é aceitável.

O relatório completo tá em `docs/data_quality_report.html`.

## Dashboard

Dashboard tem 6 visualizações:

- Top 15 artistas por número de músicas
- Top 15 artistas por popularidade
- Top 15 gêneros por popularidade
- Evolução de lançamentos desde 2000
- Distribuição de energia das músicas
- Relação entre danceability e popularidade

Abre o arquivo `docs/dashboard.html` pra ver.

## Dataset

Dataset do Spotify com 1.159.764 músicas de 1921 até 2024. Tem informações de artista, popularidade, gênero, e várias métricas de áudio (danceability, energy, acousticness, etc).

## Tecnologias

Python 3.13, UV (gerenciador de pacotes), PostgreSQL 16, Docker, Pandas, SQLAlchemy, Plotly.

## Autor

Caetano - PECE/USP  
GitHub: @Ctrl-Caetano