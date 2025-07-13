# API Embrapa Vitivinicultura

Disponibiliza via API dados sobre consumo, produção, importação e exportação de produtos de uva em relação ao Rio Grande do Sul.
A fonte dos dados é um [site da Embrapa](http://vitibrasil.cnpuv.embrapa.br/).

TL;DR: acesse a documentação da API [aqui](https://api-embrapa-vinhos.vercel.app/docs). 

## índice

- ⚙️ Tecnologias empregadas;
- 📁 Estrutura do projeto;
- 🏛️ Arquitetura;
- 🖥️ Setup e funcionalidade geral;
- 📞 Contatos.

---

## ⚙️ Tecnologias empregadas

- FastAPI;
- Pandas;
- BeautifulSoup;
- SQLite;
- Vercel (para deploy).

---

## 📁 Estutura do projeto

├── utils/
│   ├── disclaimer.txt
│   ├── SQLite_visualizer.py
│   ├── total_scraping_to_excel.py
|   ├── total_scraping_to_SQLite.py
|   ├── vitibrasil_data.xlsx
├── api.py
├── filtered_scraping.py
├── LICENSE.txt
├── main_scraper.py
├── README.md
├── requirements.txt
├── vercel.json
└── vitibrasil_data.sqlite

A pasta utils contém 3 arquivos Python utilizados para desenvolvimento e teste da aplicação. Os demais arquivos da raiz são vitais para o funcionamento geral.

---

## 🏛️ Arquitetura

A aplicação como um todo é regida e executada pelo arquivo api.py. Através dele são feitas alterações e consultas no banco vitibrasil_data.sqlite. A rota GET do arquivo api.py aciona uma rotina de atualização dos dados disponível no arquivo filtered_scraping.py, que, por sua vez, importa uma função definida no arquivo main_scraper.py. A consulta é sempre feita no banco de dados vitibrasil_data.sqlite.py. Se o site estiver com instabilidades, o arquivo filtered_scraping.py falha e a requisição consulta diretamente o banco de dados, que possui os dados persistidos de requisições anteriores ou do scraping total feito em tempo de desenvolvimento. Isso garante solidez para a aplicação.

O deploy foi feito usando Vercel. Para configuração do Vercel, há o arquivo vercel.json. A cada atualização do repositório, temos um novo deploy automático.

- 🖥️ Setup e funcionalidade geral;

### Para fazer a aplicação rodar localmente:

1 - Abra o terminal;
2 - Rode "git clone https://github.com/otavioconquista/API_Embrapa_Vinhos.git";
3 - Crie um ambiente virtual com "python -m venv venv";
4 - Ative o ambiente virtual com "venv\Scripts\activate";
5 - Instale as dependências rodando "pip install -r requirements.txt".
6 - Rode ""uvicorn api:app --reload".

A aplicação estará ativa no endereço http://127.0.0.1:8000. Para seguir com uma requisição, siga o padrão:

http://localhost:8000/tabela/X/Y?formato=Z.

Onde X é a tabela a ser consultada, Y é o ano a ser filtrado e Z é o formato da response body.

X pode ser Producao, ProcessamentoViniferas, ProcessamentoAmericanaseh, ProcessamentoUvasdemesa, Processamentosemclassific, Comercializacao, ImportacaoVinhosdemesa, ImportacaoEspumantes, ImportacaoUvasfrescas, ImportacaoUvaspassas, ImportacaoSucodeuva, ExportacaoVinhosdemesa, ExportacaoEspumantes, ExportacaoUvasfrescas, ExportacaoSucodeuva.

Y pode ser qualquer ano desde 1970.

Z pode ser html ou json.

Um exemplo de requisição local: http://localhost:8000/tabela/Producao/2016?formato=json

### Para fazer a aplicação rodar remotamente:

É necessário abrir uma conta no Vercel, conectar a conta em um repositório GitHub contendo a aplicação e fazer o deploy. Esta aplicação já se encontra em funcionamento.

Remotamente, pode ser acessada no endereço: https://api-embrapa-vinhos.vercel.app. Para fazer uma requisição, siga exatamente a estrutura da requisição local. Exemplo: https://api-embrapa-vinhos.vercel.app/tabela/Producao/2016?formato=html

---

## 📞 Contatos

- Acesse meu LinkedIn [aqui](www.linkedin.com/in/otavioconquista)
- e-Mail: otavio1204@gmail.com

---

Aplicação desenvolvida sob efeito de [ENTROPIA, de L'Imperatrice](https://open.spotify.com/track/7dzlMlXxwC2vhpKsfhM6S5?si=6d3a3c1fe5ca4fb4).