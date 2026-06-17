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

from services.acessos import (
    init_db, 
    authenticate, 
    register_user,
    log_audit, 
    get_db_connection,
    get_user_by_username,
    update_user_profile
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
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class='card'>
            <div style='color: #667eea; font-size: 0.9rem;'>Saldo Total</div>
            <div class='metric'>R$ 5.420,00</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='card'>
            <div style='color: #667eea; font-size: 0.9rem;'>Receitas</div>
            <div class='metric' style='color: #28a745;'>R$ 8.230,50</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='card'>
            <div style='color: #667eea; font-size: 0.9rem;'>Despesas</div>
            <div class='metric' style='color: #dc3545;'>R$ 2.810,50</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class='card'>
            <div style='color: #667eea; font-size: 0.9rem;'>Transações</div>
            <div class='metric'>127</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📈 Evolução do Saldo")
        data = {
            'Data': pd.date_range('2024-01-01', periods=12, freq='M'),
            'Saldo': np.cumsum(np.random.randn(12) * 500 + 300)
        }
        df = pd.DataFrame(data)
        fig = px.line(df, x='Data', y='Saldo', title='Saldo ao Longo do Tempo', markers=True)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 💰 Distribuição de Categorias")
        data = {
            'Categoria': ['Alimentação', 'Transporte', 'Saúde', 'Educação', 'Outros'],
            'Valor': [450, 320, 180, 250, 210]
        }
        df = pd.DataFrame(data)
        fig = px.pie(df, values='Valor', names='Categoria', title='Gastos por Categoria')
        st.plotly_chart(fig, use_container_width=True)

def page_contas():
    """Página de gerenciamento de contas"""
    st.markdown("### 💳 Minhas Contas")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("➕ Nova Conta"):
            st.info("Funcionalidade em desenvolvimento")
    
    # Exemplo de dados
    contas = pd.DataFrame({
        'Conta': ['Principal', 'Poupança', 'Investimentos'],
        'Banco': ['Banco A', 'Banco B', 'Banco C'],
        'Saldo': ['R$ 5.420,00', 'R$ 2.150,00', 'R$ 8.900,00'],
        'Status': ['✅ Ativa', '✅ Ativa', '✅ Ativa']
    })
    
    st.dataframe(contas, use_container_width=True)

def page_transacoes():
    """Página de transações"""
    st.markdown("### 💰 Transações")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        tipo = st.selectbox("Tipo de Transação", ["Receita", "Despesa"])
    with col2:
        if st.button("➕ Nova Transação"):
            st.info("Funcionalidade em desenvolvimento")
    
    # Exemplo de dados
    transacoes = pd.DataFrame({
        'Data': pd.date_range('2024-01-01', periods=5),
        'Tipo': ['Receita', 'Despesa', 'Receita', 'Despesa', 'Despesa'],
        'Categoria': ['Salário', 'Alimentação', 'Freelance', 'Transporte', 'Saúde'],
        'Valor': ['R$ 3.500,00', '-R$ 450,00', 'R$ 1.200,00', '-R$ 150,00', '-R$ 200,00']
    })
    
    st.dataframe(transacoes, use_container_width=True)

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
        telefone = st.text_input("Telefone", placeholder="(11) 99999-9999")
        
        st.markdown("#### Segurança")
        nova_senha = st.text_input("Nova Senha", type="password", placeholder="Deixe em branco para manter a atual")
        confirmar_senha = st.text_input("Confirmar Senha", type="password")
        
        if st.form_submit_button("💾 Salvar Alterações"):
            st.success("✅ Configurações atualizadas com sucesso!")

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
