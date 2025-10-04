import streamlit as st
import pandas as pd
import sqlite3
import os


DB_FILE = 'gestao_clientes.db'

if not os.path.exists(DB_FILE):
    st.error(f"Erro: Arquivo do banco de dados '{DB_FILE}' não encontrado.")
    st.info("Execute o script 'etl_popula_bd.py' primeiro para criar o banco de dados.")
    st.stop()

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()


def obter_dashboard_resumo():
    total_contatos = pd.read_sql_query("SELECT COUNT(*) FROM contatos", conn).iloc[0, 0]
    total_empresas = pd.read_sql_query("SELECT COUNT(*) FROM empresas", conn).iloc[0, 0]
    
    return total_contatos, total_empresas

def obter_todas_empresas():
    query = "SELECT DISTINCT Empresa_ID FROM empresas ORDER BY Empresa_ID"
    df = pd.read_sql_query(query, conn)
    return df['Empresa_ID'].tolist()

def obter_todos_gestores():
    query = "SELECT DISTINCT Gestor_Responsavel_LUX FROM contatos ORDER BY Gestor_Responsavel_LUX"
    df = pd.read_sql_query(query, conn)
    return df['Gestor_Responsavel_LUX'].tolist()

def detalhar_contatos_por_empresas(empresa_id):
    query = f""" 
    SELECT
        c.Nome, c.Cargo, c.Telefone, c."e-mail", c.Identificador
    FROM contatos c
    WHERE c.Empresa_ID_FK = '{empresa_id}'
    """
    return pd.read_sql_query(query, conn)

def detalhar_contatos_por_gestor(gestor_nome):
    query = f"""
    SELECT
        c.Nome, c.Cargo, c.Empresa_ID_FK as Empresa, c.Telefone, c."e-mail"
    FROM contatos c
    WHERE c.Gestor_Responsavel_LUX = '{gestor_nome}'
    ORDER BY c.Empresa_ID_FK
    """
    return pd.read_sql_query(query, conn)

def incluir_novo_contato(dados_contato):
    campos = ', '.join([f'"{c}"' for c in dados_contato.keys()]) 
    valores = tuple(dados_contato.values())
    placeholders = ', '.join(['?' for _ in valores])

    query = f"INSERT INTO contatos ({campos}) VALUES ({placeholders})"

    try:
        cursor.execute(query, valores)
        conn.commit()
        return True
    except sqlite3.Error as e:
        st.error(f"Erro ao incluir contato: {e}")
        return False


st.set_page_config(layout="wide")

st.title("Sistema de Gestão de Clientes LUX Energia ⚡️")
st.sidebar.title("Navegação")

page = st.sidebar.radio("Selecione a Funcionalidade:", [
    "Dashboard de Resumo",
    "Detalhamento por Empresa",
    "Gestão por Gestor LUX",
    "Incluir Novo Contato"
])

if page == "Dashboard de Resumo":
    st.header("Dashboard de Resumo")
    
    total_contatos, total_empresas = obter_dashboard_resumo()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(label="Total de Empresas Cadastradas", value=total_empresas)
    
    with col2:
        st.metric(label="Total de Contatos Registrados", value=total_contatos)

elif page == "Detalhamento por Empresa":
    st.header("Detalhar Contatos por Empresa")
    
    empresas = obter_todas_empresas()
    
    empresa_selecionada = st.selectbox("Selecione uma Empresa:", empresas)
    
    if empresa_selecionada:
        df_detalhe = detalhar_contatos_por_empresas(empresa_selecionada)
        st.subheader(f"Contatos na {empresa_selecionada}")
        st.dataframe(df_detalhe, use_container_width=True)
        st.info(f"Total de contatos: {len(df_detalhe)}")

elif page == "Gestão por Gestor LUX":
    st.header("Gestão de Contatos por Gestor Responsável")
    
    gestores = obter_todos_gestores()
    
    gestor_selecionado = st.selectbox("Selecione um Gestor LUX:", gestores)
    
    if gestor_selecionado:
        df_gestor = detalhar_contatos_por_gestor(gestor_selecionado)
        st.subheader(f"Contatos de {gestor_selecionado}")
        st.dataframe(df_gestor, use_container_width=True)
        st.info(f"Total de contatos sob responsabilidade: {len(df_gestor)}")

elif page == "Incluir Novo Contato":
    st.header("Adicionar Novo Contato")
    
    empresas = obter_todas_empresas()
    gestores = obter_todos_gestores()

    with st.form("form_novo_contato"):
        col_id, col_nome = st.columns(2)
        with col_id:
            identificador = st.selectbox("Identificador", ["Cliente", "Prospect"], index=0)
        with col_nome:
            nome = st.text_input("Nome Completo", max_chars=100)
            
        col_cargo, col_empresa = st.columns(2)
        with col_cargo:
            cargo = st.text_input("Cargo", max_chars=100)
        with col_empresa:
            empresa_id_fk = st.selectbox("Empresa (ID)", empresas)
            
        col_tel, col_email = st.columns(2)
        with col_tel:
            telefone = st.text_input("Telefone", max_chars=50)
        with col_email:
            email = st.text_input("E-mail", max_chars=100)
        
        gestor_lux = st.selectbox("Gestor Responsável LUX", gestores)
        
        submitted = st.form_submit_button("Salvar Novo Contato")

        if submitted:
            if nome and cargo and telefone and email:
                novo_contato = {
                    "Identificador": identificador,
                    "Nome": nome,
                    "Cargo": cargo,
                    "Empresa_ID_FK": empresa_id_fk,
                    "Telefone": telefone,
                    "e-mail": email,
                    "Gestor_Responsavel_LUX": gestor_lux
                }
                
                if incluir_novo_contato(novo_contato):
                    st.success(f"Contato {nome} adicionado com sucesso!")
                else:
                    st.error("Falha ao adicionar contato. Verifique o console.")
            else:
                st.error("Preencha todos os campos obrigatórios.")