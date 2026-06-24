# =======================================
# APP.PY - Sistema Modular de Gestão SIG com Streamlit
# ORQUESTRADOR PRINCIPAL - UI, MENU, MÓDULOS VISUAIS
# =======================================
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
from io import BytesIO
from fpdf import FPDF

from finaneasy.services.acessos import (
    init_db,
    authenticate,
    register_user,
    log_audit,
    get_db_connection,
    get_user_by_username,
    update_user_profile,
    criar_conta,
    listar_contas,
    obter_conta,
    saldo_total,
    depositar,
    sacar,
    listar_transacoes
)

# =======================================
# CSS CUSTOM E CONFIGS
# =======================================
st.set_page_config(
    page_title="FinanEasy - Gestão Financeira",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main {
        padding: 2rem;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .sidebar .sidebar-content {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .metric {
        font-size: 2rem;
        font-weight: bold;
        color: #667eea;
    }
    .card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
    .header {
        color: #764ba2;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# =======================================
# INICIALIZAÇÃO DE SESSÃO
# =======================================
def init_session_state():
    """Inicializa variáveis de sessão"""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "username" not in st.session_state:
        st.session_state.username = None
    if "user_id" not in st.session_state:
        st.session_state.user_id = None
    if "user_role" not in st.session_state:
        st.session_state.user_role = None

init_session_state()

# =======================================
# INICIALIZAR BANCO DE DADOS
# =======================================
init_db()

# =======================================
# PÁGINA DE LOGIN / REGISTRO
# =======================================
def page_login():
    """Página de autenticação"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<div class='header'>💰 FinanEasy</div>", unsafe_allow_html=True)
        st.markdown("### Gestão Financeira Inteligente")
        st.divider()
        
        tab_login, tab_register = st.tabs(["🔓 Login", "📝 Registrar"])
        
        # TAB LOGIN
        with tab_login:
            st.markdown("#### Faça login em sua conta")
            username = st.text_input("Usuário", key="login_username", placeholder="Digite seu usuário")
            password = st.text_input("Senha", type="password", key="login_password", placeholder="Digite sua senha")
            
            if st.button("🔓 Entrar", use_container_width=True, key="btn_login"):
                if not username or not password:
                    st.error("⚠️ Preencha todos os campos!")
                else:
                    user = authenticate(username, password)
                    if user:
                        st.session_state.authenticated = True
                        st.session_state.username = username
                        st.session_state.user_id = user['id']
                        st.session_state.user_role = user['role']
                        
                        # Log de acesso
                        log_audit(
                            user_id=user['id'],
                            action="LOGIN",
                            details=f"Usuário {username} realizou login",
                            ip_address="localhost"
                        )
                        
                        st.success("✅ Login realizado com sucesso!")
                        st.rerun()
                    else:
                        st.error("❌ Usuário ou senha inválidos!")
                        log_audit(
                            user_id=None,
                            action="FAILED_LOGIN",
                            details=f"Tentativa de login falhada para {username}",
                            ip_address="localhost"
                        )
        
        # TAB REGISTRO
        with tab_register:
            st.markdown("#### Crie uma nova conta")
            new_username = st.text_input("Novo usuário", key="register_username", placeholder="Escolha um usuário")
            new_email = st.text_input("Email", key="register_email", placeholder="seu@email.com")
            new_password = st.text_input("Senha", type="password", key="register_password", placeholder="Crie uma senha segura")
            new_password_confirm = st.text_input("Confirme a senha", type="password", key="register_password_confirm", placeholder="Repita a senha")
            
            if st.button("📝 Registrar", use_container_width=True, key="btn_register"):
                if not all([new_username, new_email, new_password, new_password_confirm]):
                    st.error("⚠️ Preencha todos os campos!")
                elif new_password != new_password_confirm:
                    st.error("❌ As senhas não coincidem!")
                elif len(new_password) < 6:
                    st.error("❌ A senha deve ter no mínimo 6 caracteres!")
                else:
                    success, message = register_user(new_username, new_email, new_password)
                    if success:
                        st.success(f"✅ {message}")
                        st.info("Agora faça login com suas credenciais!")
                    else:
                        st.error(f"❌ {message}")

# =======================================
# PÁGINA PRINCIPAL (DASHBOARD)
# =======================================
def page_dashboard():
    """Dashboard principal após autenticação"""
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        st.markdown(f"<div class='header'>👋 Bem-vindo, {st.session_state.username}!</div>", unsafe_allow_html=True)
    
    with col3:
        if st.button("🚪 Sair"):
            log_audit(
                user_id=st.session_state.user_id,
                action="LOGOUT",
                details=f"Usuário {st.session_state.username} realizou logout",
                ip_address="localhost"
            )
            st.session_state.authenticated = False
            st.session_state.username = None
            st.session_state.user_id = None
            st.session_state.user_role = None
            st.rerun()
    
    st.divider()
    
    # Menu lateral
    with st.sidebar:
        st.markdown("### 📊 Menu de Navegação")
        menu = st.radio(
            "Selecione uma opção:",
            ["📈 Dashboard", "💳 Contas", "💰 Transações", "📊 Relatórios", "⚙️ Configurações", "📋 Auditoria"],
            label_visibility="collapsed"
        )
    
    # Renderizar páginas
    if menu == "📈 Dashboard":
        page_dashboard_main()
    elif menu == "💳 Contas":
        page_contas()
    elif menu == "💰 Transações":
        page_transacoes()
    elif menu == "📊 Relatórios":
        page_relatorios()
    elif menu == "⚙️ Configurações":
        page_configuracoes()
    elif menu == "📋 Auditoria":
        page_auditoria()

def page_dashboard_main():
    """Dashboard principal com métricas"""
    st.markdown("### 📊 Visão Geral")
    
    saldo = saldo_total(st.session_state.user_id)
    contas = listar_contas(st.session_state.user_id)
    transacoes = listar_transacoes(st.session_state.user_id, limit=5)
    
    receitas = sum(t['amount'] for t in transacoes if t['transaction_type'] == 'Depósito')
    despesas = sum(t['amount'] for t in transacoes if t['transaction_type'] == 'Saque')
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class='card'>
            <div style='color: #667eea; font-size: 0.9rem;'>Saldo Total</div>
            <div class='metric'>R$ {saldo:.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='card'>
            <div style='color: #667eea; font-size: 0.9rem;'>Receitas</div>
            <div class='metric' style='color: #28a745;'>R$ {receitas:.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='card'>
            <div style='color: #667eea; font-size: 0.9rem;'>Despesas</div>
            <div class='metric' style='color: #dc3545;'>R$ {despesas:.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class='card'>
            <div style='color: #667eea; font-size: 0.9rem;'>Contas</div>
            <div class='metric'>{len(contas)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    if transacoes:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 📈 Últimas Transações")
            df_trans = pd.DataFrame(transacoes[:5])
            st.dataframe(df_trans[['transaction_date', 'transaction_type', 'category', 'amount', 'account_name']], use_container_width=True)
        
        with col2:
            st.markdown("#### 💳 Suas Contas")
            if contas:
                df_contas = pd.DataFrame(contas)
                st.dataframe(df_contas[['account_name', 'account_type', 'bank_name', 'balance']], use_container_width=True)

def page_contas():
    """Página de gerenciamento de contas"""
    st.markdown("### 💳 Minhas Contas")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("➕ Nova Conta"):
            st.session_state.show_nova_conta = True
    
    if st.session_state.get("show_nova_conta", False):
        with st.form("nova_conta_form"):
            st.markdown("#### Criar Nova Conta")
            nome_conta = st.text_input("Nome da Conta", placeholder="Ex: Conta Principal")
            tipo_conta = st.selectbox("Tipo de Conta", ["Corrente", "Poupança", "Investimento"])
            banco = st.text_input("Nome do Banco", placeholder="Ex: Banco A")
            saldo_inicial = st.number_input("Saldo Inicial", min_value=0.0, step=0.01)
            
            if st.form_submit_button("✅ Criar Conta"):
                if nome_conta:
                    conta_id = criar_conta(st.session_state.user_id, nome_conta, tipo_conta, banco, saldo_inicial)
                    st.success(f"✅ Conta criada com sucesso! ID: {conta_id}")
                    st.session_state.show_nova_conta = False
                    st.rerun()
                else:
                    st.error("⚠️ Preencha o nome da conta!")
    
    contas = listar_contas(st.session_state.user_id)
    
    if contas:
        df = pd.DataFrame(contas)
        st.dataframe(df[['id', 'account_name', 'account_type', 'bank_name', 'balance', 'active']], use_container_width=True)
    else:
        st.info("Você não possui contas cadastradas. Crie uma nova conta!")

def page_transacoes():
    """Página de transações"""
    st.markdown("### 💰 Transações")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        tipo_trans = st.selectbox("Tipo de Transação", ["Depósito", "Saque"])
    with col2:
        if st.button("➕ Nova Transação"):
            st.session_state.show_nova_trans = True
    
    contas = listar_contas(st.session_state.user_id)
    
    if st.session_state.get("show_nova_trans", False) and contas:
        with st.form("nova_trans_form"):
            st.markdown(f"#### Registrar {tipo_trans}")
            conta_id = st.selectbox("Conta", options=[c['id'] for c in contas], 
                                   format_func=lambda x: next(c['account_name'] for c in contas if c['id'] == x))
            categoria = st.text_input("Categoria", placeholder="Ex: Salário, Alimentação")
            valor = st.number_input("Valor (R$)", min_value=0.01, step=0.01)
            descricao = st.text_area("Descrição", placeholder="Adicione uma descrição (opcional)")
            
            if st.form_submit_button(f"✅ Registrar {tipo_trans}"):
                if categoria and valor > 0:
                    if tipo_trans == "Depósito":
                        sucesso, msg = depositar(conta_id, st.session_state.user_id, valor, categoria, descricao)
                    else:
                        sucesso, msg = sacar(conta_id, st.session_state.user_id, valor, categoria, descricao)
                    
                    if sucesso:
                        st.success(f"✅ {msg}")
                        st.session_state.show_nova_trans = False
                        st.rerun()
                    else:
                        st.error(f"❌ {msg}")
                else:
                    st.error("⚠️ Preencha todos os campos!")
    
    elif not contas:
        st.warning("⚠️ Crie uma conta antes de registrar transações!")
    
    st.divider()
    st.markdown("#### Histórico de Transações")
    transacoes = listar_transacoes(st.session_state.user_id)
    
    if transacoes:
        df = pd.DataFrame(transacoes)
        st.dataframe(df[['transaction_date', 'transaction_type', 'category', 'amount', 'description', 'account_name']], use_container_width=True)
    else:
        st.info("Nenhuma transação registrada.")

def page_relatorios():
    """Página de relatórios"""
    st.markdown("### 📊 Relatórios")
    
    periodo = st.selectbox("Período", ["Últimos 7 dias", "Último mês", "Últimos 3 meses", "Último ano"])
    
    if st.button("📥 Gerar Relatório PDF"):
        st.success("✅ Relatório gerado com sucesso!")

def page_configuracoes():
    """Página de configurações"""
    st.markdown("### ⚙️ Configurações")
    
    user = get_user_by_username(st.session_state.username)
    
    with st.form("config_form"):
        st.markdown("#### Dados Pessoais")
        email = st.text_input("Email", value=user.get('email', '') if user else '')
        
        st.markdown("#### Segurança")
        nova_senha = st.text_input("Nova Senha", type="password", placeholder="Deixe em branco para manter a atual")
        confirmar_senha = st.text_input("Confirmar Senha", type="password")
        
        if st.form_submit_button("💾 Salvar Alterações"):
            if nova_senha and nova_senha != confirmar_senha:
                st.error("❌ As senhas não coincidem!")
            else:
                sucesso, msg = update_user_profile(
                    st.session_state.user_id, 
                    email=email if email != user.get('email', '') else None,
                    password=nova_senha if nova_senha else None
                )
                if sucesso:
                    st.success(f"✅ {msg}")
                else:
                    st.error(f"❌ {msg}")

def page_auditoria():
    """Página de auditoria"""
    st.markdown("### 📋 Log de Auditoria")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT datetime, action, details 
        FROM audit_log 
        WHERE user_id = ? 
        ORDER BY datetime DESC 
        LIMIT 50
    """, (st.session_state.user_id,))
    
    logs = cursor.fetchall()
    conn.close()
    
    if logs:
        df = pd.DataFrame(logs, columns=['Data/Hora', 'Ação', 'Detalhes'])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Nenhum registro de auditoria disponível")

# =======================================
# MAIN
# =======================================
def main():
    """Função principal"""
    if not st.session_state.authenticated:
        page_login()
    else:
        page_dashboard()

if __name__ == "__main__":
    main()
#Dicas Para rodar:
#####cd C:\Users\Raquel\Desktop\fineansy1.2
#python -m venv .venv
# .venv\Scripts\activate  # Ativar ambiente virtual (Windows)

#pip install streamlit pandas numpy matplotlib sqlalchemy python-dotenv
# python -m pip install --upgrade pip
# pip install streamlit 
#pip install plotly
#pip install fpdf2
#python -m streamlit run app.py arrastar o arquivo app.py


   