import pandas as pd
from main_scraper import scrape_table, queries, base_url, anos

# Dicionário para armazenar todos os DataFrames
all_data = {}

for description, query in queries.items():
    frames = []
    for ano in anos:
        url = f"{base_url}{query}&ano={ano}"
        df = scrape_table(url)
        if df is not None and not df.empty:
            df.insert(0, "Ano", ano)
            frames.append(df)
    if frames:
        all_data[description] = pd.concat(frames, ignore_index=True)

# Salva cada DataFrame em uma aba do Excel
excel_filename = 'vitibrasil_data.xlsx'
with pd.ExcelWriter(excel_filename) as writer:
    for description, df in all_data.items():
        sheet_name = ''.join(e for e in description if e.isalnum())[:25]
        df.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"\nDados salvos no arquivo Excel: {excel_filename}")