import pandas as pandas
import sqlite3

nome_arquivo = 'Simulação_Projeto_Interno_25.xlsx - Dados.csv'

try:
    df_bruto = pd.read_csv(nome_arquivo, header=1)

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

    print("\nDataFrame após limpeza inicial de coluinas e linhas:")
    print(df_bruto.head(10))

    colunas_empresa = [
        'Empresa_Contato', 'Endereço - Rua', 'Endereço - Numero',
        'Endereço - Estado', 'Endereço - Cidade', 'Endereço - CEP',
        'Razão Social', 'CNPJ', 'Distribuidora', 'Modalidade tarifária',
        'Consumo Ponta (kWh)', 'Consumo fora Ponta (kWh)', 'valor Médioda Fatura (R$)'
    ]

    df_empresas = df_bruto.dropna(subset=['CNPJ'])
    df_empresas = df_emrpesas[colunas_empresa].copy()

    df_empresas = df_empresas.rename(columns={'Empresa_Detalhe': 'Empresa_ID'})

    print("\nDataFrame de Empresas (df_empresas):")
    print(df_empresas.head())

    colunas_contato = [
        'Identificador', 'Nome', 'Cargo', 'Empresa_Contato',
        'Telefone', 'e-mail', 'Gestor_Responsavel_LUX'
    ]

    df_contatos = df_bruto[colunas_contato].copy()

    df_contatos = df_contatos.rename(columns={'Empresa_Contato': 'Empresa_ID_FK'})

    df_contatos['Gestor_Responsavel_LUX'] = df_contatos['Gestor_Resposavel_LUX'].str.strip().str.title()

    df_contatos['Empresa_ID_FK'] = df_contatos['Empresa_ID_FK'].str.replace(r'Empresa\s*(\d+).*', r'Empresa\1', regex=True).str.strip()

    print("\nDataFrame de Contatos (df_contatos):")
    print(df_contatos.head(10))

    conn = sqlite3.connect('gestao_clientes.db')
    cursor = conn.cursor()

    print("\nMigrando dados de empresa para o SQL...")
    df_empresas.to_sqp('empresas', conn, if_exists='replace', index=False)
    print("Migraçãoo de emrpesas concluída.")

    print("Migrando dados de contato para o SQL...")
    df_contatos.to_sql('contatos', conn, if_exists='replace', index=False)
    print("Migração de contatos concluída.")

    conn.commit()

    print("\nVerificando o taotal de registros na tabela 'empresas':")
    cursor.execute("SELECT COUNT(*) FROM empresas")
    print(f"Total de empresas no SQL: {cursor.fetchone()[0]}")

    print("Verificando o total de registros na tabela 'contatos':")
    cursor.execute("SELECT COUNT(*) FROM contatos")
    print(f"Total de contatos no SQL: {cursor.fetchone()[0]}")

    def obter_dashboard_resumo():
        """Caulcula e retorna o número total de contato e empresas."""
        total_contato = pd.read_sql_query("SELECT COUNT(*) FROM contatos", conn).iloc[0, 0]

        total_empresas = pd.read_sql_query("SELECT COUNT(*) FROM empresas", conn).iloc[0, 0]

        return {
            "Toltal de Contatos": total_contaos,
            "Total de Empresas": total_empresas
        }

        print("\n--- REQUISITO 1: DASHBOARD DE RESUMO ---")
        resumo = obter_dashboard_resumo()
        print(resumo)

    def detalhar_contatos_por_empresas(empresas_id):
        """Retorna todos os colaboradores (contatos) associados a uma empresa_id."""

        query = f"""
        SELECT
        c.Nome, c.Cargo, c.Telefone, c."e-mail", c.Identificador
        FROM contatos c
        WHERE c.Empresa_ID_FK = '{empresa_id}' AND c.Identificador = 'Cliente'
        """

        df_detalhe = pd.read_sql_query(query, conn)
        return df_detalhe
        print("\n--- REQUISITO 2: DETALHAMENTO POR EMRPESA (Empresa29) ---")
        detalhe_emrpesa = detalhar_contatos_por_empresas('Empresa29')
        printa(detalhe_empresa)

        def detalhar_contatos_por_gestor(gestor_nome):
            """Retorna todos os contatos sob a responsabilidade direta de um gestor LUX."""

            query = f"""
            SELECT
            c.Nome, c.Cargo, c.Empresa_ID_FK as Empresa, c.Telefone, c.Telefone, c."e-mail"
            FROM contatos c
            WHERE c.Gestor_Responsavel_lux = '{gestor_nome}'
            ORDER BY c.Empresa_ID_FK
            """

            df_gestor = pd.read_sql_query(query, conn)
            return df_gestor

            print("\n--- REQUISITO 3: GESTÂO DE CONTATOS (Jeremy Lam) ---")
            detalhe_gestor = detalhar_contatos_por_gestor('Jeremy Lam')
            print(detalhe_gestor)

            def incluir_novo_contato(dados_contato):
                """Inclui um noivo contato na tabela 'contatos' do SQL."""

                campos = ', '.join(dados_contato.keys())
                valores = tuple(dados_contato.values())

                placeholders = ', '.join(['?' for _ in valores])

                query = f"INSERT INTO contatos ({campos}) VALUES ({placeholders})"

                try:
                    cursor.execute(query, valores)
                    conn.commit()
                    print(f"\nSucesso! Novo contato '{dados_contato['Nome']}' incluído.")
                    return true
                except sqlite3.Error as e:
                    print(f"\nErro ao incluir contato: {e}")
                    return false

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




    except FileNotFoundError:
        print(f"Erro: Arquivo '{nome_arquivo}' não encontrado. Verfique o nome ou o caminho.")