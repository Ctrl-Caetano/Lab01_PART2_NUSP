import pandas as pd
from sqlalchemy import create_engine
import os


def ingest_data(csv_path: str, table_name: str):
    """
    Ingere dados CSV para PostgreSQL
    """
    print(f"🚀 Iniciando ingestão de {csv_path}...")
    
    # Ler CSV
    print("📖 Lendo CSV...")
    df = pd.read_csv(csv_path, index_col=0)
    print(f"✅ {len(df)} linhas lidas")
    
    # Conectar ao PostgreSQL
    print("🔌 Conectando ao PostgreSQL...")
    db_host = os.getenv('DB_HOST', 'localhost')
    engine = create_engine(
        f'postgresql://postgres:123@{db_host}:5434/lab01b'
    )
    # Ingerir dados (camada RAW)
    print(f"💾 Salvando em raw.{table_name}...")
    df.to_sql(
        table_name, 
        engine, 
        schema='raw',
        if_exists='append',
        index=False, 
        chunksize=10000
    )
    
    print(f"\n✅ Ingestão completa! {len(df)} linhas em raw.{table_name}")

if __name__ == "__main__":
    csv_path = r"D:\Python\spotify_data.csv"
    table_name = "spotify_tracks"
    
    ingest_data(csv_path, table_name)