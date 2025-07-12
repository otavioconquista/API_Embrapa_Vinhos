from fastapi import FastAPI, HTTPException, Query, Path
import sqlite3
import pandas as pd
from fastapi.responses import HTMLResponse, JSONResponse
from main_scraper import queries, db_filename
from filtered_scraping import update_year_table
from enum import Enum
from datetime import datetime

# Gera lista de anos de 1970 até o ano atual
anos_disponiveis = [str(ano) for ano in range(1970, datetime.now().year)]

# Gera lista de nomes de tabelas
tabela_nomes = [
    ''.join(e for e in description if e.isalnum())[:25]
    for description in queries.keys()
]

class NomeTabelaEnum(str, Enum):
    # Cria dinamicamente os campos do Enum
    locals().update({nome: nome for nome in tabela_nomes})

class AnoEnum(str, Enum):
    locals().update({ano: ano for ano in anos_disponiveis})

app = FastAPI()

@app.get("/tabela/{nome}/{ano}")
def get_table(
    nome: NomeTabelaEnum = Path(..., description="Nome da tabela"),
    ano: AnoEnum = Path(..., description="Ano"),
    formato: str = Query("json", enum=["json", "html"])
):
    # Busca a query e a descrição correspondente
    query = None
    descricao = None
    for description, q in queries.items():
        table_name = ''.join(e for e in description if e.isalnum())[:25]
        if table_name.lower() == ''.join(e for e in nome if e.isalnum())[:25].lower():
            query = q
            descricao = description
            break
    if not query:
        raise HTTPException(status_code=404, detail="Tabela não encontrada")

    # Tenta atualizar via scraping; se falhar, usa apenas o banco local
    try:
        update_year_table(descricao, query, ano.value, db_filename=db_filename)
    except Exception as e:
        # Log opcional: print(f"Scraping falhou: {e}")
        pass  # Continua para buscar do banco

    table_name = ''.join(e for e in nome if e.isalnum())[:25]
    conn = sqlite3.connect(db_filename)
    try:
        df = pd.read_sql(f"SELECT * FROM '{table_name}' WHERE Ano = ?", conn, params=(ano.value,))
    except Exception:
        conn.close()
        raise HTTPException(status_code=404, detail="Tabela não encontrada")
    conn.close()
    if df.empty:
        raise HTTPException(status_code=404, detail="Nenhum dado encontrado para este ano nesta tabela")
    if formato == "html":
        return HTMLResponse(df.to_html(index=False, border=1))
    else:
        return JSONResponse(df.to_dict(orient="records"))