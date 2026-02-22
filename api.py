from fastapi import FastAPI, HTTPException, Query, Path, Request
import pandas as pd
from fastapi.responses import HTMLResponse, JSONResponse
from main_scraper import queries
from filtered_scraping import update_year_table
from db import get_connection
from enum import Enum
from datetime import datetime
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

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

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Muitas requisições. Tente novamente em breve."}
    )

@app.get("/tabela/{nome}/{ano}")
@limiter.limit("10/minute")
def get_table(
    request: Request,
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

    # Tenta atualizar via scraping; se falhar, usa apenas o banco
    try:
        update_year_table(descricao, query, ano.value)
    except Exception as e:
        print(f"[AVISO] Atualização falhou (usando dados existentes no banco): {e}")
        pass  # Continua para buscar do banco

    table_name = ''.join(e for e in nome if e.isalnum())[:25]
    conn = get_connection()
    try:
        result = conn.execute(f"SELECT * FROM [{table_name}] WHERE Ano = ?", (ano.value,))
        rows = result.fetchall()
        columns = [desc[0] for desc in result.description]
        df = pd.DataFrame(rows, columns=columns)
    except Exception:
        raise HTTPException(status_code=404, detail="Tabela não encontrada")
    if df.empty:
        raise HTTPException(status_code=404, detail="Nenhum dado encontrado para este ano nesta tabela")
    if formato == "html":
        return HTMLResponse(df.to_html(index=False, border=1))
    else:
        return JSONResponse(df.to_dict(orient="records"))