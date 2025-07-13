import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Nome do banco SQLite
db_filename = 'vitibrasil_data.sqlite'

def scrape_table(url):
    # Faz a requisição HTTP para obter o conteúdo da página
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Encontra a tabela na página
    table = soup.find('table', class_='tb_base tb_dados')
    
    if table is None:
        return None
    
    # Inicializa listas para armazenar os dados e os cabeçalhos
    data = []
    headers = []
    
    # Adiciona os cabeçalhos da tabela
    for th in table.find_all('th'):
        headers.append(th.text.strip())
    
    # Adiciona os dados da tabela
    for row in table.find_all('tr')[1:]:  # Ignora o cabeçalho
        row_data = []
        for cell in row.find_all(['td', 'th']):
            row_data.append(cell.text.strip())
        if row_data:  # Verifica se a linha não está vazia
            data.append(row_data)
    
    # Cria o DataFrame
    df = pd.DataFrame(data, columns=headers)
    return df

# URL base
base_url = "http://vitibrasil.cnpuv.embrapa.br/index.php"

# Dicionário de queries
queries = {
    "Producao": "opcao=opt_02",
    "Processamento_Viniferas": "subopcao=subopt_01&opcao=opt_03",
    "Processamento_Americanas_e_hibridas": "subopcao=subopt_02&opcao=opt_03",
    "Processamento_Uvas_de_mesa": "subopcao=subopt_03&opcao=opt_03",
    "Processamento_sem_classificacao": "subopcao=subopt_04&opcao=opt_03",
    "Comercializacao": "opcao=opt_04",
    "Importacao_Vinhos_de_mesa": "subopcao=subopt_01&opcao=opt_05",
    "Importacao_Espumantes": "subopcao=subopt_02&opcao=opt_05",
    "Importacao_Uvas_frescas": "subopcao=subopt_03&opcao=opt_05",
    "Importacao_Uvas_passas": "subopcao=subopt_04&opcao=opt_05",
    "Importacao_Suco_de_uva": "subopcao=subopt_05&opcao=opt_05",
    "Exportacao_Vinhos_de_mesa": "subopcao=subopt_01&opcao=opt_06",
    "Exportacao_Espumantes": "subopcao=subopt_02&opcao=opt_06",
    "Exportacao_Uvas_frescas": "subopcao=subopt_03&opcao=opt_06",
    "Exportacao_Suco_de_uva": "subopcao=subopt_04&opcao=opt_06"
}

# Anos a serem considerados
anos = list(range(1970, datetime.now().year))