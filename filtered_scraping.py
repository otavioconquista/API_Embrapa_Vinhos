from main_scraper import scrape_table, base_url
from db import get_connection

def update_year_table(descricao, query, ano):
    url = f"{base_url}?ano={ano}&{query}"
    print(f"[INFO] Buscando dados para '{descricao}' do ano {ano} na URL: {url}")
    df = scrape_table(url)
    if df is not None and not df.empty:
        table_name = ''.join(e for e in descricao if e.isalnum())[:25]
        print(f"[INFO] Dados encontrados. Atualizando tabela '{table_name}'...")
        df.insert(0, "Ano", ano)
        conn = get_connection()

        # Cria a tabela se não existir
        cols_def = ', '.join([f'[{c}] TEXT' for c in df.columns])
        conn.execute(f'CREATE TABLE IF NOT EXISTS [{table_name}] ({cols_def})')

        # Remove linhas antigas do ano
        print(f"[INFO] Removendo linhas antigas do ano {ano} na tabela '{table_name}'...")
        conn.execute(f"DELETE FROM [{table_name}] WHERE Ano = ?", (ano,))

        # Insere novas linhas
        print(f"[INFO] Inserindo novas linhas para o ano {ano} na tabela '{table_name}'...")
        placeholders = ', '.join(['?' for _ in df.columns])
        cols = ', '.join([f'[{c}]' for c in df.columns])
        for _, row in df.iterrows():
            conn.execute(f'INSERT INTO [{table_name}] ({cols}) VALUES ({placeholders})', tuple(row))
        
        conn.commit()
        print(f"[SUCESSO] Tabela '{table_name}' atualizada para o ano {ano}.")
        print(url)
    else:
        print(f"[AVISO] Nenhum dado encontrado para {descricao} em {ano}.")

#update_year_table("Produção", queries["Produção"], 2022)