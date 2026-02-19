import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from main_scraper import scrape_table, queries, base_url, anos
from db import get_connection

# Cria conexão com o Turso
conn = get_connection()

# Faz o scraping para cada query e ano
for description, query in queries.items():
    for ano in anos:
        url = f"{base_url}?ano={ano}&{query}"
        df = scrape_table(url)
        
        if df is not None and not df.empty:
            # Nome da tabela: remove caracteres especiais e limita a 25 caracteres
            table_name = ''.join(e for e in description if e.isalnum())[:25]
            # Adiciona o ano como coluna
            df.insert(0, "Ano", ano)

            # Cria a tabela se não existir
            cols_def = ', '.join([f'[{c}] TEXT' for c in df.columns])
            conn.execute(f'CREATE TABLE IF NOT EXISTS [{table_name}] ({cols_def})')

            # Insere os dados
            placeholders = ', '.join(['?' for _ in df.columns])
            cols = ', '.join([f'[{c}]' for c in df.columns])
            for _, row in df.iterrows():
                conn.execute(f'INSERT INTO [{table_name}] ({cols}) VALUES ({placeholders})', tuple(row))
            
            conn.commit()
            print(f"[OK] {table_name} - {ano}")

print("\nDados salvos no Turso com sucesso!")