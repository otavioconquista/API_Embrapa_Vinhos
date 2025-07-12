import sqlite3
from main_scraper import scrape_table, base_url

def update_year_table(descricao, query, ano, db_filename='vitibrasil_data.sqlite'):
    url = f"{base_url}?ano={ano}&{query}"
    print(f"[INFO] Buscando dados para '{descricao}' do ano {ano} na URL: {url}")
    df = scrape_table(url)
    if df is not None and not df.empty:
        table_name = ''.join(e for e in descricao if e.isalnum())[:25]
        print(f"[INFO] Dados encontrados. Atualizando tabela '{table_name}' no banco '{db_filename}'...")
        df.insert(0, "Ano", ano)
        conn = sqlite3.connect(db_filename)
        print(f"[INFO] Removendo linhas antigas do ano {ano} na tabela '{table_name}'...")
        conn.execute(f"DELETE FROM {table_name} WHERE Ano = ?", (ano,))
        print(f"[INFO] Inserindo novas linhas para o ano {ano} na tabela '{table_name}'...")
        df.to_sql(table_name, conn, if_exists='append', index=False)
        conn.close()
        print(f"[SUCESSO] Tabela '{table_name}' atualizada para o ano {ano}.")
        print(url)
    else:
        print(f"[AVISO] Nenhum dado encontrado para {descricao} em {ano}.")

#update_year_table("Produção", queries["Produção"], 2022)