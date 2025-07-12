import sqlite3
from main_scraper import scrape_table, queries, base_url, anos, db_filename

# Cria conexão com o banco SQLite
conn = sqlite3.connect(db_filename)

# Scrape each table and save to SQLite database
for description, query in queries.items():
    for ano in anos:
        #print(f"Scraping {description} - {ano}...")
        # Adiciona o parâmetro ano à query
        if "ano=" in query:
            url = f"{base_url}?ano={ano}&{query}"
        else:
            url = f"{base_url}?ano={ano}&{query}"
        df = scrape_table(url)
        
        if df is not None and not df.empty:
            # Nome da tabela: remove caracteres especiais e limita a 25 caracteres
            table_name = ''.join(e for e in description if e.isalnum())[:25]
            # Adiciona o ano como coluna
            df.insert(0, "Ano", ano)
            # Salva no banco, acumulando os dados (append)
            df.to_sql(table_name, conn, if_exists='append', index=False)

conn.close()
print(f"\nDados salvos no banco {db_filename}")