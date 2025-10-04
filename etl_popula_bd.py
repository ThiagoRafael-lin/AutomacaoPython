import pandas as pd
import sqlite3

nome_arquivo = 'Simulação_Projeto_Interno_25 - Dados.csv.xlsx' 

try:
    df_bruto = pd.read_excel(nome_arquivo, sheet_name=0, header=1)
except FileNotFoundError:
    print(f"ERRO CRÍTICO: Arquivo '{nome_arquivo}' não encontrado. Verifique o nome ou o caminho.")
    exit()

print("Dados brutos carregados (primeiras 5 linhas):")
print(df_bruto.head())

colunas_a_remover = [col for col in df_bruto.columns if col.startswith('Unnamed:')]
df_bruto = df_bruto.drop(columns=colunas_a_remover)

df_bruto = df_bruto.dropna(how='all')

df_bruto = df_bruto.rename(columns={
    'Empresa': 'Empresa_Contato',
    'Empresa.1' : 'Empresa_Detalhe',
    'Gestor Responsável (LUX)' : 'Gestor_Responsavel_LUX'
})

print("\nDataFrame após limpeza inicial de colunas e linhas:")
print(df_bruto.head(10))

colunas_empresa = [ 
    'Empresa_Detalhe', 'Endereço - Rua', 'Endereço - Numero',
    'Endereço - Estado', 'Endereço - Cidade', 'Endereço - CEP',
    'Razão Social', 'CNPJ', 'Distribuidora', 'Modalidade Tarifária',
    'Consumo Ponta (kWh)', 'Consumo Fora Ponta (kWh)', 'Valor Médio da Fatura (R$)'
]

df_empresas = df_bruto.dropna(subset=['CNPJ'])
df_empresas = df_empresas[colunas_empresa].copy()

df_empresas = df_empresas.rename(columns={'Empresa_Detalhe': 'Empresa_ID'})

print("\nDataFrame de Empresas (df_empresas):")
print(df_empresas.head())

colunas_contato = [
    'Identificador', 'Nome', 'Cargo', 'Empresa_Contato',
    'Telefone', 'e-mail', 'Gestor_Responsavel_LUX'
]

df_contatos = df_bruto[colunas_contato].copy()

df_contatos = df_contatos.rename(columns={'Empresa_Contato': 'Empresa_ID_FK'})

df_contatos['Gestor_Responsavel_LUX'] = df_contatos['Gestor_Responsavel_LUX'].astype(str).str.strip().str.title()
df_contatos['Empresa_ID_FK'] = df_contatos['Empresa_ID_FK'].astype(str).str.replace(r'Empresa\s*(\d+).*', r'Empresa\1', regex=True).str.strip()

print("\nDataFrame de Contatos (df_contatos):")
print(df_contatos.head(10))

conn = sqlite3.connect('gestao_clientes.db')
cursor = conn.cursor()

print("\nMigrando dados de empresa para o SQL...")
# Correção: to_sql
df_empresas.to_sql('empresas', conn, if_exists='replace', index=False)
print("Migração de empresas concluída.")

print("Migrando dados de contato para o SQL...")
df_contatos.to_sql('contatos', conn, if_exists='replace', index=False)
print("Migração de contatos concluída.")

conn.commit()

print("\nVerificando o total de registros na tabela 'empresas':")
cursor.execute("SELECT COUNT(*) FROM empresas")
print(f"Total de empresas no SQL: {cursor.fetchone()[0]}")

print("Verificando o total de registros na tabela 'contatos':")
cursor.execute("SELECT COUNT(*) FROM contatos")
print(f"Total de contatos no SQL: {cursor.fetchone()[0]}")

def obter_dashboard_resumo():
    total_contatos = pd.read_sql_query("SELECT COUNT(*) FROM contatos", conn).iloc[0, 0]
    total_empresas = pd.read_sql_query("SELECT COUNT(*) FROM empresas", conn).iloc[0, 0]

    return {
        "Total de Contatos": total_contatos,
        "Total de Empresas": total_empresas
    }

def detalhar_contatos_por_empresas(empresa_id):

    query = f"""
    SELECT
    c.Nome, c.Cargo, c.Telefone, c."e-mail", c.Identificador
    FROM contatos c
    WHERE c.Empresa_ID_FK = '{empresa_id}' AND c.Identificador = 'Cliente'
    """

    df_detalhe = pd.read_sql_query(query, conn)
    return df_detalhe

def detalhar_contatos_por_gestor(gestor_nome):

    query = f"""
    SELECT
    c.Nome, c.Cargo, c.Empresa_ID_FK as Empresa, c.Telefone, c."e-mail"
    FROM contatos c
    WHERE c.Gestor_Responsavel_LUX = '{gestor_nome}'
    ORDER BY c.Empresa_ID_FK
    """

    df_gestor = pd.read_sql_query(query, conn)
    return df_gestor

def incluir_novo_contato(dados_contato):

    campos = ', '.join([f'"{c}"' for c in dados_contato.keys()])

    valores = tuple(dados_contato.values())

    placeholders = ', '.join(['?' for _ in valores])

    query = f"INSERT INTO contatos ({campos}) VALUES ({placeholders})"

    try:
        cursor.execute(query, valores)
        conn.commit()
        print(f"\nSucesso! Novo contato '{dados_contato['Nome']}' incluído.")
        return True
    except sqlite3.Error as e:
        print(f"\nErro ao incluir contato: {e}")
        return False

novo_contato_exemplo = {
    "Identificador": "Cliente",
    "Nome": "Maria da Silva",
    "Cargo": "Diretor",
    "Empresa_ID_FK": "Empresa10",
    "Telefone": "1111-2222",
    "e-mail": "maria@exemplo.com",
    "Gestor_Responsavel_LUX": "Amanda Thompson"
}

incluir_novo_contato(novo_contato_exemplo)

print("\n--- BACK-END CONCLUÍDO. ARQUIVO 'gestao_clientes.db' CRIADO. ---")