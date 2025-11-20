import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

# ==============================================================================
# 1. CONFIGURAÇÃO
# ==============================================================================
LOCAL_DB_NAME = "data_core.db"
LOCAL_URI = f"sqlite:///{LOCAL_DB_NAME}"
REMOTE_URI = os.getenv("DATABASE_URL")

if not REMOTE_URI:
    print("❌ Erro: DATABASE_URL ausente.")
    exit()

if REMOTE_URI.startswith("postgres://"):
    REMOTE_URI = REMOTE_URI.replace("postgres://", "postgresql://", 1)

# ==============================================================================
# 2. ORDEM DE MIGRAÇÃO
# ==============================================================================
tabelas_ordenadas = [
    "organizacao",
    "pessoa",
    "usuario",
    "paciente",
    "endereco",
    "procedimento",
    "atendimento",
    "acesso"
]

def limpar_string(valor, max_len):
    """Função auxiliar para cortar strings e tratar Nulos/None"""
    if valor is None or pd.isna(valor) or str(valor).strip() == 'None':
        return None
    s = str(valor).strip()
    return s[:max_len]

def migrar():
    print(f"🔌 Conectando ao banco local: {LOCAL_DB_NAME}")
    
    if not os.path.exists(LOCAL_DB_NAME):
        print(f"❌ Erro: {LOCAL_DB_NAME} não encontrado.")
        return

    local_engine = create_engine(LOCAL_URI)
    remote_engine = create_engine(REMOTE_URI)

    # A. LIMPEZA DO BANCO REMOTO
    print("\n🧹 Limpando Supabase...")
    with remote_engine.connect() as remote_conn:
        remote_conn.execute(text("SET session_replication_role = 'replica';"))
        for tabela in reversed(tabelas_ordenadas):
            try:
                remote_conn.execute(text(f'TRUNCATE TABLE "{tabela}" RESTART IDENTITY CASCADE;'))
            except:
                pass
        remote_conn.execute(text("SET session_replication_role = 'origin';"))
        remote_conn.commit()

    # B. TRANSFERÊNCIA COM TRATAMENTO DE DADOS
    print("\n🚀 Iniciando cópia...\n")

    for tabela in tabelas_ordenadas:
        try:
            df = pd.read_sql(f"SELECT * FROM {tabela}", local_engine)
            
            if df.empty:
                print(f"⚠️  Tabela '{tabela}' vazia. Pulando.")
                continue

            # === TRATAMENTO DE DADOS SUJOS ===
            
            # 1. Remove a string 'None' que o Pandas/SQLite às vezes gera
            df = df.replace(['None', 'nan', 'NaN'], None)
            
            # 2. Ajustes Específicos por Tabela
            if tabela == 'pessoa':
                # --- CORREÇÃO NOVA: REMOVER DUPLICATAS DE CPF ---
                print(f"   ℹ️ Verificando duplicatas de CPF em '{tabela}'...")
                df = df.drop_duplicates(subset=['cpf'], keep='first')
                # ------------------------------------------------

                # CPF: max 11 chars
                df['cpf'] = df['cpf'].apply(lambda x: limpar_string(x, 11))
                # Raça: max 2 chars
                df['raca'] = df['raca'].apply(lambda x: limpar_string(x, 2))
                # Sexo: max 1 char
                df['sexo'] = df['sexo'].apply(lambda x: limpar_string(x, 1))

            elif tabela == 'endereco':
                df['uf'] = df['uf'].apply(lambda x: limpar_string(x, 2))
                df['tipo_logradouro'] = df['tipo_logradouro'].apply(lambda x: limpar_string(x, 3))

            elif tabela == 'procedimento':
                df['nome_procedimento'] = df['nome_procedimento'].apply(lambda x: limpar_string(x, 120))
                df['cod_procedimento'] = df['cod_procedimento'].apply(lambda x: limpar_string(x, 10))
                # Remover duplicatas de código de procedimento também, por garantia
                df = df.drop_duplicates(subset=['cod_procedimento'], keep='first')

            elif tabela == 'atendimento':
                df['carater_atendimento'] = df['carater_atendimento'].apply(lambda x: limpar_string(x, 2))
                df['cid'] = df['cid'].apply(lambda x: limpar_string(x, 4))

            elif tabela == 'organizacao':
                 df['codigo'] = df['codigo'].apply(lambda x: limpar_string(x, 6))

            # =================================

            print(f"📤 Enviando {len(df)} registros para '{tabela}'...")
            df.to_sql(tabela, remote_engine, if_exists='append', index=False)
            print(f"✅ Sucesso: '{tabela}' migrada.")

        except Exception as e:
            print(f"❌ FALHA em '{tabela}': {e}")
            # Se a tabela pessoa falhar, paramos o script, pois o resto vai falhar também
            if tabela == 'pessoa':
                print("⛔ Parando migração pois a tabela base 'pessoa' falhou.")
                break

    print("\n🏁 Finalizado!")

if __name__ == "__main__":
    migrar()