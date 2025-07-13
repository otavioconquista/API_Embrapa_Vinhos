import sqlite3

#Query para mostrar o esquema de uma tabela
def show_schema(table_name, db_filename='vitibrasil_data.sqlite'):
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()
    cursor.execute(f'PRAGMA table_info("{table_name}")')
    schema = cursor.fetchall()
    conn.close()
    for col in schema:
        print(col)

#Query para mostrar os dados de uma tabela
def show_table_data(table_name, db_filename='vitibrasil_data.sqlite'):
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM "{table_name}"')
    data = cursor.fetchall()
    cursor.execute(f'PRAGMA table_info("{table_name}")')
    columns = [col[1] for col in cursor.fetchall()]
    conn.close()
    print("Columns:", columns)
    print("\nData:")
    for row in data:
        print(row)

#Query para mostrar os diferentes anos disponíveis na tabela
def show_years(table_name, db_filename='vitibrasil_data.sqlite'):
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()
    cursor.execute(f'SELECT DISTINCT Ano FROM "{table_name}" ORDER BY Ano')
    years = cursor.fetchall()
    conn.close()
    if not years:
        print(f"No data found for table: {table_name}")
        return []
    years = [year[0] for year in years]
    print(f"Available years in table '{table_name}': {years}")

#Query para mostrar os dados de um ano específico
def show_year_data(table_name, year, db_filename='vitibrasil_data.sqlite'):
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM "{table_name}" WHERE Ano = ?', (year,))
    data = cursor.fetchall()
    cursor.execute(f'PRAGMA table_info("{table_name}")')
    columns = [col[1] for col in cursor.fetchall()]
    conn.close()
    if not data:
        print(f"No data found for year {year} in table: {table_name}")
        return []
    print("Columns:", columns)
    print(f"\nData for year {year}:")
    for row in data:
        print(row)

# Exemplos de uso:
#show_schema("ProcessamentodeViníferas")
#show_table_data("ImportaçãodeEspumantes")
#show_years("ImportaçãodeEspumantes")
#show_year_data("ExportaçãodeUvasFrescas", 1971)