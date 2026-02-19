import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from db import get_connection

#Query para mostrar o esquema de uma tabela
def show_schema(table_name):
    conn = get_connection()
    result = conn.execute(f'PRAGMA table_info([{table_name}])')
    schema = result.fetchall()
    for col in schema:
        print(col)

#Query para mostrar os dados de uma tabela
def show_table_data(table_name):
    conn = get_connection()
    result = conn.execute(f'SELECT * FROM [{table_name}]')
    data = result.fetchall()
    columns = [desc[0] for desc in result.description]
    print("Columns:", columns)
    print("\nData:")
    for row in data:
        print(row)

#Query para mostrar os diferentes anos disponíveis na tabela
def show_years(table_name):
    conn = get_connection()
    result = conn.execute(f'SELECT DISTINCT Ano FROM [{table_name}] ORDER BY Ano')
    years = result.fetchall()
    if not years:
        print(f"No data found for table: {table_name}")
        return []
    years = [year[0] for year in years]
    print(f"Available years in table '{table_name}': {years}")

#Query para mostrar os dados de um ano específico
def show_year_data(table_name, year):
    conn = get_connection()
    result = conn.execute(f'SELECT * FROM [{table_name}] WHERE Ano = ?', (year,))
    data = result.fetchall()
    columns = [desc[0] for desc in result.description]
    if not data:
        print(f"No data found for year {year} in table: {table_name}")
        return []
    print("Columns:", columns)
    print(f"\nData for year {year}:")
    for row in data:
        print(row)

# Exemplos de uso:
#show_schema("ProcessamentodeVinferas")
#show_table_data("ImportaodeEspumantes")
#show_years("ImportaodeEspumantes")
#show_year_data("ExportaodeUvasFrescas", 1971)