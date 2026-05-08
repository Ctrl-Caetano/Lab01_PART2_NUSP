import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import json

print("Carregando dados...")
engine = create_engine('postgresql://postgres:123@localhost:5434/lab01b')
df = pd.read_sql_table('spotify_tracks', engine, schema='raw')
print(f"✅ {len(df)} linhas carregadas\n")

# Validações
validations = []

# 1. Track ID não nulo
null_tracks = df['track_id'].isnull().sum()
validations.append({
    "rule": "Track ID não pode ser nulo",
    "passed": null_tracks == 0,
    "details": f"{null_tracks} valores nulos encontrados"
})

# 2. Popularidade entre 0-100
invalid_pop = df[(df['popularity'] < 0) | (df['popularity'] > 100)].shape[0]
validations.append({
    "rule": "Popularidade deve estar entre 0 e 100",
    "passed": invalid_pop == 0,
    "details": f"{invalid_pop} valores fora do range"
})

# 3. Year válido (>1900)
invalid_year = df[df['year'] < 1900].shape[0]
validations.append({
    "rule": "Ano deve ser maior que 1900",
    "passed": invalid_year == 0,
    "details": f"{invalid_year} valores inválidos"
})

# 4. Danceability entre 0-1
invalid_dance = df[(df['danceability'] < 0) | (df['danceability'] > 1)].shape[0]
validations.append({
    "rule": "Danceability deve estar entre 0 e 1",
    "passed": invalid_dance == 0,
    "details": f"{invalid_dance} valores fora do range"
})

# 5. Energy entre 0-1
invalid_energy = df[(df['energy'] < 0) | (df['energy'] > 1)].shape[0]
validations.append({
    "rule": "Energy deve estar entre 0 e 1",
    "passed": invalid_energy == 0,
    "details": f"{invalid_energy} valores fora do range"
})

# 6. Artist name não nulo
null_artists = df['artist_name'].isnull().sum()
validations.append({
    "rule": "Artist name não pode ser nulo",
    "passed": null_artists == 0,
    "details": f"{null_artists} valores nulos"
})

# Resultados
passed = sum(1 for v in validations if v['passed'])
total = len(validations)

print(f"Resultado: {passed}/{total} validações passaram\n")
for i, v in enumerate(validations, 1):
    status = "✅ PASS" if v['passed'] else "❌ FAIL"
    print(f"{i}. {status} - {v['rule']}")
    print(f"   {v['details']}\n")

# Gerar HTML
html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Relatório de Qualidade de Dados</title>
    <style>
        body {{ font-family: Arial; margin: 40px; background: #f5f5f5; }}
        .container {{ background: white; padding: 30px; border-radius: 8px; }}
        h1 {{ color: #333; }}
        .summary {{ background: #e8f4f8; padding: 20px; border-radius: 5px; margin: 20px 0; }}
        .validation {{ margin: 15px 0; padding: 15px; border-left: 4px solid #ddd; }}
        .pass {{ border-left-color: #4caf50; background: #f1f8f4; }}
        .fail {{ border-left-color: #f44336; background: #fef1f0; }}
        .status {{ font-weight: bold; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Relatório de Qualidade de Dados - Spotify</h1>
        <div class="summary">
            <h2>Resumo</h2>
            <p><strong>Data:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p><strong>Total de registros:</strong> {len(df):,}</p>
            <p><strong>Validações:</strong> {passed}/{total} passaram</p>
            <p><strong>Taxa de sucesso:</strong> {(passed/total*100):.1f}%</p>
        </div>
        <h2>Validações</h2>
"""

for i, v in enumerate(validations, 1):
    css_class = "pass" if v['passed'] else "fail"
    status = "✅ PASSOU" if v['passed'] else "❌ FALHOU"
    html += f"""
        <div class="validation {css_class}">
            <p class="status">{i}. {status}</p>
            <p><strong>Regra:</strong> {v['rule']}</p>
            <p><strong>Detalhes:</strong> {v['details']}</p>
        </div>
    """

html += """
    </div>
</body>
</html>
"""

# Salvar relatório
with open('docs/data_quality_report.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("📊 Relatório salvo em: docs/data_quality_report.html")