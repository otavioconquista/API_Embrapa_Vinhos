# API Embrapa Vitivinicultura

Disponibiliza via API dados sobre consumo, produção, importação e exportação de produtos de uva em relação ao Rio Grande do Sul.
A fonte dos dados é um [site da Embrapa](http://vitibrasil.cnpuv.embrapa.br/).

**TL;DR**: acesse a documentação da API [aqui](https://api-embrapa-vinhos.vercel.app/docs). 

## índice

- ⚙️ Tecnologias empregadas;
- 📁 Estrutura do projeto;
- 🏛️ Arquitetura;
- 🖥️ Setup e funcionalidade geral;
- 📞 Contatos.

## ⚙️ Tecnologias empregadas

- FastAPI;
- Pandas;
- BeautifulSoup;
- Turso (banco de dados SQLite na nuvem);
- Vercel (para deploy).

## 📁 Estrutura do projeto

├── utils/  
│   ├── disclaimer.txt  
│   ├── SQLite_visualizer.py  
│   ├── total_scraping_to_excel.py  
│   ├── total_scraping_to_SQLite.py  
│   ├── vitibrasil_data.xlsx  
├── api.py  
├── db.py  
├── filtered_scraping.py  
├── LICENSE.txt  
├── main_scraper.py  
├── README.md  
├── requirements.txt  
└── vercel.json  

A pasta utils contém arquivos Python utilizados para desenvolvimento e teste da aplicação. Os demais arquivos da raiz são vitais para o funcionamento geral.

## 🏛️ Arquitetura

A aplicação como um todo é regida e executada pelo arquivo api.py. A conexão com o banco de dados é gerenciada pelo arquivo db.py, que conecta ao Turso — um banco SQLite hospedado na nuvem. A rota GET do arquivo api.py aciona uma rotina de atualização dos dados disponível no arquivo filtered_scraping.py, que, por sua vez, importa uma função definida no arquivo main_scraper.py. A cada requisição, os dados são raspados do site da Embrapa e persistidos no Turso, garantindo que o banco esteja sempre atualizado. Se o site estiver com instabilidades, o filtered_scraping.py falha e a requisição consulta diretamente o banco de dados, que possui os dados persistidos de requisições anteriores. Isso garante solidez para a aplicação.

O deploy foi feito usando Vercel. Para configuração do Vercel, há o arquivo vercel.json. A cada atualização do repositório, temos um novo deploy automático. As credenciais do Turso são configuradas como variáveis de ambiente na Vercel (TURSO_DATABASE_URL e TURSO_AUTH_TOKEN).

## 🖥️ Setup e funcionalidade geral

### Para fazer a aplicação rodar localmente:

1 - Abra o terminal;  
2 - Rode "git clone https://github.com/otavioconquista/API_Embrapa_Vinhos.git";  
3 - Crie um ambiente virtual com "python -m venv venv";  
4 - Ative o ambiente virtual com "venv\Scripts\activate";  
5 - Instale as dependências rodando "pip install -r requirements.txt";  
6 - Configure as variáveis de ambiente do Turso:  
    - `set TURSO_DATABASE_URL=<sua_url>`  
    - `set TURSO_AUTH_TOKEN=<seu_token>`  
7 - Rode "uvicorn api:app --reload".  

A aplicação estará ativa no endereço http://127.0.0.1:8000.

Para seguir com uma requisição, siga o padrão: http://localhost:8000/tabela/X/Y?formato=Z.

Onde X é a tabela a ser consultada, Y é o ano a ser filtrado e Z é o formato da response body.

- X pode ser Producao, ProcessamentoViniferas, ProcessamentoAmericanaseh, ProcessamentoUvasdemesa, Processamentosemclassific, Comercializacao, ImportacaoVinhosdemesa, ImportacaoEspumantes, ImportacaoUvasfrescas, ImportacaoUvaspassas, ImportacaoSucodeuva, ExportacaoVinhosdemesa, ExportacaoEspumantes, ExportacaoUvasfrescas, ExportacaoSucodeuva.

- Y pode ser qualquer ano desde 1970.

- Z pode ser html ou json.

Um exemplo de requisição local: http://localhost:8000/tabela/Producao/2016?formato=json.

### Para fazer a aplicação rodar remotamente:

É necessário abrir uma conta no Vercel, conectar a conta em um repositório GitHub contendo a aplicação e fazer o deploy. Também é necessário configurar as variáveis de ambiente `TURSO_DATABASE_URL` e `TURSO_AUTH_TOKEN` no painel da Vercel (Settings → Environment Variables).

Esta aplicação já se encontra em funcionamento. Remotamente, pode ser acessada no endereço: https://api-embrapa-vinhos.vercel.app. Para fazer uma requisição, siga exatamente a estrutura da requisição local.

Exemplo: https://api-embrapa-vinhos.vercel.app/tabela/Producao/2019?formato=json.

## 📞 Contatos

- Acesse meu LinkedIn [aqui](https://www.linkedin.com/in/otavioconquista)
- e-Mail: otavio1204@gmail.com

---

Aplicação desenvolvida sob efeito de [ENTROPIA, de L'Imperatrice](https://open.spotify.com/track/7dzlMlXxwC2vhpKsfhM6S5?si=6d3a3c1fe5ca4fb4).