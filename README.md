## 🐍 Sistema de Gestão e Análise de Clientes

## 🌟 Visão Geral da Solução
Este projeto implementa uma solução completa de ETL (Extract, Transform, Load) e visualização de dados, utilizando Python. O objetivo é automatizar o processamento de dados brutos de clientes e fornecer uma interface web intuitiva para análise e gestão. A solução divide-se em duas partes principais:Backend (ETL): Script em Python/Pandas para limpeza, transformação e carga dos dados em um banco SQLite. Frontend (Dashboard): Aplicação interativa desenvolvida com Streamlit para visualização e gestão dos dados.

## 🛠️ Tecnologias Utilizadas

| Categoria | Tecnologias |
| :--- | :--- |
| **Linguagem Principal** | **Python** |
| **Manipulação de Dados** | **Pandas** |
| **Banco de Dados** | SQLite |
| **Interface Web** | **Streamlit** |

## 📊 Estrutura e Funcionalidades do Dashboard
O dashboard (criado com app_dashboard.py) é uma interface web que atende a quatro requisitos essenciais de gestão:

- Resumo de Métricas: Visualização de indicadores-chave de performance (KPIs).

- Detalhamento por Empresa: Consulta e análise de informações específicas por CNPJ ou nome da empresa.

- Gestão por Gestor: Filtro e análise de contatos e resultados por gestor responsável.

- Inclusão de Novos Contatos: Formulário para inserção direta de novos dados na base (funcionalidade de update).

## ⚙️ Instruções de Execução (Para Teste)
Para testar a aplicação no seu ambiente local, siga estes três passos.

- Passo 1: Preparação do Ambiente
Instale as bibliotecas e dependências necessárias listadas no arquivo requirements.txt:

Bash:
pip install -r requirements.txt

- Passo 2: Geração do Banco de Dados (ETL)
O script de Backend irá ler o arquivo Excel de origem, realizar a limpeza e popular o banco de dados gestao_clientes.db.

Bash:
python etl_popula_bd.py

- Passo 3: Inicialização do Dashboard
Inicie o aplicativo web Streamlit. O dashboard será aberto automaticamente no seu navegador padrão.

Bash:
streamlit run app_dashboard.py

## 📝 Detalhes dos Arquivos
- etl_popula_bd.py: Script de Backend responsável pela lógica de ETL.

- app_dashboard.py: Script de Frontend que gera a interface web interativa do Dashboard.

- requirements.txt: Lista de todas as bibliotecas Python necessárias (Pandas, Streamlit, etc.).

- gestao_clientes.db: Banco de dados SQLite gerado pelo processo de ETL.
