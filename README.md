1. Visão Geral da Solução
Tecnologias: Python, Pandas, SQLite e Streamlit.

Backend (ETL): O script etl_popula_bd.py é responsável por ler os dados brutos do Excel, realizar a limpeza, padronização e separação em duas tabelas (Empresas e Contatos), e carregá-los no banco de dados portátil gestao_clientes.db.

Frontend (Dashboard): O script app_dashboard.py usa o Streamlit para criar uma interface web intuitiva que atende aos quatro requisitos: Resumo de Métricas, Detalhamento por Empresa, Gestão por Gestor e Inclusão de Novos Contatos.

2. Instruções de Execução (Para Teste)
Para testar a aplicação, siga apenas estes três passos:

Passo 1: Preparação do Ambiente
Instale as bibliotecas necessárias usando o arquivo requirements.txt:

Bash:
pip install -r requirements.txt


Passo 2: Geração do Banco de Dados (ETL)
Rode o script de Backend para gerar o banco de dados gestao_clientes.db:

Bash:
python etl_popula_bd.py


Passo 3: Inicialização do Dashboard
Inicie o aplicativo web Streamlit. O dashboard será aberto automaticamente no seu navegador:

Bash:
streamlit run app_dashboard.py
