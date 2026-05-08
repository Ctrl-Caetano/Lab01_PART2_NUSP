import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sqlalchemy import create_engine

print("Carregando dados...")
engine = create_engine('postgresql://postgres:123@localhost:5434/lab01b')
df = pd.read_sql_table('spotify_tracks', engine, schema='raw')
print(f"✅ {len(df)} linhas carregadas\n")

# Query 1: Top 15 artistas por número de músicas
df_artists = df.groupby('artist_name').size().reset_index(name='total')
df_artists = df_artists.nlargest(15, 'total')

# Query 2: Top 15 artistas por popularidade
df_pop = df.groupby('artist_name')['popularity'].mean().reset_index()
df_pop = df_pop.nlargest(15, 'popularity')

# Query 3: Top 15 gêneros por popularidade
df_genres = df.groupby('genre')['popularity'].mean().reset_index()
df_genres = df_genres.nlargest(15, 'popularity')

# Query 4: Evolução por ano (últimos 25 anos)
df_years = df[df['year'] >= 2000].groupby('year').size().reset_index(name='total')

# Query 5: Distribuição de energia (energy)
energy_bins = pd.cut(df['energy'], bins=10)
df_energy = energy_bins.value_counts().sort_index().reset_index()
df_energy.columns = ['range', 'count']

# Query 6: Correlação entre danceability e popularity
df_corr = df[['danceability', 'popularity']].copy()
df_corr['dance_bin'] = pd.cut(df_corr['danceability'], bins=10)
df_corr_agg = df_corr.groupby('dance_bin')['popularity'].mean().reset_index()

# Dashboard
fig = make_subplots(
    rows=3, cols=2,
    subplot_titles=(
        'Top 15 Artistas por Número de Músicas',
        'Top 15 Artistas por Popularidade Média',
        'Top 15 Gêneros por Popularidade',
        'Evolução de Lançamentos (2000-2024)',
        'Distribuição de Energia das Músicas',
        'Popularidade vs Danceability'
    ),
    specs=[[{"type": "bar"}, {"type": "bar"}],
           [{"type": "bar"}, {"type": "scatter"}],
           [{"type": "bar"}, {"type": "scatter"}]]
)

# Gráfico 1
fig.add_trace(
    go.Bar(x=df_artists['artist_name'], y=df_artists['total'],
           marker_color='indianred', text=df_artists['total'],
           textposition='outside'),
    row=1, col=1
)

# Gráfico 2
fig.add_trace(
    go.Bar(x=df_pop['artist_name'], y=df_pop['popularity'],
           marker_color='royalblue',
           text=[f"{val:.1f}" for val in df_pop['popularity']],
           textposition='outside'),
    row=1, col=2
)

# Gráfico 3
fig.add_trace(
    go.Bar(x=df_genres['genre'], y=df_genres['popularity'],
           marker_color='lightsalmon',
           text=[f"{val:.1f}" for val in df_genres['popularity']],
           textposition='outside'),
    row=2, col=1
)

# Gráfico 4
fig.add_trace(
    go.Scatter(x=df_years['year'], y=df_years['total'],
               mode='lines+markers', line=dict(color='green', width=3),
               marker=dict(size=8)),
    row=2, col=2
)

# Gráfico 5
fig.add_trace(
    go.Bar(x=[str(r) for r in df_energy['range']], y=df_energy['count'],
           marker_color='purple'),
    row=3, col=1
)

# Gráfico 6
fig.add_trace(
    go.Scatter(x=[r.mid for r in df_corr_agg['dance_bin']], 
               y=df_corr_agg['popularity'],
               mode='lines+markers', line=dict(color='orange', width=3)),
    row=3, col=2
)

# Layout
fig.update_layout(
    title_text="<b>Dashboard Spotify - Análise Completa de Dados Musicais</b>",
    title_font_size=22,
    height=1200,
    showlegend=False
)

fig.update_xaxes(tickangle=45, row=1, col=1)
fig.update_xaxes(tickangle=45, row=1, col=2)
fig.update_xaxes(tickangle=45, row=2, col=1)
fig.update_xaxes(tickangle=45, row=3, col=1)

fig.update_yaxes(title_text="Total", row=1, col=1)
fig.update_yaxes(title_text="Popularidade", row=1, col=2)
fig.update_yaxes(title_text="Popularidade", row=2, col=1)
fig.update_yaxes(title_text="Total", row=2, col=2)
fig.update_yaxes(title_text="Quantidade", row=3, col=1)
fig.update_yaxes(title_text="Popularidade", row=3, col=2)

# Salvar
fig.write_html("docs/dashboard.html")
print("✅ Dashboard salvo em: docs/dashboard.html")